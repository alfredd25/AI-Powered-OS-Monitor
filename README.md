# AI-Powered OS Monitor

An AI-powered system monitoring tool that collects real-time system metrics, logs them into a database, and uses machine learning for anomaly detection. The project includes a backend for monitoring, a PyQt5-based UI for visualization, and an ML module for training and detecting anomalies.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

The AI-Powered OS Monitor continuously tracks system metrics (CPU, memory, disk, and network usage) and logs them into a SQLite database. An anomaly detection model based on Isolation Forest identifies unusual patterns. The results are displayed in a real-time PyQt5 UI, which includes a dynamic graph and alert labels.

## Project Structure

AI-Powered-OS-Monitor/ ├── backend-monitoring/ │ ├── monitor.py # Basic system monitoring script │ ├── monitor_with_anomaly.py # Monitoring script with integrated anomaly detection │ ├── database.py # Database setup and logging functions │ └── data_handler.py # Additional data processing functions (if needed) ├── frontend-ui/ │ ├── main.py # PyQt5 UI for real-time display of system metrics │ ├── system_stats.txt # Temporary file updated with system stats │ └── system_logs.db # SQLite database for logging system metrics └── ml-ai/ ├── anomaly_detection.py # Training and prediction functions for anomaly detection └── isolation_forest_model.pkl # Trained model file (generated via anomaly_detection.py)


## Requirements

- **Python 3.6+**
- **PyQt5** – for the graphical UI.
- **matplotlib** – for plotting the CPU usage graph.
- **psutil** – for accessing system metrics.
- **scikit-learn** – for the Isolation Forest model.
- **joblib** – for model serialization.
- pip install -r requirements.txt


## Setup Instructions
Clone the Repository:


git clone https://github.com/yourusername/AI-Powered-OS-Monitor.git
cd AI-Powered-OS-Monitor
Create and Activate a Virtual Environment (Recommended):

python -m venv venv
### On Linux/Mac
source venv/bin/activate
### On Windows
venv\Scripts\activate
Install Dependencies:


pip install -r requirements.txt
Database Setup: Run the following command to create or update the database with the necessary tables:


python backend-monitoring/database.py
Generate the Anomaly Detection Model: Navigate to the ml-ai folder and run the training script:


cd ml-ai
python anomaly_detection.py
This will train an Isolation Forest model (using synthetic or historical data) and save it as isolation_forest_model.pkl.

## Usage
Starting the Monitoring Pipeline
Start the Monitoring Script with Anomaly Detection: Open a terminal and run:

python backend-monitoring/monitor_with_anomaly.py
This script collects system metrics, applies anomaly detection, writes stats to system_stats.txt, and logs data to system_logs.db.

Launch the GUI: Open a second terminal and run:


python frontend-ui/main.py
The PyQt5 interface will open, displaying:

Real-time system metrics with color-coded labels.

A dynamic graph plotting CPU usage over time.

An alert label that indicates if an anomaly is detected.

## Testing
Manual Testing
Database Verification:
Confirm that system_logs.db is updated with records containing system metrics and an anomaly flag.

File Check:
Inspect system_stats.txt to ensure it contains five comma-separated values (CPU, Memory, Disk, Network, and Anomaly flag).

UI Testing:
Run the UI (main.py) and verify that labels update and the graph reflects CPU usage. Manually edit system_stats.txt to simulate an anomaly (e.g., set the anomaly flag to 1) and observe the UI changes.

Automated Testing
Consider adding tests in a tests/ directory and using a framework like pytest:

pytest tests/
Contributing
Contributions are welcome! Please fork the repository and submit pull requests. Ensure your code follows the project structure and is well-documented. For major changes, open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Inspired by the need for robust, real-time system monitoring.

Utilizes the Isolation Forest algorithm for effective anomaly detection.

Thanks to the contributors and open-source libraries that make this project possible.


Feel free to adjust the repository URL, contribution guidelines, or any additional details as n