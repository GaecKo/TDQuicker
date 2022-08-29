### Code créé par GaecKo, inspiré de Docstring. 
from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QTextEdit, QVBoxLayout, QPushButton, QWidget, QApplication, QListWidget, QLineEdit, QCheckBox, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import *


from functools import partial

# To Do: dic : {layout_to_do: [QTCheckButton, QtPushButton, QtPushButton]}}

class TDQuicker(QWidget):
    class Task:
        def __init__(self, GenHBox, LeftH, CheckButton, RightH, DeleteButton):
            self.GenHBox = GenHBox
            self.LeftH = LeftH
            self.CheckButton = CheckButton
            self.RightH = RightH
            self.DeleteButton = DeleteButton
            self.attributes = [self.GenHBox, self.LeftH, self.CheckButton, self.RightH, self.DeleteButton]
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDQuicker")
        self.setStyleSheet("""
                background-color: rgb(200, 200, 200)""")
        
        self.__create_ui()
        
        self.ip_add.returnPressed.connect(self.add_task)
        self.btn_clearAll.pressed.connect(self.clear_all_tasks)

    def add_task(self):
        lab_text = self.ip_add.text()
        if lab_text in self.tasks:
            return 
        self.ip_add.clear()
        GenHBox = QHBoxLayout()
        LeftH = QHBoxLayout()
        CheckButton = QCheckBox(lab_text)
        
        RightH = QHBoxLayout()
        Icon = QIcon(".requirement/bin.png")
        DeleteButton = QPushButton(icon=Icon)
        DeleteButton.setMaximumWidth(25)
        DeleteButton.setMaximumHeight(25)
        DeleteButton.setStyleSheet("""
                            QPushButton {
                                margin-right: 0;
                                border: 5;
                                font-size: 16;
                            }
        """)

        task = self.Task(GenHBox, LeftH, CheckButton, RightH, DeleteButton)
        self.tasks[lab_text] = task

        RightH.addWidget(DeleteButton)
        LeftH.addWidget(CheckButton)
        
        GenHBox.addLayout(LeftH)
        GenHBox.addLayout(RightH)

        DeleteButton.pressed.connect(partial(self.delete_task, CheckButton))
        CheckButton.pressed.connect(partial(self.done_task, CheckButton))

        self.tasks_layout.addLayout(GenHBox)

    def done_task(self, CheckButton):
        for CheckButton_text, task_elem in self.tasks.items():
            if CheckButton == task_elem.CheckButton:
                print('Found task elem!')

    def delete_task(self, CheckButton):
        for CheckButton_text, task_elem in self.tasks.items():
            if CheckButton == task_elem.CheckButton:
                for attribute in task_elem.attributes:
                    attribute.deleteLater()
                del self.tasks[CheckButton_text]  
                return

    def clear_all_tasks(self):
        for CheckButton_text, task_elem in self.tasks.items():
            for attribute in task_elem.attributes:
                attribute.deleteLater()
        self.tasks = {}

    def __create_ui(self, tasks={}):
        self.main_layout = QVBoxLayout(self)
        self.tasks_layout = QVBoxLayout()
        self.resize(250, 500)
        self.main_layout.setSpacing(0)
        #self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # items
        self.ip_add = QLineEdit(); self.ip_add.setPlaceholderText("Add Task")
        self.ip_add.setStyleSheet("""
            background-color: white;
        """)
        self.ip_add.setMinimumHeight(30)
        self.tasks = tasks

        self.btn_clearAll = QPushButton("Click to Clear All")
        self.lbl_action = QLabel()

        #items added in layout
        self.main_layout.addWidget(self.ip_add) 
        self.main_layout.addLayout(self.tasks_layout)

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.btn_clearAll)
        self.main_layout.addWidget(self.lbl_action)

if __name__ == "__main__":
    app = QApplication()

    main_window = TDQuicker()
    main_window.show()

    app.exec()