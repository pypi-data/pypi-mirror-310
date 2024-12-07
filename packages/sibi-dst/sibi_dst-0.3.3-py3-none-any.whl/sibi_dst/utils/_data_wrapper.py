import datetime
from typing import Type, Any, Dict, Optional
import fsspec
import pandas as pd
from IPython.display import display

from sibi_dst.utils import Logger
from tqdm import tqdm
from sibi_dst.utils import ParquetSaver


logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')

class DataWrapper:
    DEFAULT_MAX_AGE_MINUTES = 1440
    DEFAULT_HISTORY_DAYS_THRESHOLD = 30

    def __init__(self,
                 dataclass: Type,
                 date_field: str,
                 data_path: str,
                 parquet_filename: str,
                 start_date: Any,
                 end_date: Any,
                 filesystem_type: str = "file",
                 filesystem_options: Optional[Dict] = None,
                 verbose: bool = False,
                 class_params: Optional[Dict] = None,
                 load_params: Optional[Dict] = None,
                 reverse_order: bool = False,
                 overwrite: bool = False,
                 ignore_missing: bool = False,
                 max_age_minutes: int = DEFAULT_MAX_AGE_MINUTES,
                 history_days_threshold: int = DEFAULT_HISTORY_DAYS_THRESHOLD,
                 show_progress: bool = False):
        self.dataclass = dataclass
        self.date_field = date_field
        self.data_path = self.ensure_forward_slash(data_path)
        self.parquet_filename = parquet_filename
        self.filesystem_type = filesystem_type
        self.filesystem_options = filesystem_options or {}
        self.fs = fsspec.filesystem(filesystem_type, **self.filesystem_options)
        self.verbose = verbose
        self.class_params = class_params or {}
        self.load_params = load_params or {}
        self.reverse_order = reverse_order
        self.overwrite = overwrite
        self.ignore_missing = ignore_missing
        self.max_age_minutes = max_age_minutes
        self.history_days_threshold = history_days_threshold
        self.show_progress = show_progress

        self.start_date = self.convert_to_date(start_date)
        self.end_date = self.convert_to_date(end_date)

    @staticmethod
    def convert_to_date(date: Any) -> datetime.date:
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d').date() if isinstance(date, str) else date
        except ValueError as e:
            logger.error(f"Error converting {date} to datetime: {e}")
            raise

    @staticmethod
    def ensure_forward_slash(path: str) -> str:
        return path if path.endswith('/') else path + '/'

    def generate_date_range(self):
        step = -1 if self.reverse_order else 1
        start, end = (self.end_date, self.start_date) if self.reverse_order else (self.start_date, self.end_date)
        current_date = start
        while current_date != end + datetime.timedelta(days=step):
            yield current_date
            current_date += datetime.timedelta(days=step)

    def process(self):
        """Execute the update plan following the specified hierarchy."""
        update_plan, update_plan_table = self.generate_update_plan_with_conditions()

        # Display the update plan table to the user

        display(update_plan_table)

        # Process files according to the hierarchy, considering only `update_required` dates
        for category, description in [
            ("overwrite", "Processing files due to overwrite=True"),
            ("history_days", "Processing files within history_days_threshold"),
            ("missing_files", "Processing missing files")
        ]:
            # Filter dates in the category where `update_required` is True
            dates_to_process = update_plan_table[
                (update_plan_table["update_category"] == category) & (update_plan_table["update_required"])
                ]["date"].tolist()

            for current_date in tqdm(dates_to_process, desc=description, unit="date"):
                self.process_date(current_date)

    def is_file_older_than(self, file_path: str, current_date: datetime.date) -> bool:
        """Check if a file is older than the specified max_age_minutes."""
        if not self.fs.exists(file_path):
            return True

        file_modification_time = self.fs.info(file_path)['mtime']
        file_modification_date = datetime.datetime.utcfromtimestamp(file_modification_time).date()
        file_age_days = (datetime.date.today() - file_modification_date).days

        # Apply max_age_minutes only for files within the history threshold
        if self.history_days_threshold and current_date >= datetime.date.today() - datetime.timedelta(
                days=self.history_days_threshold):
            file_age_seconds = (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(
                file_modification_time)).total_seconds()
            if self.verbose:
                logger.info(f"File {file_path} is {round((file_age_seconds / 60), 0)} minutes old")
            return file_age_seconds / 60 > self.max_age_minutes or self.max_age_minutes == 0

        return False

    def process_date(self, date: datetime.date):
        """Process a specific date by regenerating data as necessary."""
        folder = f'{self.data_path}{date.year}/{date.month:02d}/{date.day:02d}/'
        full_parquet_filename = f"{folder}{self.parquet_filename}"

        start_time = datetime.datetime.now()

        if self.verbose:
            logger.info(f"Processing {full_parquet_filename}...")

        data_object = self.dataclass(**self.class_params)
        #date_filter_params = {
        #    f'{self.date_field}__year': date.year,
        #    f'{self.date_field}__month': date.month,
        #    f'{self.date_field}__day': date.day
        #}
        df=data_object.load_period(dt_field=self.date_field, start=date, end=date)
        #df = data_object.load(**self.load_params, **date_filter_params)

        if len(df.index) == 0:
            if self.verbose:
                logger.info("No data found for the specified date.")
            return

        parquet_saver = ParquetSaver(df, folder, logger)
        parquet_saver.save_to_parquet(self.parquet_filename, clear_existing=True)

        end_time = datetime.datetime.now()
        duration_seconds = (end_time - start_time).total_seconds()

        if self.verbose:
            logger.info(f"Data saved to {full_parquet_filename}. Processing time: {duration_seconds:.2f} seconds")


    def remove_empty_directories(self, path: str):
        if not self.fs.isdir(path) or self.fs.abspath(path) == self.fs.abspath(self.data_path):
            return

        if not self.fs.ls(path):  # Check if directory is empty
            try:
                self.fs.rmdir(path)
                if self.verbose:
                    logger.info(f"Removed empty directory: {path}")
                self.remove_empty_directories(self.fs.path.dirname(path))
            except Exception as e:
                if self.verbose:
                    logger.error(f"Error removing directory {path}: {e}")
        else:
            if self.verbose:
                logger.info(f"Directory not empty, stopping: {path}")

    def generate_update_plan_with_conditions(self):
        """
        Generate an update plan that evaluates files based on the specified hierarchy:
        1. Overwrite (all files regenerated).
        2. History threshold: Files within `history_days_threshold` are evaluated for `max_age_minutes`.
        3. Missing files: Detect missing files, ignoring future dates.
        """
        update_plan = {
            "overwrite": [],
            "history_days": [],
            "missing_files": []
        }
        rows = []

        today = datetime.date.today()
        history_start_date = today - datetime.timedelta(days=self.history_days_threshold) if self.history_days_threshold else None

        for current_date in tqdm(self.generate_date_range(), desc="Evaluating update plan", unit="date"):
            folder = f'{self.data_path}{current_date.year}/{current_date.month:02d}/{current_date.day:02d}/'
            full_parquet_filename = f"{folder}{self.parquet_filename}"

            file_exists = self.fs.exists(full_parquet_filename)
            file_is_old = False
            within_history = False
            missing_file = not file_exists and not self.ignore_missing
            category = None

            # Hierarchy 1: Overwrite (all files are marked for regeneration)
            if self.overwrite:
                category = "overwrite"

            # Hierarchy 2: History threshold evaluation
            elif self.history_days_threshold and history_start_date and history_start_date <= current_date <= today:
                within_history = True
                if missing_file or self.is_file_older_than(full_parquet_filename, current_date):
                    category = "history_days"

            # Hierarchy 3: Detect missing files, ignoring future dates
            elif missing_file and current_date <= today:
                category = "missing_files"

            # Append to update plan
            if category:
                update_plan[category].append(current_date)

            # Collect condition descriptions for the update plan table
            rows.append({
                "date": current_date,
                "file_exists": file_exists,
                "file_is_old": file_is_old,
                "within_history": within_history,
                "missing_file": missing_file,
                "update_required": category is not None,
                "update_category": category
            })

        # Sort dates in descending order if reverse_order is True
        if self.reverse_order:
            for key in update_plan:
                update_plan[key].sort(reverse=True)

        update_plan_table = pd.DataFrame(rows)
        return update_plan, update_plan_table

# Usage:
# wrapper = DataWrapper(
#     dataclass=YourDataClass,
#     date_field="created_at",
#     data_path="/path/to/data",
#     parquet_filename="data.parquet",
#     start_date="2022-01-01",
#     end_date="2022-12-31",
#     filesystem_type="file",
#     verbose=True
# )
# wrapper.process()
# wrapper = DataWrapper(
#    dataclass=YourDataClass,
#    date_field="created_at",
#    data_path="s3://your-bucket-name/path/to/data",
#    parquet_filename="data.parquet",
#    start_date="2022-01-01",
#    end_date="2022-12-31",
#    filesystem_type="s3",
#    filesystem_options={
#        "key": "your_aws_access_key",
#        "secret": "your_aws_secret_key",
#        "client_kwargs": {"endpoint_url": "https://s3.amazonaws.com"}
#    },
#    verbose=True
#)
#wrapper.process()
