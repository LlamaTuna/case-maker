# app.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from controllers.DashboardController import DashboardController
# … you’ll import the other controllers as you build them …

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Case Manager")
        self.resize(1024, 768)

        # Create a tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add the Dashboard tab
        dashboard = DashboardController()
        self.tabs.addTab(dashboard, "Dashboard")

        # In future: self.tabs.addTab(NewCaseController(), "New Case")
        # In future: self.tabs.addTab(CaseViewController(), "Case View")
