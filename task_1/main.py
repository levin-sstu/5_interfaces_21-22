import os
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

os.environ['QT_PLUGIN_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графики и диаграммы")
        self.setGeometry(100, 100, 1200, 800)

        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Вкладки
        tab_widget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        main_widget.setLayout(layout)

        # Добавляем вкладки с графиками
        tab_widget.addTab(self.create_area_chart(), "Area Chart")
        tab_widget.addTab(self.create_pie_chart(), "Pie Chart")
        tab_widget.addTab(self.create_line_chart(), "Line Chart")
        tab_widget.addTab(self.create_bar_chart(), "Bar Chart")
        tab_widget.addTab(self.create_spline_chart(), "Spline Chart")
        tab_widget.addTab(self.create_scatter_chart(), "Scatter Chart")
        tab_widget.addTab(self.create_simple_line_chart(), "Simple Line Chart")
        tab_widget.addTab(self.create_simple_bar_chart(), "Simple Bar Chart")
        tab_widget.addTab(self.create_radar_chart(), "Radar Chart")

    def create_area_chart(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        x = np.linspace(0, 6, 100)
        y1 = np.sin(x)
        y2 = y1 + 1
        y3 = y2 + 1
        ax.fill_between(x, 0, y1, color="blue", alpha=0.6)
        ax.fill_between(x, y1, y2, color="green", alpha=0.6)
        ax.fill_between(x, y2, y3, color="orange", alpha=0.6)
        ax.set_title("Area Chart")
        return canvas

    def create_pie_chart(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        sizes = [10, 20, 30, 40]
        labels = ['Slice 1', 'Slice 2', 'Slice 3', 'Slice 4']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax.set_title("Pie Chart")
        return canvas

    def create_line_chart(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        y3 = np.sin(x) + np.cos(x)
        ax.plot(x, y1, label="sin(x)", color="blue")
        ax.plot(x, y2, label="cos(x)", color="green")
        ax.plot(x, y3, label="sin(x)+cos(x)", color="orange")
        ax.legend()
        ax.set_title("Line Chart")
        return canvas

    def create_bar_chart(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        categories = ['A', 'B', 'C', 'D']
        values1 = [5, 7, 8, 6]
        values2 = [4, 3, 9, 5]
        x = np.arange(len(categories))
        ax.bar(x - 0.2, values1, width=0.4, label="Set 1", color="blue")
        ax.bar(x + 0.2, values2, width=0.4, label="Set 2", color="orange")
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.set_title("Bar Chart")
        return canvas

    def create_spline_chart(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = y1 + 0.5
        y3 = y2 + 0.5
        ax.plot(x, y1, label="Spline 1", color="blue")
        ax.plot(x, y2, label="Spline 2", color="green")
        ax.plot(x, y3, label="Spline 3", color="orange")
        ax.legend()
        ax.set_title("Spline Chart")
        return canvas

    def create_scatter_chart(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        x = np.random.rand(50)
        y = np.random.rand(50)
        sizes = np.random.rand(50) * 100
        ax.scatter(x, y, s=sizes, color="blue", alpha=0.6)
        ax.set_title("Scatter Chart")
        return canvas

    def create_simple_line_chart(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, color="blue")
        ax.set_title("Simple Line Chart")
        return canvas

    def create_simple_bar_chart(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        values = [5, 6, 7, 8, 5, 6]
        ax.bar(categories, values, color="blue")
        ax.set_title("Simple Bar Chart")
        return canvas

    def create_radar_chart(self):
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111, polar=True)
        categories = ['A', 'B', 'C', 'D', 'E']
        values = [4, 3, 2, 5, 4]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        ax.plot(angles, values, color="blue")
        ax.fill(angles, values, color="blue", alpha=0.25)
        ax.set_title("Radar Chart")
        return canvas


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
