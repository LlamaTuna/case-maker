# controllers/DashboardController.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsEllipseItem
import pyqtgraph as pg

class DashboardController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # Title
        layout.addWidget(QLabel("<h2>Dashboard</h2>"))

        # Line chart
        self.line_chart = pg.PlotWidget(title="Revisions Over Time")
        layout.addWidget(self.line_chart)
        self._populate_line_chart()

        # Pie chart
        self.pie_chart = pg.PlotWidget()
        layout.addWidget(self.pie_chart)
        self._populate_pie_chart()

    def _populate_line_chart(self):
        x = list(range(1, 11))
        y = [5, 7, 6, 8, 12, 15, 18, 20, 22, 25]
        self.line_chart.plot(x, y, pen=pg.mkPen(width=3))

    def _populate_pie_chart(self):
        data = {"Reports": 30, "Photos": 50, "Videos": 10, "Other": 10}
        total = sum(data.values())
        start_deg = 0

        # Lock aspect so circle isn’t squashed
        vb = self.pie_chart.getPlotItem().getViewBox()
        vb.setAspectLocked(True)

        for label, value in data.items():
            span_deg = (value / total) * 360
            wedge = QGraphicsEllipseItem(-100, -100, 200, 200)
            # Angles in Qt are in 1/16th of a degree
            wedge.setStartAngle(int(start_deg * 16))
            wedge.setSpanAngle(int(span_deg * 16))

            # Color based on label hash
            color = pg.intColor(hash(label) % 256)
            wedge.setBrush(pg.mkBrush(color))
            wedge.setPen(pg.mkPen(None))  # no border

            vb.addItem(wedge)
            start_deg += span_deg

        # Hide axes
        self.pie_chart.hideAxis("bottom")
        self.pie_chart.hideAxis("left")
