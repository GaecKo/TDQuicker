from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTextEdit

def on_return_pressed():
    print("Return key pressed")

app = QApplication([])
te_text = QTextEdit()
te_text.setReadOnly(False)
te_text.setStyleSheet("""border: 2px solid black;""")

# Detect return key press event
te_text.keyPressEvent = lambda event: on_return_pressed() if event.key() == Qt.Key_Return else QTextEdit.keyPressEvent(te_text, event)

te_text.show()
app.exec()
