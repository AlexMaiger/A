import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QLabel, QHeaderView, QScrollArea
)
from PyQt5.QtCore import Qt

# Пример расписания для всех водителей
schedule = {
    "Водитель 1": {6: "Начало смены", 7: "Поездка", 8: "Перерыв", 15: "Окончание смены"},
    "Водитель 2": {7: "Начало смены (час пик)", 8: "Поездка (час пик)", 9: "Перерыв", 16: "Окончание смены"},
    "Водитель 3": {8: "Начало смены", 10: "Поездка", 13: "Перерыв", 17: "Окончание смены"},
    "Водитель 4": {9: "Начало смены", 11: "Поездка", 14: "Перерыв", 18: "Окончание смены"},
    "Водитель 5": {10: "Начало смены", 12: "Поездка", 15: "Перерыв", 19: "Окончание смены"},
    "Водитель 6": {11: "Начало смены", 13: "Поездка", 16: "Перерыв", 20: "Окончание смены"},
    "Водитель 7": {12: "Начало смены", 14: "Поездка", 17: "Перерыв", 21: "Окончание смены"},
    "Водитель 8": {13: "Начало смены", 15: "Поездка", 18: "Перерыв", 22: "Окончание смены"},
}

class ScheduleApp(QMainWindow):
    def __init__(self, schedule):
        super().__init__()
        self.setWindowTitle("Расписание водителей автобусов")
        self.setGeometry(100, 100, 800, 600)
        self.schedule = schedule
        self.initUI()

    def initUI(self):
        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Создание прокручиваемой области
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Основной layout
        layout = QVBoxLayout(main_widget)

        # Заголовок
        title = QLabel("Расписание водителей автобусов", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)

        # Виджет для таблицы
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)

        # Создание таблицы
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Водитель", "Время", "Действие"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        # Заполнение таблицы данными
        self.populate_table()

        # Добавляем таблицу в layout
        table_layout.addWidget(self.table)
        scroll.setWidget(table_widget)
        layout.addWidget(scroll)

    def populate_table(self):
        row = 0
        for driver, hours in self.schedule.items():
            for hour, action in hours.items():
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(driver))
                self.table.setItem(row, 1, QTableWidgetItem(f"{hour:02d}:00"))
                self.table.setItem(row, 2, QTableWidgetItem(action))
                row += 1

        # Оформление таблицы
        self.table.setStyleSheet("""
            QTableWidget {
                font-size: 16px;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #444;
                color: white;
                padding: 5px;
                font-size: 16px;
            }
            QTableWidgetItem {
                padding: 10px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #ccc;
            }
        """)


def main():
    app = QApplication(sys.argv)
    window = ScheduleApp(schedule)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
