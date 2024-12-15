# Imports
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QLabel, QCalendarWidget, QWidget, QVBoxLayout, QPushButton,
    QHBoxLayout, QFileDialog, QMessageBox, QTableView, QTableWidget, QTableWidgetItem,
    QCheckBox, QDateEdit, QLineEdit, QSizePolicy, QHeaderView,
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


# Main Class
class FitTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.button_click()

    def settings(self):
        self.setWindowTitle("FitTracker")
        self.resize(800, 600)

    # Initialize UI
    def initUI(self):
        # Widgets
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())

        self.kal_box = QLineEdit()
        self.kal_box.setPlaceholderText("Calories Burned")

        self.distance_box = QLineEdit()
        self.distance_box.setPlaceholderText("Distance Covered")

        self.description = QLineEdit()
        self.description.setPlaceholderText("Description")

        self.submit_button = QPushButton("Submit")
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")
        self.clear_button = QPushButton("Clear")

        self.dark_mode = QCheckBox("Dark Mode")  # Initialize dark_mode
        self.dark_mode.stateChanged.connect(self.toggle_dark_mode)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Date", "Calories Burned", "Distance Covered", "Description"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Design Layouts
        self.master_layout = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        self.sub_row1 = QHBoxLayout()
        self.sub_row2 = QHBoxLayout()
        self.sub_row3 = QHBoxLayout()
        self.sub_row4 = QHBoxLayout()

        # Populate Rows
        self.sub_row1.addWidget(QLabel("Date: "))
        self.sub_row1.addWidget(self.date_box)

        self.sub_row2.addWidget(QLabel("Calories Burned: "))
        self.sub_row2.addWidget(self.kal_box)

        self.sub_row3.addWidget(QLabel("Distance Covered: "))
        self.sub_row3.addWidget(self.distance_box)

        self.sub_row4.addWidget(QLabel("Description: "))
        self.sub_row4.addWidget(self.description)

        # Add to Layouts
        self.col1.addLayout(self.sub_row1)
        self.col1.addLayout(self.sub_row2)
        self.col1.addLayout(self.sub_row3)
        self.col1.addLayout(self.sub_row4)
        self.col1.addWidget(self.dark_mode)

        btn_row1 = QHBoxLayout()
        btn_row2 = QHBoxLayout()

        btn_row1.addWidget(self.add_button)
        btn_row1.addWidget(self.delete_button)
        btn_row2.addWidget(self.submit_button)
        btn_row2.addWidget(self.clear_button)

        self.col1.addLayout(btn_row1)
        self.col1.addLayout(btn_row2)

        self.col2.addWidget(self.canvas)
        self.col2.addWidget(self.table)

        # Add Columns to Master Layout
        self.master_layout.addLayout(self.col1, 30)
        self.master_layout.addLayout(self.col2, 70)

        # Set Layout
        self.setLayout(self.master_layout)
        self.apply_styles()
        self.load_table()

    # Events
    def button_click(self):
        self.add_button.clicked.connect(self.add_workout)
        self.delete_button.clicked.connect(self.delete_workout)
        self.submit_button.clicked.connect(self.calculate_calories)
        self.dark_mode.stateChanged.connect(self.toggle_dark_mode)
        self.clear_button.clicked.connect(self.clear_form)

    # Load Table
    def load_table(self):
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM fittracker ORDER BY date DESC")
        row = 0
        while query.next():
            fit_id = query.value(0)
            date = query.value(1)
            calories = query.value(2)
            distance = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(fit_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(str(calories)))
            self.table.setItem(row, 3, QTableWidgetItem(str(distance)))
            self.table.setItem(row, 4, QTableWidgetItem(description))
            row += 1

    # Add Workout
    def add_workout(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        calories = self.kal_box.text()
        distance = self.distance_box.text()
        description = self.description.text()

        if not calories or not distance:
            QMessageBox.warning(self, "Warning", "Please enter calories and distance")
            return

        query = QSqlQuery()
        query.prepare(
            "INSERT INTO fittracker (date, calories, distance, description) VALUES (?, ?, ?, ?)"
        )
        query.addBindValue(date)
        query.addBindValue(calories)
        query.addBindValue(distance)
        query.addBindValue(description)

        if query.exec_():
            self.load_table()
            self.clear_form()
        else:
            QMessageBox.critical(self, "Error", query.lastError().text())

    # Delete Workout
    def delete_workout(self):
        row = self.table.currentRow()
        if row == -1:
            return

        fit_id = self.table.item(row, 0).text()
        confirm = QMessageBox.question(
            self,
            "Delete",
            "Are you sure you want to delete this workout?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.No:
            return

        query = QSqlQuery()
        query.prepare("DELETE FROM fittracker WHERE id = ?")
        query.addBindValue(fit_id)

        if query.exec_():
            self.load_table()
        else:
            QMessageBox.critical(self, "Error", "Please choose a row to delete")

    # Calculate Calories
    def calculate_calories(self):
        distances = []
        calories = []

        query = QSqlQuery("SELECT distance, calories FROM fittracker ORDER BY calories ASC")
        while query.next():
            distance = query.value(0)
            calorie = query.value(1)

            if distance is not None and calorie is not None:
                distances.append(float(distance))
                calories.append(float(calorie))

        if not distances or not calories:
            QMessageBox.warning(self, "Warning", "No data available to calculate!")
            return

        try:
            min_calorie = min(calories)
            max_calories = max(calories)
            normalized_calories = [(calorie - min_calorie) / (max_calories - min_calorie) for calorie in calories]
            self.figure.clear()
            ax = self.figure.subplots()
            ax.scatter(distances, calories, c=normalized_calories, cmap="viridis", label="Data Points")
            ax.set_title("Calories vs Distance")
            ax.set_xlabel("Distance (km)")
            ax.set_ylabel("Calories Burned")
            cbar = self.figure.colorbar(ax.collections[0], label="Normalized Calories")
            ax.grid(True)
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #FFFFFF; color: #000000; }
            QPushButton { background-color: #555555; color: #FFFFFF; border: 1px solid #777777; }
            QLineEdit, QDateEdit, QTableWidget { background-color: #FFFFFF; color: #000000; border: 1px solid #555555; }
            QHeaderView::section { background-color: #555555; color: #FFFFFF; }
        """)
        figure_color = "#b8c9e1"
        self.figure.patch.set_facecolor(figure_color)
        self.canvas.setStyleSheet(f"background-color: {figure_color};")

    # Clear Form
    def clear_form(self):
        self.kal_box.clear()
        self.distance_box.clear()
        self.description.clear()
        self.date_box.setDate(QDate.currentDate())
        self.figure.clear()
        self.canvas.draw()

    # Toggle Dark Mode
    def toggle_dark_mode(self, state):
        if state == Qt.Checked:
            self.setStyleSheet("""
                QWidget { background-color: #2E2E2E; color: #FFFFFF; }
                QPushButton { background-color: #555555; color: #FFFFFF; border: 1px solid #777777; }
                QLineEdit, QDateEdit, QTableWidget { background-color: #3E3E3E; color: #FFFFFF; border: 1px solid #555555; }
                QHeaderView::section { background-color: #555555; color: #FFFFFF; }
            """)
        else:
            self.setStyleSheet("")


# Initialize Database
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("fittracker.db")

if not db.open():
    QMessageBox.critical(None, "Error", "Cannot open the database")
    exit(2)

query = QSqlQuery()
query.exec_("""
    CREATE TABLE IF NOT EXISTS fittracker (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    calories REAL,
    distance REAL,
    description TEXT
    )
""")

# Run the Application
if __name__ == "__main__":
    app = QApplication([])
    main = FitTracker()
    main.show()
    app.exec_()
