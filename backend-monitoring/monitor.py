
import psutil
import time
import threading
import queue
import sqlite3


def write_system_stats(cpu, memory, disk, network):

    log_queue = queue.Queue()

def write_system_stats_to_file(cpu, memory, disk, network):

    with open("system_stats.txt", "w") as f:
        f.write(f"{cpu}, {memory}, {disk}, {network}")

def database_worker(db_path, log_queue):
    
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    while True:
        try:
            log_entry = log_queue.get(timeout=5)
            if log_entry is None: 
                break
            cpu, memory, disk, network = log_entry
            cursor.execute("""
                INSERT INTO logs (cpu_usage, memory_usage, disk_usage, network_usage)
                VALUES (?, ?, ?, ?)
            """, (cpu, memory, disk, network))
            conn.commit()
            log_queue.task_done()
        except queue.Empty:
            continue  
    conn.close()

def monitor_system():
    
    db_path = "system_logs.db"
    worker_thread = threading.Thread(target=database_worker, args=(db_path, log_queue))
    worker_thread.daemon = True
    worker_thread.start()

    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_bytes_sent = psutil.net_io_counters().bytes_sent
        network_usage = round(network_bytes_sent / (1024 * 1024), 2)

        print(f"CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk: {disk_usage}%, Network: {network_usage} MB")

        write_system_stats_to_file(cpu_usage, memory_usage, disk_usage, network_usage)

        log_queue.put((cpu_usage, memory_usage, disk_usage, network_usage))

        time.sleep(2)


if __name__ == '__main__':
    monitor_system()