# Author: Arthur De Neyer (GaecKo)
# Date: 26/02/2023
# GitHub: https://github.com/GaecKo/TDQuicker 

from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QTextEdit, QVBoxLayout, QPushButton, QWidget, QApplication, QLineEdit, QCheckBox, QLabel, QGroupBox, QMessageBox, QScrollArea
from PySide6.QtGui import QIcon, QTextOption
from PySide6.QtCore import Qt

from datetime import datetime
from data.data import * 
import time


from functools import partial

class TDQuicker(QWidget):
    class Task:
        # Used to 
        def __init__(self, task_text, date: str =None):
            self.task_text = task_text
            self.create_task(date)

        def create_task(self, date: str =None): 
            # Create the QGroupBox 
            self.GroupBox = QGroupBox()

            # Create the QCheckBox and QPushButton widgets
            self.CheckButton = QCheckBox()
            self.CheckButton.setMaximumSize(25, 25)

            # Text of the task 
            self.le_text = QTextEdit(self.task_text)
            self.le_text.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
            self.le_text.setReadOnly(True)
              # set a fixed height
            self.le_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # hide the vertical scrollbar
            recommanded_height = (len(self.task_text) / 17) * 17
            self.le_text.setMinimumHeight(recommanded_height)
            
            self.le_text.setObjectName("taskText")

            # Icon and button to delete task
            self.bin = QIcon(".assets/bin.png")
            self.DeleteButton = QPushButton(self.bin, "")
            self.DeleteButton.setMaximumSize(20, 30)
            self.cus = QIcon(".assets/edit.png")
            self.EditButton = QPushButton(self.cus, "")
            self.EditButton.setMaximumSize(20, 30)


            # Create the main layout containing the elements to place in GroupBox
            self.GenHBox = QHBoxLayout()

            # Sub layout for Check button and text
            self.LeftH = QHBoxLayout()
            self.LeftH.addWidget(self.CheckButton)
            self.LeftH.addWidget(self.le_text)
            
            self.LeftH.setAlignment(Qt.AlignVCenter)
            
            # Sub layout for delete button
            self.RightH = QHBoxLayout()
            self.RightH.addWidget(self.EditButton)
            self.RightH.addWidget(self.DeleteButton)

            # Add these layouts to main layout
            self.GenHBox.addLayout(self.LeftH)
            self.GenHBox.addLayout(self.RightH)

            # Set layout of group Box
            self.GroupBox.setLayout(self.GenHBox)
            
            self.GroupBox.setMaximumHeight(recommanded_height + 50)

            # self.GroupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
            self.done = False

            # Date of task management:
            if date == None:
                now = datetime.now()
                self.date = now.strftime("%d/%m/%Y %H:%M:%S")
            else:
                self.date = date
            
            self.attributes = [self.GroupBox, self.GenHBox, self.LeftH, self.CheckButton, self.le_text, self.RightH, self.DeleteButton]

        def manage_text_size(self):
            words = self.task_text.split(" ")
            for i in range(len(words)):
                word = words[i]
                
                
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDQuicker")

        self.setup_ui()
        self.__init_tasks__()

    # ========= Initial UI =========
    def setup_ui(self): 
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.modify_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        # Add Task Bar:
        self.ip_add = QLineEdit()

        # main widget for scrollable uses
        self.main_widget = QWidget()


        # Add Clear All button: 
        self.btn_clearDone = QPushButton(icon=QIcon(".assets/bin.png"), text="Done") 
        self.btn_clearNotDone = QPushButton(icon=QIcon(".assets/bin.png"), text="To Do") 

        # Label for Tasks
        self.lb_tasks = QLabel(text="To Do Tasks:")

        # Label for DoneTasks
        self.lb_doneTasks = QLabel(text="Done Tasks:")

    def modify_widgets(self):
        # Add Task Bar:
        self.ip_add.setPlaceholderText("Add Task")
        self.ip_add.setMinimumHeight(30)

        # Rule for To DO tasks Label:
        size_policy = QSizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Fixed)

        self.lb_tasks.setSizePolicy(size_policy)


    def create_layouts(self):
        # Main layout: 
        self.main_layout = QVBoxLayout(self)

        # Tasks layout:
        self.tasks_layout = QVBoxLayout()

        # Done Tasks layout:
        self.doneTasks_layout = QVBoxLayout()

        # Clear layout:
        self.clear_layout = QHBoxLayout()

        # Create the scrollable widget and layout
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_area = QScrollArea(widgetResizable=True) 
        

    def modify_layouts(self):
        self.resize(350, 500)
        self.setMaximumSize(500, 800)
        self.setMinimumSize(300, 300)
        self.main_layout.setSpacing(0)

    def add_widgets_to_layouts(self):
        # main layout disposition: 
        self.main_layout.addWidget(self.ip_add) 

        # ---- Scrollable Widget: 

        
        self.scroll_widget.setLayout(self.scroll_layout)
        

        # Add the two layouts to the scrollable layout
        self.scroll_layout.addLayout(self.tasks_layout, 0)
        self.scroll_layout.addLayout(self.doneTasks_layout)

        
        self.scroll_area.setWidget(self.scroll_widget)

        size_policy = QSizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Expanding)
        size_policy.setHorizontalPolicy(QSizePolicy.Expanding)
        # size_policy.setVerticalStretch(100)

        self.scroll_area.setSizePolicy(size_policy)
        self.scroll_area.setAlignment(Qt.AlignAbsolute)
        self.main_layout.addWidget(self.scroll_area)

        # ---- 

        # Add tasks label
        self.tasks_layout.addWidget(self.lb_tasks)
        # Add done tasks label
        self.doneTasks_layout.addWidget(self.lb_doneTasks) 

        self.clear_layout.addWidget(self.btn_clearDone)
        self.clear_layout.addSpacing(20)
        self.clear_layout.addWidget(self.btn_clearNotDone)

        self.main_layout.addLayout(self.clear_layout)
        
    def setup_connections(self):
        self.ip_add.returnPressed.connect(self.add_task)
        self.btn_clearDone.pressed.connect(partial(self.clear_tasks, True))
        self.btn_clearNotDone.pressed.connect(partial(self.clear_tasks, False))
    
    # ========= Tasks Addition =========

    def __init_tasks__(self):
        self.tasks = self.load_tasks()
    
    def add_task(self):
        # get task_text
        task_text = self.ip_add.text()

        if task_text in self.tasks or task_text == "": # case of not adding the task
            return
        else:
            self.ip_add.clear()

        # Create instance of task and its widgets / layouts
        task = self.Task(task_text)
        
        # Setup connections 
        task.CheckButton.pressed.connect(partial(self.task_checked, task_text))

        task.DeleteButton.pressed.connect(partial(self.task_delete, task_text))

        # Add task to tasks_layout
        self.tasks_layout.addWidget(task.GroupBox)

        # Keep task in memory
        self.tasks[task_text] = task # within ram
        save_task(task_text, task.date)  # within storage 

    def task_checked(self, task_text, from_save=False):
        checked_task = self.tasks[task_text] # get instance that was checked
        if not from_save:
            checked_task.CheckButton.setChecked(True)
            time.sleep(0.2) # better user experience
        
        if checked_task.done == False:
            checked_task.done = True
            checked_task.CheckButton.setStyleSheet("color:green;") # apply style 
            checked_task.le_text.setStyleSheet("text-decoration: line-through;")
        else:
            checked_task.done = False
            checked_task.CheckButton.setStyleSheet("color: white;") # apply style
            checked_task.le_text.setStyleSheet("text-decoration: none;")
        self.move_task(task_text, from_save)
    
    def task_delete(self, task_text: str):
        to_delete_task = self.tasks[task_text] # get instance of Task
        if to_delete_task.done: # remove group widget of the good layout
            self.doneTasks_layout.removeWidget(to_delete_task.GroupBox)
        else:
            self.tasks_layout.removeWidget(to_delete_task.GroupBox)

        delete_task(task_text, to_delete_task.done) # delete the task from memory

        for elem in to_delete_task.attributes:
            elem.deleteLater() # force delete elements of memory 

        del self.tasks[task_text] # delete the task from the memory 

    def clear_tasks(self, done: bool):
        # delete task with given done state (True or False) 

        # Pop Up Warning
        action = "delete all tasks marked as 'done tasks'" if done else "delete all tasks marked as 'not done'"
        
        reply = QMessageBox.question(self, "Warning", f"Are you sure you want to {action}?", 
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    )
        if reply != QMessageBox.Yes:
            return

        # Delete specified task: 
        deleted = []
        for task_text in self.tasks.keys():
            if self.tasks[task_text].done == done:
                delete_task(task_text, done)
                deleted.append(task_text)
                for elem in self.tasks[task_text].attributes:
                    elem.deleteLater()
        
        for task_text in deleted: # remove removed task from self.tasks
            del self.tasks[task_text]
        del deleted
        
    def move_task(self, task_text: str, from_save: bool =None):
        GroupBox = self.tasks[task_text].GroupBox # get widget to move 
        if self.tasks[task_text].done: # move group to done task layout
            if not from_save: # so we don't do useless / error making operations 
                move_saved_task(task_text, True) # Manage task saving
                self.tasks_layout.removeWidget(GroupBox)

            self.doneTasks_layout.addWidget(GroupBox) # add to new state layout
            self.tasks[task_text].CheckButton.setChecked(True) # set check state of button 

        else: # move group to not done task layout
            if not from_save: # so we don't do useless / error making operations 
                move_saved_task(task_text, False) # Manage task saving
                self.doneTasks_layout.removeWidget(GroupBox)

            self.tasks_layout.addWidget(GroupBox) # add to new state layout
            self.tasks[task_text].CheckButton.setChecked(False) # set check state of button 

    # ========= Tasks Loading =========

    def load_tasks(self):
        loaded = load_content() # get saved tasks
        self.tasks = {}
        for state in loaded.keys(): # todo and done task
            # {state: {task_name: date}}
            for task_name, date in loaded[state].items():
                task = self.Task(task_name, date) # create instance and widgets
                self.tasks[task_name] = task # keep it in memory 

                # We set it to the opposite, and then simulate a check action on it
                task.done = False if state == "done" else True 
                self.task_checked(task_name, True) # we clarify the situation with the 'from_save' set to true, so that it knows it doesnt have to change values in the storage and remove it from the initial layout. 

                # Set connections 
                task.CheckButton.pressed.connect(partial(self.task_checked, task_name))
                task.DeleteButton.pressed.connect(partial(self.task_delete, task_name))

                

        return self.tasks 

                
        



if __name__ == "__main__":
    app = QApplication()
    with open(".assets/style.css", 'r') as file:
        app.setStyleSheet(file.read())

    main_window = TDQuicker()
    main_window.show()

    app.exec()
