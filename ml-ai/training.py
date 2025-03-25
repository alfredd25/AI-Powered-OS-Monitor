import numpy as np
import pandas as pd
from anomaly_detection import train_anomaly_detector, save_model


def load_historical_data(csv_file="system_logs_export.csv"):
    try:
        df = pd.read_csv(csv_file)
        data = df[["CPU Usage", "Memory Usage", "Disk Usage", "Network Usage"]].values
        return data
    except Exception as e:
        print("Error loading historical data:", e)
        return np.random.rand(200, 4)


def train_model_from_historical_data():
    data = load_historical_data()
    print("Training model on historical data...")
    model = train_anomaly_detector(data)
    save_model(model)
    print("Model training completed.")


if __name__ == '__main__':
    train_model_from_historical_data()
