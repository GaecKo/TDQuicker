### Code créé par GaecKo, inspiré de Docstring. 
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QApplication, QListWidget, QLineEdit, QLabel
from functools import partial

# To Do: dic : {layout_to_do: [QTLabel, QtPushButton, QtPushButton]}}

class TDQuicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDQuicker")
        self.main_layout = QVBoxLayout(self)
        # items
        self.lst_tasks = QListWidget()
        self.ip_add = QLineEdit(); self.ip_add.setPlaceholderText("ToDo to add")

        self.mid_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.ip_search = QLineEdit(); self.ip_search.setPlaceholderText("Search")
        self.btn_back = QPushButton("Back")

        self.lbl_test = QLabel("Hello Test")

        self.btn_clearAll = QPushButton("Click to Clear All")
        self.lbl_action = QLabel()


        #items added in layout
        self.main_layout.addWidget(self.lbl_test)
        self.main_layout.addWidget(self.lst_tasks)
        self.main_layout.addWidget(self.ip_add) 

        self.mid_layout.addLayout(self.left_layout)
        self.left_layout.addWidget(self.ip_search)

        self.mid_layout.addLayout(self.right_layout)
        self.right_layout.addWidget(self.btn_back)
        self.temp_list = QListWidget()
        self.temp_list_on = False

        self.main_layout.addLayout(self.mid_layout)
        self.main_layout.addWidget(self.btn_clearAll)
        self.main_layout.addWidget(self.lbl_action)

        self.ip_add.returnPressed.connect(self.add_in_list)
        self.btn_clearAll.pressed.connect(self.clear_all)
        self.ip_search.returnPressed.connect(self.search_task)
        self.btn_back.pressed.connect(self.back_list)
        

    def clear_all(self):
        if self.temp_list_on:
            self.temp_list.deleteLater()
        self.temp_list_on = False
        self.lst_tasks.clear()

    def search_task(self):
        self.temp_list = QListWidget()
        self.keyword = self.ip_search.text()
        count = 0
        for index in range(self.lst_tasks.count()):
            if self.keyword.lower() in self.lst_tasks.item(index).text().lower():
                self.temp_list.addItem(self.lst_tasks.item(index).text())
                count += 1
        if count > 0:
            self.main_layout.addWidget(self.temp_list)
            self.temp_list_on = True
        self.ip_search.clear()
    
    def back_list(self):
        if self.temp_list_on:
            self.temp_list.deleteLater()
        self.temp_list_on = False

    def add_in_list(self):
        self.lst_tasks.addItem(self.ip_add.text())
        self.ip_add.clear()

if __name__ == "__main__":
    app = QApplication()

    main_window = TDQuicker()
    main_window.show()
    app.exec()