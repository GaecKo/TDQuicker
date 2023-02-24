from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QLabel, QSizePolicy
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        scroll_area = QScrollArea(widgetResizable=True)
        main_layout.addWidget(scroll_area)

        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        scroll_layout = QVBoxLayout(scroll_widget)
        for i in range(50):
            label = QLabel(f"Label {i}")
            scroll_layout.addWidget(label)

        # set vertical size policy to expanding
        scroll_widget.setSizePolicy(
            scroll_widget.sizePolicy().horizontalPolicy(),
            scroll_widget.sizePolicy().verticalPolicy() | QSizePolicy.Expanding
        )

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
