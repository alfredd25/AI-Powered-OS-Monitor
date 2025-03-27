import sqlite3
import os

def create_database():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, '..', 'frontend-ui', 'system_logs.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cpu_usage REAL,
            memory_usage REAL,
            disk_usage REAL,
            network_usage REAL,
            is_anomaly INTEGER
        )
    """)
    conn.commit()
    conn.close()
    print("Database and table created with anomaly column.")

def log_system_stats(cpu, memory, disk, network, anomaly):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, '..', 'frontend-ui', 'system_logs.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (cpu_usage, memory_usage, disk_usage, network_usage, is_anomaly)
        VALUES (?, ?, ?, ?, ?)
    """, (cpu, memory, disk, network, anomaly))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()