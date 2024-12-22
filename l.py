import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QLabel, QHeaderView
)
from PyQt5.QtCore import Qt

# Константы для пиковых часов и параметров смены
PEAK_PERIODS = [(7, 9), (17, 19)]
SHIFT_LENGTH = 9

# Данные водителей
drivers_list = [
    {"name": "Водитель 1", "start": 6, "Driver_type": "1"},
    {"name": "Водитель 2", "start": 7, "Driver_type": "1"},
    {"name": "Водитель 3", "start": 8, "Driver_type": "2"},
    {"name": "Водитель 4", "start": 10, "Driver_type": "1"},
    {"name": "Водитель 5", "start": 11, "Driver_type": "2"},
    {"name": "Водитель 6", "start": 13, "Driver_type": "2"},
    {"name": "Водитель 7", "start": 16, "Driver_type": "1"},
    {"name": "Водитель 8", "start": 18, "Driver_type": "2"},
]

# Проверка, является ли час пиковым
def is_peak_hour(hour):
    return any(start <= hour < end for start, end in PEAK_PERIODS)

# Назначение перерывов
def schedule_breaks(shift_hours, driver_type):
    available_hours = [h for h in shift_hours if not is_peak_hour(h)]
    if driver_type == "1":
        return available_hours[:1] if len(available_hours) > 4 else []
    return available_hours[:2] if len(available_hours) >= 2 else []

# Создание смены для водителя
def generate_driver_schedule(driver):
    start_time = driver['start']
    shift_hours = [(start_time + i) % 24 for i in range(SHIFT_LENGTH)]
    breaks = schedule_breaks(shift_hours, driver['Driver_type'])
    
    schedule = {}
    for hour in shift_hours:
        if hour == start_time:
            schedule[hour] = 'Начало смены (час пик)' if is_peak_hour(hour) else 'Начало смены'
        elif hour in breaks:
            schedule[hour] = 'Перерыв'
        else:
            schedule[hour] = 'Поездка (час пик)' if is_peak_hour(hour) else 'Поездка'
    
    schedule[(start_time + SHIFT_LENGTH) % 24] = 'Окончание смены'
    return schedule

# Генерация расписаний для всех водителей
def generate_all_schedules():
    return {driver['name']: generate_driver_schedule(driver) for driver in drivers_list}

# Класс для GUI приложения
class BusScheduleApp(QMainWindow):
    def __init__(self, schedules):
        super().__init__()
        self.setWindowTitle("График смен водителей")
        self.setGeometry(100, 100, 1000, 600)
        self.schedules = schedules
        self.init_ui()

    def init_ui(self):
        # Основной виджет и layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Заголовок
        title_label = QLabel("График смен водителей автобусов")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin: 10px; color: #2E3B4E;")
        layout.addWidget(title_label)

        # Создание и заполнение таблицы
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Водитель", "Время", "Действие"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.populate_table()
        layout.addWidget(self.table)

    def populate_table(self):
        row = 0
        for driver, hours in self.schedules.items():
            for hour, action in sorted(hours.items()):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(driver))
                self.table.setItem(row, 1, QTableWidgetItem(f"{hour:02d}:00"))
                self.table.setItem(row, 2, QTableWidgetItem(action))
                row += 1
        # Стилизация таблицы
        self.table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                background-color: #F7F9FC;
                gridline-color: #B0BEC5;
            }
            QHeaderView::section {
                background-color: #37474F;
                color: white;
                padding: 6px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #B0BEC5;
            }
        """)

# Основная функция
def main():
    app = QApplication(sys.argv)
    schedules = generate_all_schedules()
    window = BusScheduleApp(schedules)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
