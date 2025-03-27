import sqlite3

def create_database():
    conn = sqlite3.connect("../frontend-ui/system_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cpu_usage REAL,
            memory_usage REAL,
            disk_usage REAL,
            network_usage REAL
        )
    """)
    conn.commit()
    conn.close()
    print("Database and table created.")

def log_system_stats(cpu, memory, disk, network):
    conn = sqlite3.connect("../frontend-ui/system_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (cpu_usage, memory_usage, disk_usage, network_usage)
        VALUES (?, ?, ?, ?)
    """, (cpu, memory, disk, network))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()