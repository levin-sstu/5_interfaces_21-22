import os
import csv
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, \
    QFileDialog, QComboBox, QLabel, QCheckBox, QDialog

# Установка пути для плагинов
os.environ['QT_PLUGIN_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Lib', 'site-packages',
                                            'PyQt5', 'Qt5', 'plugins')


class DataViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Создаем QTableWidget
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        # Диалог для выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Чтение первой строки для заголовков
                self.table_widget.setColumnCount(len(headers))
                self.table_widget.setHorizontalHeaderLabels(headers)

                row_data = list(reader)
                self.table_widget.setRowCount(len(row_data))

                # Заполнение таблицы данными
                for row_idx, row in enumerate(row_data):
                    for col_idx, item in enumerate(row):
                        self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(item))


class ChartSettingsDialog(QDialog):
    def __init__(self, headers, data):
        super().__init__()
        self.setWindowTitle("Chart Settings")
        self.data = data  # Directly store the data passed from MainWindow
        self.init_ui(headers)

    def init_ui(self, headers):
        layout = QVBoxLayout()

        # Комбинированный список для выбора типа диаграммы
        self.chart_type_combo = QComboBox(self)
        self.chart_type_combo.addItems(["Line", "Bar", "Scatter"])
        layout.addWidget(QLabel("Select Chart Type"))
        layout.addWidget(self.chart_type_combo)

        # Настройка выбора цветов, осей и подписей
        self.color_checkbox = QCheckBox("Custom Line Color", self)
        layout.addWidget(self.color_checkbox)

        # Выбор столбцов для графика
        self.column_combo_x = QComboBox(self)
        self.column_combo_y = QComboBox(self)

        self.column_combo_x.addItems(headers)
        self.column_combo_y.addItems(headers)

        layout.addWidget(QLabel("Select X Column"))
        layout.addWidget(self.column_combo_x)

        layout.addWidget(QLabel("Select Y Column"))
        layout.addWidget(self.column_combo_y)

        # Кнопка для создания диаграммы
        self.create_button = QPushButton("Create Chart", self)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

        self.create_button.clicked.connect(self.create_chart)

    def get_selected_options(self):
        return {
            "chart_type": self.chart_type_combo.currentText(),
            "custom_color": self.color_checkbox.isChecked(),
            "x_column": self.column_combo_x.currentText(),
            "y_column": self.column_combo_y.currentText(),
        }

    def create_chart(self):
        selected_options = self.get_selected_options()
        print("Selected options:", selected_options)

        # Use selected x and y columns
        x_column = selected_options["x_column"]
        y_column = selected_options["y_column"]

        print(f"Creating chart with {x_column} and {y_column}")

        # Pass the selected data and options to the chart creator
        chart_creator = ChartCreator(self.data, selected_options)
        chart_creator.create_chart()


class ChartCreator:
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

    def create_chart(self):
        # Получаем выбранные столбцы для построения графика
        x_column = self.settings["x_column"]
        y_column = self.settings["y_column"]

        # Extract data for x and y columns
        x_data = [row[x_column] for row in self.data]
        y_data = [row[y_column] for row in self.data]

        print(f"x_data: {x_data}")
        print(f"y_data: {y_data}")

        fig, ax = plt.subplots()

        if self.settings["chart_type"] == "Line":
            ax.plot(x_data, y_data, color='blue' if not self.settings["custom_color"] else 'red')
        elif self.settings["chart_type"] == "Bar":
            ax.bar(x_data, y_data)
        elif self.settings["chart_type"] == "Scatter":
            ax.scatter(x_data, y_data)

        # Параметры подписей осей
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

        # Сохранение графика в файл
        self.save_chart(fig)

    def save_chart(self, fig):
        # Открытие диалога для выбора места сохранения и типа файла
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix(".png")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Images (*.jpg *.png *.bmp)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            fig.savefig(file_path)
            print(f"Chart saved to: {file_path}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Загружаем данные
        self.viewer = DataViewer()
        layout.addWidget(self.viewer)

        # Кнопка для открытия диалога с параметрами диаграммы
        self.settings_button = QPushButton("Set Chart Settings", self)
        self.settings_button.clicked.connect(self.show_settings)
        layout.addWidget(self.settings_button)

        self.setLayout(layout)

    def show_settings(self):
        headers = [self.viewer.table_widget.horizontalHeaderItem(i).text() for i in
                   range(self.viewer.table_widget.columnCount())]
        data = self.get_selected_data()  # Get the data to pass to the settings dialog
        settings_dialog = ChartSettingsDialog(headers, data)  # Pass headers and data to the dialog
        settings_dialog.exec_()  # Show the dialog

    def get_selected_data(self):
        headers = [self.viewer.table_widget.horizontalHeaderItem(i).text() for i in
                   range(self.viewer.table_widget.columnCount())]
        data = []
        for row_idx in range(self.viewer.table_widget.rowCount()):
            row_data = {}
            for col_idx, header in enumerate(headers):
                item = self.viewer.table_widget.item(row_idx, col_idx)
                row_data[header] = float(item.text()) if item else 0
            data.append(row_data)
        return data


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
