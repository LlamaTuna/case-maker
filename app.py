# app.py
from PySide6.QtWidgets import QMainWindow, QTabWidget
from controllers.DashboardController import DashboardController
from controllers.NewCaseController import NewCaseController
from controllers.CaseViewController import CaseViewController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Case Manager")
        self.resize(1024, 768)

        # Tab widget setup
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Register each tab
        self.tabs.addTab(DashboardController(), "Dashboard")
        self.tabs.addTab(NewCaseController(), "New Case")
        self.tabs.addTab(CaseViewController(), "Case View")
