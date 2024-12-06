# availai

**`availai`** is a Python library for managing and building computer vision workflows, including tools for dataset management, preprocessing, and seamless integration with [Weights & Biases (W&B)](https://wandb.ai/) and [Roboflow](https://roboflow.com/). Future updates will expand functionality to include broader machine learning, deep learning, audio processing, NLP, and large language models (LLMs).

## Features

### Dataset Management
- **Download Datasets**:
  - Fetch datasets directly from **Weights & Biases** using artifact versioning.
  - Retrieve datasets from **Roboflow** in various formats (e.g., YOLOv8).

- **Upload and Log**:
  - Upload datasets as W&B artifacts for versioning and tracking.
  - Log dataset-related tables for visualization in W&B projects.

- **Dataset Customization**:
  - Create smaller dataset versions for quick testing by reducing one or more dataset splits (e.g., `train`, `val`, `test`).

- **Copy Datasets**:
  - Copy datasets to a specified location with a progress bar for visibility.

### Integration with Roboflow
- Download datasets using workspace and project names.
- Support for multiple dataset formats, such as YOLOv8, COCO, and more.

### Integration with Weights & Biases
- Manage datasets using W&B artifact tracking.
- Log preprocessing steps and metadata as W&B artifacts for reproducibility.

---

## Installation

Install `availai` from PyPI:

```bash
pip install availai
