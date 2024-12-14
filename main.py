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
  
