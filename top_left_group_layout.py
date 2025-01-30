from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHBoxLayout, QPushButton
from fonts.getting_font import get_font


class TopLeftGroupLayout:
    """
    Левая панель управления вкладками в верхнем виджете.
    """
    def __init__(self, parent=None):
        self.button_2 = None
        self.button_1 = None
        self.main_layout = QHBoxLayout(parent if parent is not None else None)
        self.init_ui(parent)

    def init_ui(self, parent):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(8)

        self.button_1 = self.generateButton('Main', parent)
        self.button_2 = self.generateButton('Path 1', parent)

        self.main_layout.addWidget(self.button_1)
        self.main_layout.addWidget(self.button_2)

    def generateButton(self, name, parent):
        button = QPushButton(name, parent)
        button.setContentsMargins(0, 0, 0, 0)
        button.setStyleSheet("""
            QPushButton {
                border: 1px solid #7E7E7E;
                border-radius: 12px;
            }

            QPushButton:hover {
                background-color: #EAFFD5;
            }

            QPushButton:pressed {
                background-color: #DAFFB5;
            }
                """)

        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFixedWidth(100)
        button.setFixedHeight(30)

        font_family = get_font('Noto Sans')
        if font_family:
            print(f"Шрифт загружен: {font_family}")
            button.setFont(QFont(font_family, 11, 400))
        else:
            print("Не удалось загрузить шрифт, используется стандартный.")
            button.setFont(QFont("Arial", 11, 400))

        return button
