import os
import shutil
import urllib.request as request
import zipfile
from textSummarizer.logging import logger
from textSummarizer.utils.common import get_size
from pathlib import Path
from textSummarizer.entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        logger.info(f"Files extracted to {unzip_path}")
        self.organize_dataset_folders()

    def organize_dataset_folders(self):
        """
        Organizes the extracted data into train, test, and val folders inside artifacts/data_ingestion/email_data.
        """
        # Define the target directory
        target_base_dir = Path("artifacts/data_ingestion/email_data")
        target_base_dir.mkdir(parents=True, exist_ok=True)

        dataset_folders = ["train", "test", "val"]
        for folder in dataset_folders:
            (target_base_dir / folder).mkdir(parents=True, exist_ok=True)

        # Move files into respective folders
        unzip_path = self.config.unzip_dir
        for root, dirs, files in os.walk(unzip_path):
            for file in files:
                if "train" in file.lower():
                    shutil.move(os.path.join(root, file), target_base_dir / "train" / file)
                elif "test" in file.lower():
                    shutil.move(os.path.join(root, file), target_base_dir / "test" / file)
                elif "val" in file.lower() or "valid" in file.lower():
                    shutil.move(os.path.join(root, file), target_base_dir / "val" / file)

        logger.info(f"Dataset organized into {target_base_dir}/train, {target_base_dir}/test, and {target_base_dir}/val folders.")
