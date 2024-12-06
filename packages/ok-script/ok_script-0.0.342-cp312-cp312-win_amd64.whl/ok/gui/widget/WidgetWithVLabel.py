from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy


class WidgetWithVLabel(QWidget):

    def __init__(self, title, widget: QWidget, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel(title)
        self.layout.addWidget(self.label)
        self.layout.addWidget(widget)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def set_label(self, label):
        self.label.setText(label)
