# Author: Arthur De Neyer (GaecKo)
# Date: 06/03/2023
# GitHub: https://github.com/GaecKo/TDQuicker 

from PySide6.QtWidgets import QHBoxLayout, QSizePolicy, QTextEdit, QVBoxLayout, QPushButton, QWidget, QApplication, QLineEdit, QCheckBox, QLabel, QGroupBox, QMessageBox, QScrollArea, QProgressBar
from PySide6.QtGui import QIcon, QTextOption
from PySide6.QtCore import Qt, QSize, QPropertyAnimation

from datetime import datetime
from data.data import * 
import time
import re


from functools import partial

class ProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()

    def update_value(self, value, animated=True):
        if animated:
            if hasattr(self, "animation"):
                self.animation.stop()
            else:
                self.animation = QPropertyAnimation(
                    targetObject=self, propertyName=b"value"
                )
                self.animation.setDuration(300)
            self.animation.setStartValue(self.value())
            self.animation.setEndValue(value)
            self.animation.start()
        else:
            self.setValue(value)

class TDQuicker(QWidget):

    class Task: # class containing the task itself
        def __init__(self, task_text, date: str =None):
            # task text and initial status
            self.task_text = task_text
            self.done = False

            # Date of task management:
            if date == None:
                now = datetime.now()
                self.date = now.strftime("%d/%m/%Y %H:%M:%S")
            else:
                self.date = date

            # creates task components
            self.create_composers()
            self.create_widgets()
            self.modify_widgets()
            self.add_widgets_to_composers()
            self.refresh_size()

            # list for easier deletion
            self.attributes = [self.GroupBox, self.GenHBox, self.LeftH, self.CheckButton, self.te_text, self.RightH, self.DeleteButton]
            
        def create_composers(self):
            # Create the QGroupBox 
            self.GroupBox = QGroupBox()

            # Create the main layout containing the elements to place in GroupBox
            self.GenHBox = QHBoxLayout()

            # sub layout for repartition
            self.LeftH = QHBoxLayout()
            self.RightH = QHBoxLayout()

        def create_widgets(self):
            # Create the QCheckBox widgets
            self.CheckButton = QCheckBox()

            # Text of the task 
            self.te_text = QTextEdit()
            

            self.cus = QIcon(".assets/edit.png")
            self.EditButton = QPushButton(self.cus, "")

            # Icon and button to delete task
            self.bin = QIcon(".assets/bin.png")
            self.DeleteButton = QPushButton(self.bin, "")
        
        

        def linkify(self, text):
            # Regular expression pattern for matching URLs
            url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

            # Replace URLs with HTML links
            return url_pattern.sub(lambda match: '<a href="{}">{}</a>'.format(match.group(0), match.group(0)), text)


        def modify_widgets(self):
            # Cross task size
            self.CheckButton.setMaximumSize(25, 25)

            # te_text options: 
            # self.te_text.setPlainText(self.task_text)
            self.te_text.setHtml(self.linkify(self.task_text))
            self.te_text.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
            self.te_text.setReadOnly(True)
            self.te_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # hide the vertical scrollbar
            self.te_text.setObjectName("taskText")


            # Buttons size
            self.DeleteButton.setMaximumSize(20, 30)
            self.EditButton.setMaximumSize(20, 30)
        
        def add_widgets_to_composers(self):
            # Sub left layout for Check button and text
            self.LeftH.addWidget(self.CheckButton)
            self.LeftH.addWidget(self.te_text)

            # Sub Right layout for Options button (del and mod)
            self.RightH.addWidget(self.EditButton)
            self.RightH.addWidget(self.DeleteButton)

            # Add these layouts to main layout
            self.GenHBox.addLayout(self.LeftH)
            self.GenHBox.addLayout(self.RightH)

            # Set layout of group Box
            self.GroupBox.setLayout(self.GenHBox)

        def refresh_size(self):
            # refresh size to make the groupbox height correspond to the content heigh

            recommanded_height = int(len(self.task_text) * 0.9)
            self.te_text.setMinimumHeight(recommanded_height)
            self.GroupBox.setMaximumHeight(recommanded_height + 50) 
                
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDQuicker")

        self.__init_ui__()
        self.__init_tasks__()

    # ========= Initial UI =========
    def __init_ui__(self): 
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

        # Progress bar 
        self.progress_bar = ProgressBar()

    def modify_widgets(self):
        # Add Task Bar:
        self.ip_add.setPlaceholderText("Add Task")
        self.ip_add.setMinimumHeight(40)

        # Rule for To DO tasks Label:
        size_policy = QSizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Fixed)

        self.lb_tasks.setSizePolicy(size_policy)
        
        self.lb_doneTasks.setSizePolicy(size_policy)

        # value for progress bar:
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

    def create_layouts(self):
        # Main layout: 
        self.main_layout = QVBoxLayout(self)

        # Create the scrollable widget and layout
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_area = QScrollArea(widgetResizable=True) 

        # Tasks layout:
        self.tasks_layout = QVBoxLayout()

        # Done Tasks layout:
        self.doneTasks_layout = QVBoxLayout()

        # Progrosse bar layout:
        self.pb_layout = QHBoxLayout()

        # Clear layout:
        self.clear_layout = QHBoxLayout()

    def modify_layouts(self):
        self.resize(400, 550)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setMaximumSize(500, 800)
        self.setMinimumSize(300, 300)
        # self.main_layout.setSpacing(0)

        self.doneTasks_layout.setAlignment(Qt.AlignTop)

    def add_widgets_to_layouts(self):
        # main layout disposition: 
        self.main_layout.addWidget(self.ip_add) 

        # ---- Scrollable Widget: 

        
        self.scroll_widget.setLayout(self.scroll_layout)
        

        # Add the two layouts to the scrollable layout
        self.scroll_layout.addLayout(self.tasks_layout, 0)

        self.scroll_layout.addSpacing(15)

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

        # Add progress bar to its layout
        self.pb_layout.addWidget(self.progress_bar)

        # Add done tasks label
        self.doneTasks_layout.addWidget(self.lb_doneTasks) 

        self.clear_layout.addWidget(self.btn_clearDone)
        self.clear_layout.addSpacing(20)
        self.clear_layout.addWidget(self.btn_clearNotDone)

        self.main_layout.addLayout(self.pb_layout)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.clear_layout)
        
    def setup_connections(self):
        self.ip_add.returnPressed.connect(self.add_task)
        self.btn_clearDone.pressed.connect(partial(self.clear_tasks, True))
        self.btn_clearNotDone.pressed.connect(partial(self.clear_tasks, False))
    
    # ========= Tasks Addition =========

    def __init_tasks__(self):
        self.tasks = self.load_tasks()

    def add_task(self, task_text: str = None, date: str = None):
        # get task_text
        if task_text == None: # means that we didnt call the function from the load_save
            task_text = self.ip_add.text()

        if task_text in self.tasks or task_text == "" or task_text == len(task_text) * " ": # case of not adding the task
            return
        else:
            self.ip_add.clear()

        # Create instance of task and its widgets / layouts
        task = self.Task(task_text, date)
        
        # Setup connections of the task 
        task.CheckButton.pressed.connect(partial(self.task_checked, task.task_text))

        task.DeleteButton.pressed.connect(partial(self.task_delete, task.task_text))

        task.EditButton.pressed.connect(partial(self.switch_edit_mode, task.task_text))

        task.te_text.keyPressEvent = lambda event: self.update_task_text(task.task_text) if event.key() == Qt.Key_Return else QTextEdit.keyPressEvent(task.te_text, event) 

        # Add task to tasks_layout
        if date == None: # means that we didnt call the function from the load_save
            self.tasks_layout.addWidget(task.GroupBox)
            save_task(task_text, task.date)  # within storage 
            self.refresh_progress_status()

        # Keep task in memory
        self.tasks[task_text] = task # within ram

    def switch_edit_mode(self, task_text):
        task = self.tasks[task_text]
        
        if task.te_text.isReadOnly(): # if it has to be editable
            task.te_text.setReadOnly(False)
            if not task.done:
                task.te_text.setStyleSheet("border: 2px white; border-style: none none solid none; ")
            else:
                task.te_text.setStyleSheet("border: 2px white; border-style: none none solid none; text-decoration: line-through;")

            task.EditButton.setStyleSheet("border: 2px white; border-style: none none solid none; ")
            task.EditButton.setIcon(QIcon(".assets/back.svg"))
        else:
            task.te_text.setReadOnly(True) # if it has to be only readable
            task.EditButton.setStyleSheet("border: none; border-style: none;")
            task.EditButton.setIcon(QIcon(".assets/edit.png"))
            if task.te_text.toPlainText() != task_text:
                task.te_text.setText(task_text)

            if task.done:
                task.te_text.setStyleSheet("border: none; border-style: none; text-decoration: line-through;")
            else:
                task.te_text.setStyleSheet("border: none; border-style: none;")
    
    def update_task_text(self, old_task_text):

        new_text = self.tasks[old_task_text].te_text.toPlainText() # get the new text 
        self.tasks[new_text] = self.tasks.pop(old_task_text)

        task = self.tasks[new_text]
        task.task_text = new_text # refresh the task attributes 
        task.refresh_size()

        self.refresh_saved_task(old_task_text, new_text)
        self.refresh_task_connections(new_text)
        self.switch_edit_mode(new_text)

    def refresh_task_connections(self, task_text):
        task = self.tasks[task_text]
        
        # Refresh connections if task name was changed
        task.CheckButton.pressed.disconnect()
        task.CheckButton.pressed.connect(partial(self.task_checked, task_text))

        task.DeleteButton.pressed.disconnect()
        task.DeleteButton.pressed.connect(partial(self.task_delete, task_text))

        task.EditButton.pressed.disconnect()
        task.EditButton.pressed.connect(partial(self.switch_edit_mode, task_text))


        task.te_text.keyPressEvent = lambda event: self.update_task_text(task_text) if event.key() == Qt.Key_Return else QTextEdit.keyPressEvent(task.te_text, event) 

    def task_checked(self, task_text, from_save=False):
        checked_task = self.tasks[task_text] # get instance that was checked
        if not from_save:
            checked_task.CheckButton.setChecked(True)
            time.sleep(0.2) # better user experience
            
        if checked_task.done == False:
            checked_task.done = True
            checked_task.CheckButton.setStyleSheet("color:#2d7121;") # apply style 
            checked_task.te_text.setStyleSheet("text-decoration: line-through;")
        else:
            checked_task.done = False
            checked_task.CheckButton.setStyleSheet("color: white;") # apply style
            checked_task.te_text.setStyleSheet("text-decoration: none;")
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
        self.refresh_progress_status()

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

            self.doneTasks_layout.addWidget(GroupBox) # add to new state layout
            self.tasks[task_text].CheckButton.setChecked(True) # set check state of button 
            if not from_save: # so we don't do useless / error making operations 
                move_saved_task(task_text, True) # Manage task saving
                self.tasks_layout.removeWidget(GroupBox)
                self.refresh_progress_status()

        else: # move group to not done task layout

            self.tasks_layout.addWidget(GroupBox) # add to new state layout
            self.tasks[task_text].CheckButton.setChecked(False) # set check state of button 
            if not from_save: # so we don't do useless / error making operations 
                move_saved_task(task_text, False) # Manage task saving
                self.doneTasks_layout.removeWidget(GroupBox)
                self.refresh_progress_status()

    # ========= Tasks Loading / Saving =========

    def refresh_saved_task(self, old_text, new_text):
        delete_task(old_text, self.tasks[new_text].done)
        save_task(new_text, self.tasks[new_text].date, self.tasks[new_text].done)
        
    def load_tasks(self):
        loaded = load_content() # get saved tasks
        self.tasks = {}
        for state in loaded.keys(): # todo and done task
            # {state: {task_name: date}}
            for task_name, date in loaded[state].items():

                self.add_task(task_name, date) # we call the function specifying elements so that it knows we're adding saved tasks. 

                task = self.tasks[task_name] # get instance that was just created

                # We set it to the opposite, and then simulate a check action on it
                task.done = False if state == "done" else True 
                self.task_checked(task_name, True) # we clarify the situation with the 'from_save' set to true, so that it knows it doesnt have to change values in the storage and remove it from the initial layout. 

        self.refresh_progress_status()
        return self.tasks 

    # ========= Progress Status =========
    def refresh_progress_status(self):
        done = self.doneTasks_layout.count() - 1
        todo = self.tasks_layout.count() - 1

        total = done + todo
        
        self.lb_tasks.setText(f"To Do Tasks ({todo}):")
        self.lb_doneTasks.setText(f"Done Tasks ({done}):")

        percentage = (done / max(total, 1) * 100)
        self.progress_bar.update_value(percentage)

        if percentage == 100:
            self.progress_bar.setStyleSheet("""QProgressBar::chunk{background-color: #2d7121;}""")
        else:
            self.progress_bar.setStyleSheet("""QProgressBar::chunk{background-color: #394359;}""")


if __name__ == "__main__":
    app = QApplication()
    app_icon = QIcon(".assets/WIcon.svg")
    app.setWindowIcon(app_icon)
    with open(".assets/style.css", 'r') as file:
        app.setStyleSheet(file.read())

    main_window = TDQuicker()
    main_window.show()

    app.exec()
