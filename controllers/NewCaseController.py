# controllers/NewCaseController.py
from pathlib import Path
import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QGroupBox, QCheckBox, QFormLayout,
    QMessageBox
)
from utils.Validators import Validators
from utils.Settings import Settings
from services.LogService import LogService

class NewCaseController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Settings()
        self.logger = LogService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Case Number & Investigator
        form = QFormLayout()
        self.case_id_input = QLineEdit()
        form.addRow("Case Number:", self.case_id_input)
        self.investigator_input = QLineEdit()
        form.addRow("Investigator:", self.investigator_input)
        layout.addLayout(form)

        # Base Path selector
        path_layout = QHBoxLayout()
        self.base_path_input = QLineEdit(str(self.settings.case_root))
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_base_path)
        path_layout.addWidget(QLabel("Base Path:"))
        path_layout.addWidget(self.base_path_input)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # Folder checklist
        group = QGroupBox("Folders to create")
        grid = QVBoxLayout()
        self.checkboxes = {}
        for name in [
            "Reports", "Photos", "Videos", "Property Receipts",
            "Audio Recordings", "DHS 307s", "Exhibits",
            "Digital Forensics", "Other Attachments"
        ]:
            cb = QCheckBox(name)
            cb.setChecked(True)
            grid.addWidget(cb)
            self.checkboxes[name] = cb

        # Custom folder
        self.custom_input = QLineEdit()
        cb_custom = QCheckBox("Custom:")
        cb_custom.stateChanged.connect(self._toggle_custom)
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(cb_custom)
        custom_layout.addWidget(self.custom_input)
        grid.addLayout(custom_layout)
        self.checkboxes["Custom"] = (cb_custom, self.custom_input)

        group.setLayout(grid)
        layout.addWidget(group)

        # Action buttons
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("Create")
        cancel_btn = QPushButton("Cancel")
        create_btn.clicked.connect(self._create_case)
        cancel_btn.clicked.connect(self._cancel)
        btn_layout.addStretch()
        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def _browse_base_path(self):
        path = QFileDialog.getExistingDirectory(
            self, "Select Base Path", str(self.settings.case_root)
        )
        if path:
            self.base_path_input.setText(path)

    def _toggle_custom(self, state):
        cb, input_field = self.checkboxes["Custom"]
        input_field.setEnabled(state == cb.checkState())

    def _create_case(self):
        case_id = self.case_id_input.text().strip()
        if not Validators.is_valid_case_id(case_id):
            QMessageBox.warning(
                self, "Invalid Case ID",
                "Please enter a valid case number (e.g. 2025-12345678-Jones)"
            )
            return

        investigator = self.investigator_input.text().strip() or None
        base = Path(self.base_path_input.text().strip())
        parent_dir = base / case_id

        # Collision handling
        if parent_dir.exists():
            resp = QMessageBox.question(
                self, "Case Exists",
                f"Folder {parent_dir} already exists.\n\nDo you want to merge into it?",
                QMessageBox.Yes | QMessageBox.No
            )
            if resp == QMessageBox.No:
                return
        else:
            parent_dir.mkdir(parents=True, exist_ok=True)

        # Collect folders
        folders = []
        for name, widget in self.checkboxes.items():
            if name == "Custom":
                cb, input_field = widget
                custom_name = input_field.text().strip()
                if cb.isChecked() and custom_name:
                    folders.append(custom_name)
            else:
                if widget.isChecked():
                    folders.append(name)

        # Create subfolders and log
        for fld in folders:
            path = parent_dir / fld
            path.mkdir(exist_ok=True)
            self.logger.log_folder_creation(case_id, str(path))

        # Log case creation
        self.logger.log_case_created(case_id, str(parent_dir))

        QMessageBox.information(
            self, "Case Created",
            f"Case {case_id} initialized with {len(folders)} folders."
        )

        # TODO: Notify MainWindow to open new Case View tab

    def _cancel(self):
        parent = self.parent()
        if parent:
            idx = parent.tabs.currentIndex()
            parent.tabs.removeTab(idx)
