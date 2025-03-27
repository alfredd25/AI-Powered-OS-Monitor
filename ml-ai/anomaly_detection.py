import numpy as np
from sklearn.ensemble import IsolationForest
import joblib


def train_anomaly_detector(data, contamination=0.1, random_state=42):
    """
    Train an IsolationForest model on the provided data.
    :param data: Array-like, training data (should have 4 features for our system metrics)
    :param contamination: The proportion of outliers in the data.
    :param random_state: Seed for reproducibility.
    :return: Trained IsolationForest model.
    """
    model = IsolationForest(contamination=contamination, random_state=random_state)
    model.fit(data)
    return model


def save_model(model, filename="isolation_forest_model.pkl"):
    """
    Save the trained model to a pickle file.
    :param model: Trained model.
    :param filename: File name for saving the model.
    """
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")


def load_model(filename="isolation_forest_model.pkl"):
    """
    Load a model from a pickle file.
    :param filename: File name from which to load the model.
    :return: Loaded model.
    """
    return joblib.load(filename)


def detect_anomalies(model, data):
    """
    Detect anomalies in the provided data using the trained model.
    :param model: Trained IsolationForest model.
    :param data: Array-like data for prediction.
    :return: Predictions (-1 for anomaly, 1 for normal).
    """
    predictions = model.predict(data)
    return predictions


if __name__ == '__main__':
    # Generate sample data with 4 features (e.g., CPU, Memory, Disk, Network)
    data = np.random.rand(100, 4)
    model = train_anomaly_detector(data)
    save_model(model)
    loaded_model = load_model()
    anomalies = detect_anomalies(loaded_model, data)
    print("Anomaly predictions:", anomalies)
