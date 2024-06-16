# Product Data Viewer

This is a Streamlit application to view and analyze product data. The app can either crawl product data from a provided link or upload product data from a CSV file, then display and visualize the data.

## Features

- Crawl product data from various sources.
- Upload product data via CSV file.
- Display product data in a table.
- Visualize product data with various charts.
- Download crawled data as a CSV file.

## Installation

To run this application, you need to have Python installed. You can install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

## Running the Application
You can run the application using the following command:
```bash
streamlit run streamlit_app.py
```

### Configuration
Streamlit configuration can be found in the .streamlit/config.toml file.

## Usage
### 1. Crawl Data from Link:
- Select "Crawl from Link" from the sidebar.
- Enter the link to crawl and select the type of crawler.
- Click "Crawl Data".
- The crawled data will be displayed in a table and visualized with various charts.
- You can download the crawled data as a CSV file.

### 2.Upload CSV File:
- Select "Upload CSV File" from the sidebar.
- Choose a CSV file to upload.
- The uploaded data will be displayed in a table and visualized with various charts.