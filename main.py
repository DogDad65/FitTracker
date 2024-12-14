# Imports
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QCalendarWidget, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QTableView, QTableWidget, QTableWidgetItem, QCheckBox, QDateEdit, QLineEdit
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
#
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#
import numpy as np
from sys import exit

# Main Class
class FitTracker(QWidget):
  def __init__(self):
    super().__init__()
    
  # init UI
  def initUI(self):
    self.date_box = QDateEdit()
    self.date_box.setDate(QDate.currentDate())
    
    self.kal_box = QLineEdit()
    self.kal_box_box.setPlaceholderText("Calories Burned")
    self.distance_box = QLineEdit()
    self.distance_box.setPlaceholderText("Distance Covered")
    self.description = QLineEdit()
    self.description.setPlaceholderText("Description")
    
    self.submit_button = QPushButton("Submit")
    self.add_button = QPushButton("Add")
    self.delete_button = QPushButton("Delete")
    self.clear_button = QPushButton("Clear")
    self.dark_mode = QCheckBox("Dark Mode")
    
    # Load Tables
    
    # Add Tables
    
    # Delete Tables
    
    # Calculate Calories
    
