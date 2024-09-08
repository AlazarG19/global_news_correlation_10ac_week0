# Global Media News Analysis

## Overview
![Intro](/front.avif "Intro Photo")

This project aims to analyze news articles from various sources to understand the global media landscape. The analysis focuses on sentiment, topics, and entities mentioned in the articles.

## Objective
The objective of the project is to analyze and understand how sentiment and topics are correlated across different global media agencies and check for biases that may influence the reports. By accomplishing this objective, the outcome is to develop models that classify headlines into specific categories, perform sentiment and topic analysis, and generate insights about reporting trends across media outlets.

## Main Focus
The main focus of this project is to conduct comprehensive exploratory data analysis and advanced analysis of global news data. The key objectives include:

- Quantitative Analysis
- Keyword and Topic Analysis
- Event Modeling
- Visualization and Interpretation
- Model Building and Versioning
- Dashboard Design and Deployment

## Deliverables
The main deliverables for this project include:

- **Reports**: Detailed analysis reports on sentiment, topic distribution, and reporting patterns.
- **Machine Learning Models**: Models for headline classification, sentiment analysis, and topic modeling.
- **Dashboards**: A Streamlit-based dashboard or a web application using React as a frontend and Flask as a backend.

## Tools and Techniques
The various tools used in the project include:

- Python
- Git
- GitHub
- PostgreSQL
- Streamlit or React and Flask
- Docker
- AWS

## Table of Contents

- [Installation](#installation)
  - [Clone this Package](#clone-this-package)
- [Data Loading](#data-loading)
- [Utilities](#utilities)
- [Testing](#testing)
- [Documentation](#documentation)
- [Notebooks](#notebooks)
- [Additional Insights](#additional-insights)

## Installation

### Clone this Package

To install the `global_media_news_analysis` package, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/AlazarG19/global_news_correlation_10ac_week0
    ```
2. Navigate to the project directory:
    ```bash
    cd global_media_news_analysis
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Data Loading

The package provides a data loader module (`loader.py`) in the `src` directory. Use this module to load your network data into a format suitable for analysis.

**Example:**

```python
from src.loader import DataLoader

path = {
    "rating":"path to rating"}

# initiating the newsdataloader class
data_loader = NewsDataLoader(path)

# Load data from a Slack channel
rating = data_loader.get_data("rating")

## Utilities  
Explore the various utilities available in the `src/utils.py` module. This module contains functions for common tasks such as data cleaning, preprocessing, and analysis.


## Notebooks
The notebooks directory contains Jupyter notebooks that demonstrate specific use cases and analyses.

EDA: Exploratory Data Analysis notebooks
Model: Model building and evaluation notebooks

## Additional Insights
For insights into each file and folder, refer to the documentation and examples provided within each directory. The README files in the notebooks/eda and notebooks/model folders provide details on the specific analyses and models.