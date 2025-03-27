
import sqlite3
import csv

def retrieve_historical_data(limit=None):
    
    conn = sqlite3.connect("../frontend-ui/system_logs.db")
    cursor = conn.cursor()
    query = "SELECT timestamp, cpu_usage, memory_usage, disk_usage, network_usage FROM logs ORDER BY timestamp DESC"
    if limit:
        query += " LIMIT ?"
        cursor.execute(query, (limit,))
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def export_data_to_csv(filename="system_logs_export.csv"):
    
    data = retrieve_historical_data()
    headers = ["Timestamp", "CPU Usage", "Memory Usage", "Disk Usage", "Network Usage"]
    
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"Data successfully exported to {filename}")

if __name__ == '__main__':
    
    recent_data = retrieve_historical_data(limit=5)
    print("Recent Records:")
    for record in recent_data:
        print(record)
    
    export_data_to_csv()