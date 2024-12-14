# Imports
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QLabel, QCalendarWidget, QWidget, QVBoxLayout, QPushButton,
    QHBoxLayout, QFileDialog, QMessageBox, QTableView, QTableWidget, QTableWidgetItem,
    QCheckBox, QDateEdit, QLineEdit, QSizePolicy
)
#
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#
import numpy as np

# Main Class
class FitTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
    
    def settings(self):
      self.setWindowTitle("FitTracker")
      self.resize(800, 600)
    # init UI
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
        self.dark_mode = QCheckBox("Dark Mode")
        
        self.table = QTableWidget()
        
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
        
        self.col2.addWidget(self.table)
        self.col2.addWidget(self.canvas)
        
        # Add Columns to Master Layout
        self.master_layout.addLayout(self.col1)
        self.master_layout.addLayout(self.col2)
        
        # Set Layout
        self.setLayout(self.master_layout)
        
        # Set Window Properties
        self.setWindowTitle("FitTracker")
        self.setGeometry(100, 100, 800, 600)

if __name__ == '__main__':
    app = QApplication([])
    main = FitTracker()
    main.show()
    app.exec_()
