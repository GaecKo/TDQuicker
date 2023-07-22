import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from TDQuicker import TDQuicker


if __name__ == "__main__":
    app = QApplication(sys.argv)

    icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".assets/WIcon.png")
    app_icon = QIcon(icon_file)
    app.setWindowIcon(app_icon)

    style_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".assets/style.css")

    with open(style_file, 'r') as file:
        app.setStyleSheet(file.read())

    main_window = TDQuicker()
    main_window.show()

    app.exec()