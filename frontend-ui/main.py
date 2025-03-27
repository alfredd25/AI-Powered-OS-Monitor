import sys
import os
import time
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DataFetcher(QThread):
    newData = pyqtSignal(float, float, float, float, int)

    def run(self):
        while True:
            cpu, memory, disk, network, anomaly = self.read_stats()
            self.newData.emit(cpu, memory, disk, network, anomaly)
            time.sleep(2)

    def read_stats(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_stats.txt")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    content = file.read().strip()
                    if content:
                        parts = content.split(",")
                        if len(parts) >= 5:
                            return (
                                float(parts[0].strip()),
                                float(parts[1].strip()),
                                float(parts[2].strip()),
                                float(parts[3].strip()),
                                int(parts[4].strip())
                            )
            except Exception as e:
                print("Error reading system stats:", e)
        return 0.0, 0.0, 0.0, 0.0, 0

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        self.ax.set_title("CPU Usage Over Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("CPU Usage (%)")
        self.ax.set_ylim(0, 100)
        self.line, = self.ax.plot([], [], lw=2)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 AI-Powered OS Monitor")
        self.setGeometry(200, 200, 600, 500)

        main_layout = QVBoxLayout()
        stats_layout = QHBoxLayout()

        self.cpu_label = QLabel()
        self.cpu_label.setAlignment(Qt.AlignCenter)
        self.cpu_label.setStyleSheet("font-size: 18px;")

        self.memory_label = QLabel()
        self.memory_label.setAlignment(Qt.AlignCenter)
        self.memory_label.setStyleSheet("font-size: 18px;")

        self.disk_label = QLabel()
        self.disk_label.setAlignment(Qt.AlignCenter)
        self.disk_label.setStyleSheet("font-size: 18px;")

        self.network_label = QLabel()
        self.network_label.setAlignment(Qt.AlignCenter)
        self.network_label.setStyleSheet("font-size: 18px;")

        self.anomaly_label = QLabel()
        self.anomaly_label.setAlignment(Qt.AlignCenter)
        self.anomaly_label.setStyleSheet("font-size: 18px; color: red;")

        stats_layout.addWidget(self.cpu_label)
        stats_layout.addWidget(self.memory_label)
        stats_layout.addWidget(self.disk_label)
        stats_layout.addWidget(self.network_label)
        stats_layout.addWidget(self.anomaly_label)

        self.canvas = MplCanvas(self, width=5, height=3, dpi=100)
        self.cpu_data = []
        self.time_counter = []
        self.counter = 0

        main_layout.addLayout(stats_layout)
        main_layout.addWidget(self.canvas)
        self.setLayout(main_layout)

        self.data_fetcher = DataFetcher()
        self.data_fetcher.newData.connect(self.update_stats)
        self.data_fetcher.start()

    def update_stats(self, cpu, memory, disk, network, anomaly):
        self.cpu_label.setText(f"<span style='color:{self.get_color(cpu)}'>CPU: {cpu:.1f}%</span>")
        self.memory_label.setText(f"<span style='color:{self.get_color(memory)}'>Memory: {memory:.1f}%</span>")
        self.disk_label.setText(f"<span style='color:{self.get_color(disk)}'>Disk: {disk:.1f}%</span>")
        self.network_label.setText(f"<span style='color:{self.get_color(network)}'>Network: {network:.1f}%</span>")
        anomaly_text = "Anomaly Detected!" if anomaly == 1 else "Normal"
        self.anomaly_label.setText(anomaly_text)

        self.cpu_data.append(cpu)
        self.counter += 2
        self.time_counter.append(self.counter)

        if len(self.cpu_data) > 20:
            self.cpu_data = self.cpu_data[-20:]
            self.time_counter = self.time_counter[-20:]

        if self.time_counter and self.cpu_data:
            self.canvas.line.set_data(self.time_counter, self.cpu_data)

            xmin, xmax = min(self.time_counter), max(self.time_counter)
            x_padding = (xmax - xmin) * 0.05 if xmax != xmin else 1
            self.canvas.ax.set_xlim(xmin - x_padding, xmax + x_padding)

            ymin, ymax = min(self.cpu_data), max(self.cpu_data)
            y_padding = (ymax - ymin) * 0.1 if ymax != ymin else 10
            self.canvas.ax.set_ylim(ymin - y_padding, ymax + y_padding)

            self.canvas.draw()

    def get_color(self, value):
        if value < 50:
            return "green"
        elif value < 80:
            return "orange"
        else:
            return "red"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
