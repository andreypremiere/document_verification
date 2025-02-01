from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton

from task_frame import TaskFrame
from task_modal import TaskModal


class BottomActionPanel(QFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent

        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(44)
        self.setStyleSheet('background-color: transparent;')

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(8)

        self.button_generating_task = QPushButton(self)
        self.button_generating_task.setIcon(QIcon('icons/Icon plus.svg'))
        self.button_generating_task.setIconSize(QSize(30, 30))
        self.button_generating_task.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_generating_task.clicked.connect(self.add_task)
        self.button_generating_task.setStyleSheet("""
            background-color: none;
            border: 1px solid #7E7E7E;
            border-radius: 12px;
        """)

        self.main_layout.addWidget(self.button_generating_task)


    def add_task(self):
        self.dialog_window = TaskModal(self, self.parent, 1)
        self.dialog_window.show()

        task_frame = TaskFrame(self)
        self.main_layout.insertWidget(-2, task_frame)



