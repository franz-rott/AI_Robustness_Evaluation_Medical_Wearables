# Nutrition Analysis and Image Processing Repository

This repository contains tools and scripts for processing images, analyzing nutrition data, generating metrics, and visualizing results. It integrates image preprocessing, API requests for nutrition analysis, and statistical evaluations.

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
  - [Preprocessing Images](#preprocessing-images)
  - [Running API Requests](#running-api-requests)
  - [Generating Nutrition Data](#generating-nutrition-data)
  - [Analyzing Metrics](#analyzing-metrics)
  - [Visualizing Results](#visualizing-results)
- [Scripts Overview](#scripts-overview)
- [Dependencies](#dependencies)
- [License](#license)

---

## Project Structure
```
.
├── data
│   ├── raw
│   │   ├── side_angle
│   │   └── overhead
│   └── results
│       ├── processed_results
│       ├── metrics_analysis.csv
│       ├── heatmaps_metrics
│       └── heatmaps_nutrients
├── demo
│   ├── 01_compress_images.py
│   ├── 02_preprocess_images.py
│   ├── 03_run_api_requests.py
│   └── 04_generate_nutrition_csv.py
├── scripts
│   ├── analyze_nutrition_metrics.py
│   ├── generate_metrics_analysis.py
│   ├── generate_nutrition_csv.py
│   ├── generate_nutrition_heatmaps.py
│   ├── inference_statistics.py
│   ├── run_api_requests.py
│   └── visualize_metrics.py
├── src
│   ├── data_preprocessing
│   │   ├── compress_images.py
│   │   ├── extract_first_frame.py
│   │   └── preprocess_images.py
│   └── utils
│       ├── api_connector.py
├── helper.py
└── README.md
```

---

## Features
1. **Image Preprocessing**
   - Compress images to a specified size.
   - Extract frames from video files.
   - Generate image variations with adjusted brightness, contrast, and saturation.

2. **API Integration**
   - Analyze images using the Foodvisor API.
   - Save API responses in JSON format.

3. **Nutrition Analysis**
   - Generate nutrition evaluation datasets.
   - Calculate metrics such as MAE, MAPE, and Proportion Below 20%.
   - Perform statistical tests on predictions.

4. **Visualization**
   - Generate heatmaps for metrics and nutrients.
   - Plot statistical differences between predictions and ground truth.

---

## Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the API key in `src/utils/api_connector.py`.

---

## Usage

### Preprocessing Images
Use the script `01_compress_images.py` to compress images or `02_preprocess_images.py` to generate image variations:
```bash
python demo/01_compress_images.py
python demo/02_preprocess_images.py
```

### Running API Requests
Analyze images using the Foodvisor API:
```bash
python demo/03_run_api_requests.py
```

### Generating Nutrition Data
Combine API results and metadata to generate a comprehensive dataset:
```bash
python demo/04_generate_nutrition_csv.py
```

### Analyzing Metrics
Compute metrics such as MAE, MAPE, and Prop<20%:
```bash
python scripts/generate_metrics_analysis.py
```

### Visualizing Results
Generate heatmaps for metrics and nutrients:
```bash
python scripts/generate_nutrition_heatmaps.py
```

---

## Scripts Overview

### `helper.py`
Utility script to aggregate content from Python files within a directory into a single text file.

### `demo`
Scripts for basic image compression, preprocessing, API requests, and generating nutrition CSVs.

### `scripts`
Contains analysis and visualization scripts:
- `analyze_nutrition_metrics.py`: Generates sub-tables for metrics and nutrients.
- `generate_metrics_analysis.py`: Computes metrics like MAE, MAPE, and Prop<20%.
- `generate_nutrition_heatmaps.py`: Creates heatmaps for metrics and nutrients.
- `inference_statistics.py`: Performs statistical tests on predictions.
- `visualize_metrics.py`: Visualizes metrics with heatmaps.

### `src`
Core functionality:
- `data_preprocessing`: Scripts for image compression, frame extraction, and image variations.
- `utils`: API connector for sending images and saving results.

---

## Dependencies

The repository relies on the following Python libraries:
- `numpy`
- `pandas`
- `opencv-python`
- `Pillow`
- `matplotlib`
- `seaborn`
- `requests`

Install them using:
```bash
pip install -r requirements.txt
```

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.