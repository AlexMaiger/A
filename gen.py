import sys
import random
import copy
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QLabel, QHeaderView, QScrollArea
)
from PyQt5.QtCore import Qt

# Параметры
POPULATION_SIZE = 20
GENERATIONS = 50
SHIFT_DURATION = 9
PEAK_HOURS = [(7, 9), (17, 19)]
DRIVER_TYPES = ["1", "2"]

# Генерация случайного расписания
def generate_random_schedule():
    drivers = []
    for i in range(8):
        driver = {
            "name": f"Водитель {i + 1}",
            "start": random.randint(6, 18),
            "Driver_type": random.choice(DRIVER_TYPES)
        }
        drivers.append(driver)
    return drivers

# Проверка, является ли час пиковым
def is_peak(hour):
    return any(start <= hour < end for start, end in PEAK_HOURS)

# Функция оценки (фитнес-функция)
def fitness(schedule):
    total_drivers = len(schedule)
    peak_coverage = 0

    for driver in schedule:
        shift_start = driver['start']
        shift_hours = [(shift_start + i) % 24 for i in range(SHIFT_DURATION)]
        for hour in shift_hours:
            if is_peak(hour):
                peak_coverage += 1

    # Максимизация покрытия пиковых часов, минимизация количества водителей
    return peak_coverage - total_drivers * 2

# Оператор скрещивания – однородный кроссовер
def crossover(parent1, parent2):
    child = []
    for d1, d2 in zip(parent1, parent2):
        if random.random() > 0.5:
            child.append(copy.deepcopy(d1))
        else:
            child.append(copy.deepcopy(d2))
    return child

# Оператор мутации – изменяет время начала смены и тип водителя
def mutate(chromosome):
    idx = random.randint(0, len(chromosome) - 1)
    chromosome[idx]['start'] = random.randint(6, 18)
    chromosome[idx]['Driver_type'] = random.choice(DRIVER_TYPES)

# Турнирный отбор
def tournament_selection(population, k=5):
    selected = random.sample(population, k)
    selected.sort(key=fitness, reverse=True)
    return selected[0]

# Основной цикл генетического алгоритма
def genetic_algorithm():
    # Инициализация начальной популяции
    population = [generate_random_schedule() for _ in range(POPULATION_SIZE)]

    for gen in range(GENERATIONS):
        # Сортировка по фитнесу
        population.sort(key=fitness, reverse=True)
        next_gen = population[:5]  # Элитизм: переносим лучших особей

        # Генерация новой популяции
        while len(next_gen) < POPULATION_SIZE:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            if random.random() < 0.2:  # Вероятность мутации
                mutate(child)
            next_gen.append(child)

        population = next_gen
        best_fitness = fitness(population[0])
        print(f"Поколение {gen + 1}: Лучший фитнес = {best_fitness}")

    return population[0]

# Преобразование расписания в удобный формат для GUI
def format_schedule(schedule):
    formatted = {}
    for driver in schedule:
        shift_start = driver['start']
        shift_hours = [(shift_start + i) % 24 for i in range(SHIFT_DURATION)]
        driver_schedule = {}
        for hour in shift_hours:
            if hour == shift_start:
                driver_schedule[hour] = "Начало смены"
            elif is_peak(hour):
                driver_schedule[hour] = "Поездка (час пик)"
            else:
                driver_schedule[hour] = "Поездка"
        driver_schedule[(shift_start + SHIFT_DURATION) % 24] = "Окончание смены"
        formatted[driver["name"]] = driver_schedule
    return formatted

# GUI приложение
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
            for hour, action in sorted(hours.items()):
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
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #ccc;
            }
        """)

# Основная функция
def main():
    best_schedule = genetic_algorithm()
    formatted_schedule = format_schedule(best_schedule)

    app = QApplication(sys.argv)
    window = ScheduleApp(formatted_schedule)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
