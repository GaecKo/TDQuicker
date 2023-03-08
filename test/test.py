import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar
from PySide6.QtCore import Qt 
from PySide6.QtGui import QAction
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a toolbar and add it to the menu bar
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        # Create a button for toggling the sticky state
        sticky_action = QAction('Sticky', self)
        sticky_action.setCheckable(True)
        sticky_action.setChecked(True)
        sticky_action.triggered.connect(self.toggle_sticky)
        toolbar.addAction(sticky_action)    

        # Set the window title and size
        self.setWindowTitle('Sticky App')
        self.setGeometry(100, 100, 500, 300)

    def toggle_sticky(self, checked):
        # Toggle the sticky flag
        self.setWindowFlag(Qt.WindowStaysOnTopHint, checked)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
