from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect

from fonts.getting_font import get_font


class ItemRect(QFrame):
    def __init__(self, parent, rect):
        super().__init__(parent=parent)

        self.index = rect['index']
        self.color = rect['color']

        self.setStyleSheet(f"""
            background-color: {self.rgb_to_hex(*self.color)};
            border-radius: 4px;
            border: none;
        """)
        self.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=4, xOffset=0, yOffset=0, color=QColor(0, 0, 0, 64)))


        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(4, 2, 4, 2)
        self.layout.setSpacing(2)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(f'{self.index + 1}', self)
        self.label.setFont(QFont(get_font('Noto Sans'), 10, 600))

        self.button_delete = QPushButton()
        self.button_delete.setStyleSheet("""
            background-color: white;
            border-radius: 6px;
        """)
        self.button_delete.setIcon(QIcon("icons/Icon delete.svg"))
        self.button_delete.setIconSize(QSize(18, 18))

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button_delete)

    def rgb_to_hex(self, r, g, b):
        return "#{:02X}{:02X}{:02X}".format(r, g, b)


class SubTopPanel(QFrame):
    """
    Класс, где отображается информация о странице (прямоугольники и количество).
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent

        self.init_ui()

    def init_ui(self):
        # self.setFixedHeight(40)
        self.setStyleSheet('background-color: transparent;')

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(4)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        self.current_page = QLabel(f'Страница - x', self)
        self.current_page.setStyleSheet('border: none;')
        self.current_page.setFont(QFont(get_font('Noto Sans'), 10, 400))
        self.main_layout.addWidget(self.current_page)
        self.main_layout.addSpacing(20)

        self.one_frame = self.generate_frame_icon({'index': 0, 'color': (236, 255, 245)})

    def set_current_page(self, index):
        self.current_page.setText(f'Страница - {index + 1}')

    def generate_frame_icon(self, rect):
         self.main_layout.addWidget(ItemRect(self, rect))

