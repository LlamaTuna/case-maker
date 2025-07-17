# controllers/CaseViewController.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QListView, QTextEdit

class CaseViewController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Basic layout
        layout = QVBoxLayout(self)

        # TODO: replace with your actual widgets and setup
        self.folderTree = QTreeView()
        self.fileList  = QListView()
        self.preview   = QTextEdit()
        self.preview.setReadOnly(True)

        layout.addWidget(self.folderTree)
        layout.addWidget(self.fileList)
        layout.addWidget(self.preview)
