from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QStyledItemDelegate, QComboBox, QHBoxLayout

from fonts.getting_font import get_font


class TopRightGroupLayout:
    """
    Правая панель управления вкладками в верхнем виджете.
    """
    def __init__(self, parent=None):
        self.button = None
        self.combo_box = None
        self.main_layout = QHBoxLayout(parent if parent is not None else None)
        self.init_ui(parent)

    def init_ui(self, parent):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(8)

        font_family = get_font('Noto Sans')

        self.combo_box = QComboBox(parent)
        self.combo_box.setFont(QFont(font_family, 11, 400))
        self.combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self.combo_box.setFixedHeight(30)
        self.combo_box.addItems(["auto", "manual"])
        self.combo_box.view().setItemDelegate(QStyledItemDelegate(parent))
        self.combo_box.setStyleSheet("""
                    QComboBox {
                        border: 1px solid #7E7E7E;
                        border-radius: 12px;
                        background-color: #FBFBFB;
                        padding-left: 12px;
                    }

                    QComboBox::drop-down {
                        border: none;
                        background: #FBFBFB;
                        margin-right: 12px;
                    }

                    QComboBox::down-arrow {
                        image: url('icons/icon-arrow.svg');
                        width: 14px;
                        height: 14px;
                        padding: 10px;
                    }

                    QComboBox QAbstractItemView {
                        border: 1px solid #7E7E7E;  /* Граница выпадающего списка */
                        border-radius: 12px;
                        padding: 8px;
                        background-color: #FBFBFB;  /* Фон выпадающего списка */
                        spacing: 8px;
                        selection-background-color: #D3D3D3;  /* Цвет выделения */
                        selection-color: #000000;  /* Цвет текста выделенного элемента */
                        spacing: 8px;
                        }
                """)

        self.main_layout.addWidget(self.combo_box)

        self.button = QPushButton('Сессия', parent)
        self.button.setContentsMargins(0, 0, 0, 0)
        self.button.setStyleSheet("""
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

        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setFixedWidth(100)
        self.button.setFixedHeight(30)
        self.button.setFont(QFont(font_family, 11, 400))

        self.main_layout.addWidget(self.button)
