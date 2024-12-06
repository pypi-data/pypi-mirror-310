import datetime
import fsspec


class FilePathGenerator:
    """
    Dynamically generates file paths by scanning directories starting from the base path
    and determining the innermost directory structure.

    Example Usage:
        generator = FilePathGenerator(
            base_path='IbisDataWH/logistics_storage/products/tracking'
        )
        file_paths = generator.generate_file_paths('2024-11-01', '2024-11-12')
        print(file_paths)
    """

    def __init__(self, base_path=''):
        self.base_path = base_path.rstrip('/')

    def generate_file_paths(self, start_date, end_date):
        """
        Generate paths dynamically for files within the date range by scanning directories.
        """
        start_date = self._convert_to_datetime(start_date)
        end_date = self._convert_to_datetime(end_date)

        paths = []
        curr_date = start_date

        while curr_date <= end_date:
            year, month, day = curr_date.year, curr_date.month, curr_date.day
            day_path = self._determine_innermost_path(year, month, day)
            if day_path:
                paths.append(day_path)
            curr_date += datetime.timedelta(days=1)

        return paths

    def _determine_innermost_path(self, year, month, day):
        """
        Determine the innermost directory for a given year, month, and day by scanning the structure.
        """
        base_dir = f"{self.base_path}/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}"
        fs, _ = fsspec.core.url_to_fs(base_dir)

        if not fs.exists(base_dir):
            return None

        # Scan the innermost directories dynamically
        potential_dirs = fs.ls(base_dir, detail=True)
        innermost_dir = None

        for item in potential_dirs:
            if item["type"] == "directory":
                # Recursively check for subdirectories
                innermost_dir = self._get_innermost_directory(item["name"], fs)
                break  # Take the first directory for the innermost path

        if innermost_dir:
            return f"{innermost_dir}/*.parquet"

        return None

    def _get_innermost_directory(self, path, fs):
        """
        Recursively scan for the innermost directory containing files or further subdirectories.
        """
        potential_dirs = fs.ls(path, detail=True)

        for item in potential_dirs:
            if item["type"] == "directory":
                # Continue descending into subdirectories
                return self._get_innermost_directory(item["name"], fs)

        # If no subdirectories, return the current path
        return path

    @staticmethod
    def _convert_to_datetime(date):
        """Convert a date string or datetime object into a datetime object."""
        if isinstance(date, str):
            return datetime.datetime.strptime(date, '%Y-%m-%d')
        return date

# # Example usage
# if __name__ == "__main__":
#     generator = FilePathGenerator(base_path='s3://your/base/path')
#     paths = generator.generate_file_paths('2022-01-01', '2022-03-31')
#     for path in paths:
#         print(path)
# import os
# import glob
# import datetime
# import fsspec
# class FilePathGenerator:
#     # Example Usage:
#     # generator = FilePathGenerator(base_path='/your/base/path')
#     # file_paths = generator.generate_file_paths('2022-01-01', '2022-03-31')
#     # print(file_paths)
#     def __init__(self, base_path=''):
#         self.base_path = base_path.rstrip('/')
#
#     @staticmethod
#     def _get_day_file_path(dir_path, day):
#         return f"{dir_path}/{str(day).zfill(2)}/*.parquet"
#
#     @staticmethod
#     def _get_month_file_path(dir_path):
#         return f"{dir_path}/*/*.parquet"
#
#     def generate_file_paths(self, start_date, end_date):
#         start_date = self._convert_to_datetime(start_date)
#         end_date = self._convert_to_datetime(end_date)
#
#         file_paths = []
#         curr_date = start_date
#
#         while curr_date <= end_date:
#             year, month = curr_date.year, curr_date.month
#             dir_path = f"{self.base_path}/{year}/{str(month).zfill(2)}"
#
#             if os.path.exists(dir_path):
#                 file_paths.extend(self._get_files_for_month(curr_date, start_date, end_date, dir_path))
#
#             curr_date = self._increment_month(curr_date)
#
#         return file_paths
#
#     @staticmethod
#     def _convert_to_datetime(date):
#         if isinstance(date, str):
#             return datetime.datetime.strptime(date, '%Y-%m-%d')
#         return date
#
#     def _get_files_for_month(self, curr_date, start_date, end_date, dir_path):
#         files = []
#         if curr_date.year == start_date.year and curr_date.month == start_date.month:
#             if curr_date.year == end_date.year and curr_date.month == end_date.month:
#                 files.extend(self._get_files_for_range(dir_path, start_date.day, end_date.day))
#             else:
#                 start_day = start_date.day if start_date.day > 1 else 1
#                 files.extend(self._get_files_for_range(dir_path, start_day, 31))  # Max days in a month
#         elif curr_date.year == end_date.year and curr_date.month == end_date.month:
#             files.extend(self._get_files_for_range(dir_path, 1, end_date.day))
#         else:
#             month_file_path = self._get_month_file_path(dir_path)
#             if glob.glob(month_file_path):
#                 files.append(month_file_path)
#         return files
#
#     def _get_files_for_range(self, dir_path, start_day, end_day):
#         files = []
#         for day in range(start_day, end_day + 1):
#             day_file_path = self._get_day_file_path(dir_path, day)
#             if glob.glob(day_file_path):
#                 files.append(day_file_path)
#         return files
#
#     @staticmethod
#     def _increment_month(curr_date):
#         if curr_date.month == 12:
#             return datetime.datetime(curr_date.year + 1, 1, 1)
#         else:
#             return datetime.datetime(curr_date.year, curr_date.month + 1, 1)
