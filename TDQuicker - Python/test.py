# Code créé par GaecKo

from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QTextEdit, QVBoxLayout, QPushButton, QWidget, QApplication, QListWidget, QLineEdit, QSplitter, QCheckBox, QLabel, QGroupBox, QFrame, QMessageBox, QStyle, QScrollArea
from PySide6.QtGui import QIcon



from functools import partial

class TDQuicker(QWidget):
    class Task:
        # Used to 
        def __init__(self, task_text):
            self.task_text = task_text
            self.create_task()

        def create_task(self): 
            # Create the QGroupBox and set its style sheet
            self.GroupBox = QGroupBox()
            # Create the QCheckBox and QPushButton widgets
            self.CheckButton = QCheckBox(self.task_text)

            self.icon = QIcon(".assets/bin.png")
            self.DeleteButton = QPushButton(self.icon, "")
            self.DeleteButton.setMaximumSize(25, 25)

            # Create the main layout containing the elements to place in GroupBox
            self.GenHBox = QHBoxLayout()

            # Sub layout for Buttons
            self.LeftH = QHBoxLayout()
            self.LeftH.addWidget(self.CheckButton)

            self.RightH = QHBoxLayout()
            self.RightH.addWidget(self.DeleteButton)

            # Add these layouts to main layout
            self.GenHBox.addLayout(self.LeftH)
            self.GenHBox.addLayout(self.RightH)

            # Set layout of group Box
            self.GroupBox.setLayout(self.GenHBox)

            self.done = False
            self.attributes = [self.GroupBox, self.GenHBox, self.LeftH, self.icon, self.CheckButton, self.RightH, self.DeleteButton]

    # def show(self):
    #     self.main_widget.show()

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


    def create_layouts(self):
        # Main layout: 
        self.main_layout = QVBoxLayout(self)

        # Tasks layout:
        self.tasks_layout = QVBoxLayout()

        # Done Tasks layout:
        self.doneTasks_layout = QVBoxLayout()

        # Clear layout:
        self.clear_layout = QHBoxLayout()
        

    def modify_layouts(self):
        self.resize(250, 500)
        self.main_layout.setSpacing(0)

    def add_widgets_to_layouts(self):
        # main layout disposition: 
        self.main_layout.addWidget(self.ip_add) 
        self.main_layout.addSpacing(10)

        # ---- Scrollable Widget: 

        # Create the scrollable widget and layout
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        

        # Add the two layouts to the scrollable layout
        self.scroll_layout.addLayout(self.tasks_layout, 0)
        self.scroll_layout.addLayout(self.doneTasks_layout)
        

        self.scroll_area = QScrollArea(widgetResizable=True)
        self.scroll_area.setWidget(self.scroll_widget)

        size_policy = QSizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Expanding)
        size_policy.setHorizontalPolicy(QSizePolicy.Expanding)
        size_policy.setVerticalStretch(100)

        self.scroll_area.setSizePolicy(size_policy)
        self.main_layout.addWidget(self.scroll_area)

        # ---- 

        # Add tasks label
        self.tasks_layout.addWidget(self.lb_tasks)
        # Add done tasks label
        self.doneTasks_layout.addWidget(self.lb_doneTasks) 

        self.main_layout.addStretch()

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
        self.tasks = {}
    
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

        # Keep task in "memory"
        self.tasks[task.task_text] = task 
    
    def task_checked(self, task_text):
        checked_task = self.tasks[task_text]
        if checked_task.done == False:
            checked_task.done = True
            checked_task.CheckButton.setStyleSheet("""text-decoration: line-through; color: green; """)
        else:
            checked_task.done = False
            checked_task.CheckButton.setStyleSheet("")
        self.move_task(task_text)
    
    def task_delete(self, task_text):
        to_delete_task = self.tasks[task_text]
        for elem in to_delete_task.attributes:
            elem.deleteLater()
        del self.tasks[task_text]

    def clear_tasks(self, done):
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
                deleted.append(task_text)
                for elem in self.tasks[task_text].attributes:
                    elem.deleteLater()
        
        for task_text in deleted: # remove removed task from self.tasks
            del self.tasks[task_text]
        del deleted
        

    def move_task(self, task_text):
        if self.tasks[task_text].done: # move group to done task layout
            GroupBox = self.tasks[task_text].GroupBox
            self.tasks_layout.removeWidget(GroupBox)
            self.doneTasks_layout.addWidget(GroupBox)
            self.tasks[task_text].CheckButton.setChecked(True) # set check state of button 

        else: # move group to not task layout
            GroupBox = self.tasks[task_text].GroupBox
            self.doneTasks_layout.removeWidget(GroupBox)
            self.tasks_layout.addWidget(GroupBox)
            self.tasks[task_text].CheckButton.setChecked(False) # set check state of button 

if __name__ == "__main__":
    app = QApplication()
    with open(".assets/style.css", 'r') as file:
        app.setStyleSheet(file.read())

    main_window = TDQuicker()
    main_window.show()

    app.exec()
