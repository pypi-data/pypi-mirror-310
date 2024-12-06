import os
import shutil
import random
import logging
from tqdm import tqdm
import wandb
import roboflow
from typing import Optional, Dict

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Dataset:
    def __init__(
        self, path: str, name: Optional[str] = None, project_name: Optional[str] = None
    ):
        """
        Initializes a Dataset object.

        Args:
            path (str): Root directory of the datasets.
            name (Optional[str]): Name of the datasets. Defaults to the directory name.
            project_name (Optional[str]): The W&B project name. Defaults to the datasets name.

        Raises:
            FileNotFoundError: If the specified datasets path cannot be created.
        """
        self.path = path
        self.name = name if name else os.path.basename(os.path.normpath(path))
        self.project_name = project_name if project_name else self.name

    def create_small_version(
        self,
        fraction: float,
        destination_path: Optional[str] = None,
        splits_to_reduce: Optional[list] = None,
    ):
        """
        Creates a smaller version of the dataset by randomly sampling files.

        Args:
            fraction (float): Fraction of the original dataset to include in the smaller version.
            splits_to_reduce (Optional[list]): List of dataset splits to reduce (e.g., ["train", "val"]).
                                            If not provided, only the "train" split will be reduced.
            destination_path (Optional[str]): Path to save the smaller dataset. If not specified,
                                            the smaller dataset will be created in the original path
                                            with a `-small` suffix.

        Raises:
            ValueError: If the fraction is not between 0 and 1.
            FileNotFoundError: If the dataset directory does not exist.
            Exception: For other file processing errors.
        """
        if not (0 < fraction <= 1):
            raise ValueError("The fraction must be a value between 0 and 1.")

        if not os.path.exists(self.path):
            raise FileNotFoundError(f"The dataset path '{self.path}' does not exist.")

        # Define default destination path
        if not destination_path:
            destination_path = f"{self.path}-small"
            logger.info(
                f"No destination path provided. Using default: '{destination_path}'"
            )

        os.makedirs(destination_path, exist_ok=True)
        logger.info(
            f"Creating a smaller dataset version at '{destination_path}' with fraction {fraction}."
        )

        splits = ["train", "val", "test"]
        splits_to_reduce = splits_to_reduce or ["train"]

        try:
            for split in splits:
                split_path = os.path.join(self.path, split)
                destination_split_path = os.path.join(destination_path, split)

                # Reduce only the specified splits
                if split not in splits_to_reduce:
                    if os.path.exists(split_path):
                        shutil.copytree(split_path, destination_split_path)
                    continue

                if not os.path.exists(split_path):
                    logger.warning(
                        f"Split '{split}' does not exist in the dataset path '{self.path}'. Skipping."
                    )
                    continue

                # Gather image files and their corresponding labels
                images = [
                    f
                    for f in os.listdir(os.path.join(split_path, "images"))
                    if f.endswith(".jpg")
                ]
                labels = [
                    f
                    for f in os.listdir(os.path.join(split_path, "labels"))
                    if f.endswith(".txt")
                ]

                # Ensure label file exists for each image
                image_label_pairs = [
                    (img, img.replace(".jpg", ".txt"))
                    for img in images
                    if img.replace(".jpg", ".txt") in labels
                ]

                # Randomly sample a subset
                subset = random.sample(
                    image_label_pairs, int(fraction * len(image_label_pairs))
                )

                # Copy the subset to the destination
                os.makedirs(
                    os.path.join(destination_split_path, "images"), exist_ok=True
                )
                os.makedirs(
                    os.path.join(destination_split_path, "labels"), exist_ok=True
                )

                with tqdm(
                    total=len(subset), desc=f"Creating {split} subset", unit="file"
                ) as pbar:
                    for image, label in subset:
                        src_image = os.path.join(split_path, "images", image)
                        dest_image = os.path.join(
                            destination_split_path, "images", image
                        )
                        shutil.copy2(src_image, dest_image)

                        src_label = os.path.join(split_path, "labels", label)
                        dest_label = os.path.join(
                            destination_split_path, "labels", label
                        )
                        shutil.copy2(src_label, dest_label)

                        pbar.update(1)

            logger.info(
                f"Smaller dataset version created successfully at '{destination_path}'."
            )
        except Exception as e:
            logger.error(f"Error creating smaller dataset version: {e}")
            raise

    def download_from_wandb(self, api_key: str, version: str = "latest"):
        """
        Downloads a datasets from Weights & Biases.

        Args:
            api_key (str): The W&B API key, either as a string or a path to a file containing the key.
            version (str): The version of the artifact to download. Defaults to "latest".

        Raises:
            ValueError: If the API key is not provided or invalid.
            wandb.CommError: If there is a network issue or authentication failure.
        """
        api_key = self._get_api_key(api_key)
        if not api_key:
            raise ValueError("API key required for W&B.")
        self._authenticate_wandb(api_key)

        try:
            with wandb.init(project=self.project_name, job_type="download_data") as run:
                artifact = run.use_artifact(f"{self.name}:{version}", type="datasets")
                artifact_dir = artifact.download(root=self.path)
                logger.info(
                    f"Downloaded W&B datasets '{self.name}' (version: {version}) to '{artifact_dir}'."
                )
        except wandb.errors.CommError as e:
            logger.error(
                f"Failed to download W&B artifact '{self.name}:{version}': {e}"
            )

    def download_from_roboflow(
        self,
        model_format: str,
        api_key: str,
        workspace: str,
        project_name: Optional[str] = None,
    ):
        """
        Downloads a datasets from Roboflow.

        Args:
            model_format (str): The format of the datasets, e.g., 'yolov8'.
            api_key (str): The Roboflow API key, either as a string or a path to a file containing the key.
            workspace (str): The workspace in Roboflow.
            project_name (Optional[str]): The specific Roboflow project name. Defaults to the initialized project name.

        Raises:
            ValueError: If the API key, workspace, or project name is not provided.
            roboflow.exceptions.RoboflowException: If there is an issue with the Roboflow API or download process.
        """
        api_key = self._get_api_key(api_key)
        if not api_key:
            raise ValueError("API key required for Roboflow.")
        if not workspace:
            raise ValueError("Workspace required for Roboflow download.")

        project_name = project_name or self.project_name

        try:
            rf = roboflow.Roboflow(api_key=api_key)
            project = rf.workspace(workspace).project(project_name)
            dataset = project.version(1).download(model_format, location=self.path)
            logger.info(
                f"Downloaded Roboflow datasets '{self.name}' (project: {project_name}) in format '{model_format}' to '{self.path}'."
            )
        except Exception as e:
            logger.error(
                f"Failed to download Roboflow datasets '{project_name}' in workspace '{workspace}': {e}"
            )

    def copy_to(self, destination_path: str):
        """
        Copies the dataset directory to the specified destination with a progress bar.

        Args:
            destination_path (str): The path to copy the dataset to.

        Raises:
            FileNotFoundError: If the source dataset directory does not exist.
            OSError: If there's an error during the copy operation.
        """
        if not os.path.exists(self.path):
            raise FileNotFoundError(
                f"The source dataset path '{self.path}' does not exist."
            )

        os.makedirs(destination_path, exist_ok=True)
        logger.info(f"Copying dataset from '{self.path}' to '{destination_path}'.")

        try:
            files = []
            for root, _, filenames in os.walk(self.path):
                for filename in filenames:
                    files.append(os.path.join(root, filename))

            with tqdm(total=len(files), desc="Copying dataset", unit="file") as pbar:
                for src in files:
                    relative_path = os.path.relpath(src, self.path)
                    dest = os.path.join(destination_path, relative_path)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copy2(src, dest)
                    pbar.update(1)

            logger.info(f"Dataset copied successfully to '{destination_path}'.")
        except Exception as e:
            logger.error(f"Error copying dataset to '{destination_path}': {e}")
            raise

    def upload_to_wandb(self, metadata: Optional[Dict] = None):
        """
        Uploads the datasets directory as an artifact to Weights & Biases.

        Args:
            metadata (Optional[Dict]): Metadata to attach to the artifact.

        Raises:
            wandb.errors.CommError: If there is a network issue or authentication failure.
            Exception: For other upload-related issues.
        """
        try:
            with wandb.init(project=self.project_name, job_type="upload_data") as run:
                artifact = wandb.Artifact(
                    name=self.name, type="datasets", metadata=metadata or {}
                )
                artifact.add_dir(self.path)
                run.log_artifact(artifact)
                logger.info(f"Artifact '{self.name}' uploaded to W&B successfully.")
        except wandb.errors.CommError as e:
            logger.error(f"Failed to upload artifact '{self.name}' to W&B: {e}")
        except Exception as e:
            logger.error(f"Error uploading artifact '{self.name}': {e}")

    def log_table_on_wandb(self):
        """Logs a sample table to W&B."""
        try:
            with wandb.init(project=self.project_name, job_type="create_table"):
                table = wandb.Table(
                    columns=["a", "b"], data=[["a1", "b1"], ["a2", "b2"]]
                )
                wandb.log({"Football player datasets": table})
        except Exception as e:
            logger.error(f"Error creating table: {e}")

    def preprocess(self, target: str, steps: Dict, metadata: Optional[Dict] = None):
        """Preprocesses the datasets and logs the new artifact."""
        try:
            logger.info(
                f"Preprocessing datasets with target '{target}' and steps: {steps}"
            )
            metadata = metadata or {}
            metadata["preprocessing_steps"] = steps
            self.upload_to_wandb(metadata=metadata)
        except Exception as e:
            logger.error(f"Error during preprocessing: {e}")

    def _authenticate_wandb(self, api_key: str):
        """Authenticates with Weights & Biases using the provided API key."""
        wandb.login(key=api_key)

    @staticmethod
    def _get_api_key(api_key: str) -> str:
        """Checks if api_key is a file path; if so, reads the key from the file."""
        if os.path.isfile(api_key):
            with open(api_key, "r") as file:
                return file.read().strip()
        return api_key
