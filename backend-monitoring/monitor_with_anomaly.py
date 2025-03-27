import psutil
import time
import threading
import queue
import sqlite3
import joblib  
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'ml-ai', 'isolation_forest_model.pkl')
DB_PATH = os.path.join(BASE_DIR, '..', 'frontend-ui', 'system_logs.db')
STATS_FILE = os.path.join(BASE_DIR, '..', 'frontend-ui', 'system_stats.txt')

anomaly_model = joblib.load(MODEL_PATH)

log_queue = queue.Queue()

def write_system_stats_to_file(cpu, memory, disk, network, anomaly):
    
    with open(STATS_FILE, "w") as f:
        f.write(f"{cpu}, {memory}, {disk}, {network}, {anomaly}")

def database_worker(db_path, log_queue):
    
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    while True:
        try:
            log_entry = log_queue.get(timeout=5)
            if log_entry is None:
                break
            cpu, memory, disk, network, anomaly = log_entry
            cursor.execute("""
                INSERT INTO logs (cpu_usage, memory_usage, disk_usage, network_usage, is_anomaly)
                VALUES (?, ?, ?, ?, ?)
            """, (cpu, memory, disk, network, anomaly))
            conn.commit()
            log_queue.task_done()
        except queue.Empty:
            continue
    conn.close()

def monitor_system():
    
    worker_thread = threading.Thread(target=database_worker, args=(DB_PATH, log_queue))
    worker_thread.daemon = True
    worker_thread.start()

    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_bytes_sent = psutil.net_io_counters().bytes_sent
        network_usage = round(network_bytes_sent / (1024 * 1024), 2)

        features = [[cpu_usage, memory_usage, disk_usage, network_usage]]
        prediction = anomaly_model.predict(features)
        anomaly_flag = 1 if prediction[0] == -1 else 0

        print(f"CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk: {disk_usage}%, "
              f"Network: {network_usage} MB, Anomaly: {anomaly_flag}")

        write_system_stats_to_file(cpu_usage, memory_usage, disk_usage, network_usage, anomaly_flag)
        log_queue.put((cpu_usage, memory_usage, disk_usage, network_usage, anomaly_flag))

        time.sleep(2)

if __name__ == '__main__':
    monitor_system()