import sys
from PyQt5.Qt import QDesktopServices, QUrl, QApplication, QColor, Qt
from PyQt5.QtWidgets import QTextEdit


class MyWidget(QTextEdit):

    def mousePressEvent(self, e):
        self.anchor = self.anchorAt(e.pos())
        if self.anchor:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, e):
        if self.anchor:
            QDesktopServices.openUrl(QUrl(self.anchor))
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.anchor = None


app = QApplication(sys.argv)
editor = MyWidget()
cursor = editor.textCursor()
fmt = cursor.charFormat()
fmt.setForeground(QColor('blue'))
address = 'http://example.com'
fmt.setAnchor(True)
fmt.setAnchorHref(address)
fmt.setToolTip(address)
cursor.insertText("Hello world again", fmt)
editor.show()
app.exec_()