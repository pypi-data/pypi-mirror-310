import shutil
from pathlib import Path
from typing import Optional

import fsspec

class FileUtils:
    @staticmethod
    def ensure_directory_exists(directory_path, clear_existing=False):
        fs, path = fsspec.core.url_to_fs(directory_path)

        if fs.exists(path):
            if clear_existing:
                # For local file systems, clear the directory contents
                if fs.protocol == 'file':
                    shutil.rmtree(path)
                    fs.mkdirs(path)
                else:
                    # For non-local filesystems, clear each file in the directory
                    for file in fs.ls(path):
                        fs.rm(file, recursive=True)
        else:
            fs.mkdirs(path)

    @staticmethod
    def construct_full_path(storage_path:str, parquet_filename: Optional[str]) -> Path:
        """Construct and return the full path for the parquet file."""
        fs, base_path = fsspec.core.url_to_fs(storage_path)
        parquet_filename = parquet_filename or "default.parquet"
        return Path(base_path) / parquet_filename
