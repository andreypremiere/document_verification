from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QCursor, QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QPushButton

from fonts.getting_font import get_font
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
        # self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.setContentsMargins(8, 4, 8, 4)
        self.main_layout.setSpacing(0)

        self.tasks_panel = QHBoxLayout(self)
        self.tasks_panel.setContentsMargins(0, 0, 0, 0)
        self.tasks_panel.setSpacing(4)
        self.tasks_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)


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

        self.tasks_panel.addWidget(self.button_generating_task)

        # Кнопка выполнения
        self.button_panel = QHBoxLayout(self)
        self.button_panel.setContentsMargins(0, 0, 0, 0)
        self.button_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_perform = QPushButton('Выполнить', self)
        self.button_perform.setStyleSheet("""
            QPushButton {
                background-color: #B8FFB3;
                border-radius: 8px;
                padding: 4px 12px;
                border: none;
            }
            
            QPushButton:hover {
                background-color: #96FF8F;
            }
        """)
        # self.button_perform.setContentsMargins(12, 2, 12, 2)
        self.button_perform.setFont(QFont(get_font('Noto Sans'), 12, 400))
        self.button_perform.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.button_panel.addWidget(self.button_perform)


        self.main_layout.addLayout(self.tasks_panel)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.button_panel)


    def add_task(self):
        self.dialog_window = TaskModal(self, self.parent, 1)
        self.dialog_window.show()

        task_frame = TaskFrame(self)
        self.tasks_panel.insertWidget(-2, task_frame)



