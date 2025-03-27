
import psutil
import time
from database import log_system_stats

def write_system_stats(cpu, memory, disk, network):
    with open("system_stats.txt", "w") as f:
        f.write(f"{cpu}, {memory}, {disk}, {network}")

def monitor_system():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_bytes_sent = psutil.net_io_counters().bytes_sent
        network_usage = round(network_bytes_sent / (1024 * 1024), 2)  

        print(f"CPU: {cpu_usage}% | Memory: {memory_usage}% | Disk: {disk_usage}% | Network: {network_usage} MB sent")

        write_system_stats(cpu_usage, memory_usage, disk_usage, network_usage)
        log_system_stats(cpu_usage, memory_usage, disk_usage, network_usage)
        
        time.sleep(2)


if __name__ == '__main__':
    monitor_system()