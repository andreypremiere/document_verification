from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QCursor
from PyQt6.QtWidgets import QHBoxLayout, QPushButton
from fonts.getting_font import get_font


class TopLeftGroupLayout:
    """
    Левая панель управления вкладками в верхнем виджете.
    """
    def __init__(self, parent, managing_class):
        self.managing_class = managing_class
        self.parent = parent
        self.button_2 = None
        self.button_1 = None
        self.main_layout = QHBoxLayout(parent if parent is not None else None)
        self.init_ui()

    def init_ui(self):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(8)

        self.button_1 = self.generateButton('Main', self.parent)
        self.button_1.setStyleSheet("""
            QPushButton {
                background-color: #DBEEFF;
                border: 1px solid #7E7E7E;
                border-radius: 12px;
            }
        """)
        self.button_adding = QPushButton(self.parent)
        self.button_adding.setIcon(QIcon('icons/Icon plus.svg'))
        self.button_adding.setIconSize(QSize(24, 24))
        self.button_adding.clicked.connect(self.add_new_path)
        self.button_adding.setStyleSheet("""
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
        self.button_adding.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_adding.setFixedSize(30, 30)

        self.main_layout.addWidget(self.button_1)
        self.main_layout.addWidget(self.button_adding)

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

    def add_new_path(self):
        new_button = self.generateButton(f"Path {self.managing_class.stacked_widget.count()}", self.parent)

        count = self.main_layout.count()
        if count < 2:
            print("Недостаточно виджетов для вставки!")
            return

        index = count - 1  # Предпоследний индекс
        self.main_layout.insertWidget(index, new_button)

        prev_id = self.managing_class.stacked_widget.currentIndex()
        self.managing_class.add_new_path()
        self.change_color_button(prev_id, index)

    def change_color_button(self, prev_index=None, next_index=None):
        prev_widget = self.main_layout.itemAt(prev_index).widget()
        prev_widget.setStyleSheet("""
            QPushButton {
                background-color: none;
                border: 1px solid #7E7E7E;
                border-radius: 12px;
            }
        """)
        next_widget = self.main_layout.itemAt(next_index).widget()
        next_widget.setStyleSheet("""
            background-color: #DBEEFF;
                border: 1px solid #7E7E7E;
                border-radius: 12px;
        """)

