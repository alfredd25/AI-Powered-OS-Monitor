import numpy as np
from sklearn.ensemble import IsolationForest
import joblib


def train_anomaly_detector(data, contamination=0.1, random_state=42):
    model = IsolationForest(contamination=contamination, random_state=random_state)
    model.fit(data)
    return model


def save_model(model, filename="isolation_forest_model.pkl"):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")


def load_model(filename="isolation_forest_model.pkl"):
    return joblib.load(filename)


def detect_anomalies(model, data):
    predictions = model.predict(data)
    return predictions


if __name__ == '__main__':
    data = np.random.rand(100, 2)
    model = train_anomaly_detector(data)
    save_model(model)
    loaded_model = load_model()
    anomalies = detect_anomalies(loaded_model, data)
    print("Anomaly predictions:", anomalies)
