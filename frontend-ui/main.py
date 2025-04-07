import sys
import os
import time
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QGridLayout, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Apply a clean style
plt.style.use('ggplot')


class DataFetcher(QThread):
    newData = pyqtSignal(float, float, float, float, int)

    def run(self):
        while True:
            stats = self.read_stats()
            self.newData.emit(*stats)
            time.sleep(2)

    def read_stats(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_stats.txt")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    parts = file.read().strip().split(",")
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
    def __init__(self, title, ylabel, color, ylim=(0, 100), dynamic_ylim=False):
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

        self.ax.set_title(title)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel(ylabel)
        if not dynamic_ylim:
            self.ax.set_ylim(*ylim)
        self.ax.grid(True)

        self.line, = self.ax.plot([], [], lw=2, color=color, label=title)
        self.scatter = self.ax.scatter([], [], color='red', marker='x', label='Anomaly')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 AI-Powered OS Monitor")
        self.setGeometry(100, 100, 900, 720)

        # Layouts
        self.labels_layout = QHBoxLayout()
        self.chart_layout = QGridLayout()
        self.main_layout = QVBoxLayout()

        # Labels
        self.cpu_label = self._create_label()
        self.memory_label = self._create_label()
        self.disk_label = self._create_label()
        self.network_label = self._create_label()
        self.anomaly_label = QLabel("Normal")
        self.anomaly_label.setAlignment(Qt.AlignCenter)
        self.anomaly_label.setStyleSheet("font-size: 16px; color: red;")

        for lbl in [self.cpu_label, self.memory_label, self.disk_label, self.network_label, self.anomaly_label]:
            self.labels_layout.addWidget(lbl)

        # Charts
        self.cpu_canvas = MplCanvas("CPU Usage", "CPU (%)", "blue")
        self.memory_canvas = MplCanvas("Memory Usage", "Memory (%)", "green")
        self.disk_canvas = MplCanvas("Disk Usage", "Disk (%)", "orange")
        self.network_canvas = MplCanvas("Network Usage", "Network (MB)", "purple", ylim=(0, 50), dynamic_ylim=True)

        self.chart_layout.addWidget(self.cpu_canvas, 0, 0)
        self.chart_layout.addWidget(self.memory_canvas, 0, 1)
        self.chart_layout.addWidget(self.disk_canvas, 1, 0)
        self.chart_layout.addWidget(self.network_canvas, 1, 1)

        # Final layout
        self.main_layout.addLayout(self.labels_layout)
        self.main_layout.addLayout(self.chart_layout)
        self.setLayout(self.main_layout)

        # Data buffers
        self.max_points = 50
        self.counter = 0
        self.timestamps = []
        self.cpu_data = []
        self.memory_data = []
        self.disk_data = []
        self.network_data = []
        self.anomaly_points = []  # [(time, cpu_value), ...]

        # Data fetcher thread
        self.data_fetcher = DataFetcher()
        self.data_fetcher.newData.connect(self.update_stats)
        self.data_fetcher.start()

    def _create_label(self):
        lbl = QLabel()
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 16px;")
        return lbl

    def update_stats(self, cpu, memory, disk, network, anomaly):
        self.counter += 2
        self.timestamps.append(self.counter)
        self.cpu_data.append(cpu)
        self.memory_data.append(memory)
        self.disk_data.append(disk)
        self.network_data.append(network)

        if len(self.timestamps) > self.max_points:
            self.timestamps = self.timestamps[-self.max_points:]
            self.cpu_data = self.cpu_data[-self.max_points:]
            self.memory_data = self.memory_data[-self.max_points:]
            self.disk_data = self.disk_data[-self.max_points:]
            self.network_data = self.network_data[-self.max_points:]
            self.anomaly_points = [(x, y) for x, y in self.anomaly_points if x >= self.timestamps[0]]

        # Label Updates
        self.cpu_label.setText(f"<span style='color:{self.get_color(cpu)}'>CPU: {cpu:.1f}%</span>")
        self.memory_label.setText(f"<span style='color:{self.get_color(memory)}'>Memory: {memory:.1f}%</span>")
        self.disk_label.setText(f"<span style='color:{self.get_color(disk)}'>Disk: {disk:.1f}%</span>")
        self.network_label.setText(f"<span style='color:{self.get_color(network)}'>Network: {network:.1f}%</span>")
        self.anomaly_label.setText("Anomaly Detected!" if anomaly else "Normal")

        # Store anomaly point if any
        if anomaly == 1:
            self.anomaly_points.append((self.counter, cpu))

        # Update all charts
        self.update_canvas(self.cpu_canvas, self.cpu_data, self.anomaly_points)
        self.update_canvas(self.memory_canvas, self.memory_data)
        self.update_canvas(self.disk_canvas, self.disk_data)
        self.update_canvas(self.network_canvas, self.network_data)

    def update_canvas(self, canvas, ydata, anomaly_pts=None):
        canvas.line.set_data(self.timestamps, ydata)
        canvas.ax.set_xlim(min(self.timestamps), max(self.timestamps))

        canvas.draw()

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
