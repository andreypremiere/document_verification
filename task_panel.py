from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QColor, QCursor
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QGraphicsEffect, QGraphicsDropShadowEffect

from fonts.getting_font import get_font


class TaskPanel(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.init_ui()

    def init_ui(self):
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(4)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            border: 1px solid #7E7E7E;
            border-radius: 12px;
        """)

        self.label = QLabel('Задача 1', self)
        self.label.setFont(QFont(get_font('Noto Sans'), 12, 400))
        self.label.setStyleSheet('border: none;')

        self.delete_button = QPushButton(self)
        self.delete_button.setIcon(QIcon('icons/IconDonedelete.svg'))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=0, color=QColor(0, 0, 0, 64)))
        self.delete_button.setStyleSheet('border: none;')


        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.delete_button)



