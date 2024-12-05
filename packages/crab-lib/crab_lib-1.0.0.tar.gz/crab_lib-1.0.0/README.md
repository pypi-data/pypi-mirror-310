# Crab-Lib

**Crab-Lib** is a Python library designed to simplify the processing, analysis, and visualization of GPS data, particularly for fishing grounds in the Gulf of Mexico. It includes tools for cleaning data, calculating distances, detecting clusters, and generating insightful visualizations. Whether you're a fisheries scientist, data analyst, or GIS enthusiast, **Crab-Lib** helps you make sense of complex geospatial datasets.

---

## Features

- **Data I/O**:
  - Load and save GPS data in CSV format.
  - Validate and handle missing or malformed data.
- **Data Preprocessing**:
  - Remove duplicates and invalid rows.
  - Filter data based on keywords in comments.
  - Standardize comment text for consistency.
- **Geospatial Analysis**:
  - Calculate great-circle distances using the Haversine formula.
  - Identify clusters of GPS points based on proximity.
  - Summarize datasets with averages and bounding boxes.
- **Visualization**:
  - Plot points, clusters, and density heatmaps.
  - Create interactive and informative visualizations.
- **Utilities**:
  - Convert coordinates from DMS to decimal degrees.
  - Calculate initial bearings between two GPS points.
  - Validate if a point lies within a bounding box.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Detailed Examples](#detailed-examples)
   - [Data I/O](#data-io)
   - [Preprocessing](#preprocessing)
   - [Analysis](#analysis)
   - [Visualization](#visualization)
   - [Utilities](#utilities)
4. [API Reference](#api-reference)
5. [Troubleshooting](#troubleshooting)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

---

## Installation

### Install via Source
1. Clone the repository:
   ```bash
   git clone https://github.com/RedGloveProductions/crab-lib.git
   cd crab-lib
Install the library:
pip install -e .
Dependencies
Crab-Lib requires the following Python packages:
matplotlib >= 3.0.0
For development, additional tools like pytest and black are recommended.
Quick Start

Here's a quick guide to get started with Crab-Lib:
Load Data:
from crab_lib.io import load_csv
data = load_csv("fishing_data.csv")
Clean Data:
from crab_lib.preprocessing import clean_data
cleaned_data = clean_data(data)
Analyze Data:
from crab_lib.analysis import calculate_distances, find_clusters
distances = calculate_distances(cleaned_data)
clusters = find_clusters(cleaned_data, radius=100)
Visualize Data:
from crab_lib.visualization import plot_points
plot_points(cleaned_data)
Detailed Examples

Data I/O
Load and Save Data:
from crab_lib.io import load_csv, save_csv

# Load data from a CSV file
data = load_csv("fishing_data.csv")

# Save cleaned data to a new file
save_csv("cleaned_data.csv", data)
Preprocessing
Clean, Filter, and Standardize Data:
from crab_lib.preprocessing import clean_data, filter_data, standardize_comments

# Remove duplicates and invalid rows
cleaned_data = clean_data(data)

# Filter rows containing the keyword 'hotspot'
filtered_data = filter_data(cleaned_data, "hotspot")

# Standardize comments for consistency
standardized_data = standardize_comments(filtered_data)
Analysis
Calculate Distances and Find Clusters:
from crab_lib.analysis import calculate_distances, find_clusters, summarize_data

# Calculate pairwise distances
distances = calculate_distances(cleaned_data)

# Identify clusters within a 50 km radius
clusters = find_clusters(cleaned_data, radius=50)

# Summarize the dataset
summary = summarize_data(cleaned_data)
print(summary)
Visualization
Visualize Data:
from crab_lib.visualization import plot_points, plot_clusters, create_heatmap

# Plot individual points
plot_points(cleaned_data)

# Plot clusters
plot_clusters(clusters)

# Create a heatmap of point density
create_heatmap(cleaned_data)
Utilities
Convert Coordinates and Calculate Bearings:
from crab_lib.utils import convert_coordinates, calculate_bearing, is_within_bounds

# Convert DMS to decimal degrees
decimal_coord = convert_coordinates("25°46'26.5\"N")

# Calculate bearing between two points
bearing = calculate_bearing((25.774, -80.19), (27.345, -82.567))
print("Bearing:", bearing)

# Check if a point is within bounds
bounds = (25.0, 26.0, -81.0, -79.0)
print("Is within bounds:", is_within_bounds((25.774, -80.19), bounds))
API Reference

I/O Module
load_csv(file_path: str) -> List[Dict[str, str]]: Load GPS data from a CSV file.
save_csv(file_path: str, data: List[Dict[str, str]]) -> None: Save data to a CSV file.
Preprocessing Module
clean_data(data: List[Dict[str, str]]) -> List[Dict[str, str]]: Remove duplicates and invalid rows.
filter_data(data: List[Dict[str, str]], keyword: str) -> List[Dict[str, str]]: Filter rows by keyword.
standardize_comments(data: List[Dict[str, str]]) -> List[Dict[str, str]]: Standardize comment text.
Analysis Module
calculate_distances(data: List[Dict[str, float]]) -> List[Dict[str, float]]: Compute pairwise distances.
find_clusters(data: List[Dict[str, float]], radius: float) -> List[List[Dict[str, float]]]: Detect clusters.
summarize_data(data: List[Dict[str, float]]) -> Dict[str, float]: Summarize dataset metrics.
Visualization Module
plot_points(data: List[Dict[str, float]]) -> None: Scatter plot of GPS points.
plot_clusters(clusters: List[List[Dict[str, float]]]) -> None: Visualize clusters.
create_heatmap(data: List[Dict[str, float]], bins: int) -> None: Generate a heatmap.
Utils Module
convert_coordinates(dms: str) -> float: Convert DMS to decimal degrees.
calculate_bearing(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float: Compute initial bearing.
is_within_bounds(coord: Tuple[float, float], bounds: Tuple[float, float, float, float]) -> bool: Check if a point is in bounds.
Troubleshooting

Issue: FileNotFoundError when loading a CSV.
Solution: Verify the file path and ensure the file exists.
Issue: ValueError when cleaning or processing data.
Solution: Ensure your data matches the required format (x, y, comment).
Contributing

Contributions are welcome! To contribute:
Fork the repository.
Create a feature branch.
Submit a pull request with a clear description of changes.
License

This project is licensed under the MIT License.
Contact

Author: Your Name
Email: your_email@example.com
GitHub: RedGloveProductions
Project Links

GitHub Repository
Issue Tracker

---

This `README.md` includes the additional details and provides a comprehensive introduction to your library.
