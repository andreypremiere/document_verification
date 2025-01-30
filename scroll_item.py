from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtWidgets import QFrame, QSizePolicy, QHBoxLayout, QLabel, QScrollArea, QCheckBox, QGraphicsDropShadowEffect
from fonts.getting_font import get_font


class ScrollItem(QFrame):
    """
    Элемент, представляющий файл в боковой верхней панели.
    """
    def __init__(self, count, parent, file_name, path):
        super().__init__()
        self.index = count
        self.parent = parent
        self.checkbox = None
        self.path = path
        self.file_name = file_name
        self.state_selected = False
        self.init_ui(count)

    def init_ui(self, count):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet('background-color: #F7F7F7; border-radius: 3px;')
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setContentsMargins(6, 2, 6, 2)
        self.main_layout.setSpacing(6)

        text_style = QFont(get_font('Noto Sans'), 8, 400)

        self.serial_number = QLabel(f'{count + 1}. ', self)
        self.serial_number.setFont(text_style)
        self.name_file = QLabel(f'{self.file_name}')

        self.name_file.setFont(text_style)
        self.name_file.setWordWrap(False)  # Отключаем перенос текста

        self.scroll_for_name = QScrollArea(self)
        self.scroll_for_name.setMinimumWidth(50)
        self.scroll_for_name.setContentsMargins(0, 0, 0, 0)
        self.scroll_for_name.setWidget(self.name_file)
        self.scroll_for_name.setWidgetResizable(True)  # Виджет внутри будет автоматически изменять размер
        self.scroll_for_name.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar {
                width: 0px;
                height: 0px;
            }
        """)

        self.checkbox = QCheckBox('', parent=self)
        self.checkbox.setContentsMargins(0, 0, 0, 0)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                background-color: transparent;    
                padding: 0px;        
            }

            QCheckBox::indicator {
                width: 12px;
                height: 12px;
                border-radius: 3px;  /* Скругление */
                border: none;  /* Цвет границы */
                background-color: #FFFFFF;  /* Фон */
                margin: 0px;
                padding: 3px;
            }

            QCheckBox::indicator:checked {
                image: url('icons/Ellipse_checked.svg');  /* Свой значок отметки */
                width: 8px;
                height: 8px;
            }

            QCheckBox::indicator:unchecked {
                background-color: #FFFFFF;  /* Фон в выключенном состоянии */
                width: 8px;
                height: 8px;
            }
        """)
        self.checkbox.setChecked(False)
        self.checkbox.setGraphicsEffect(
            QGraphicsDropShadowEffect(blurRadius=4, offset=QPointF(0, 0), color=QColor(0, 0, 0, 48)))

        self.main_layout.addWidget(self.serial_number)
        self.main_layout.addWidget(self.scroll_for_name)
        self.main_layout.addWidget(self.checkbox)

    def mousePressEvent(self, event):
        """Обрабатываем клик по фрейму."""
        if event.modifiers() != Qt.KeyboardModifier.ShiftModifier and self.parent.selected_element_index != self.index:
            if self.parent.selected_element_index is not None:
                self.parent.widget_layout1.itemAt(self.parent.selected_element_index).widget().setStyleSheet(
                    """
                    QFrame {
                        background-color: #F7F7F7;
                        outline: none;
                        border-radius: 0px;
                    }
                    """
                )

            self.setStyleSheet("""
                    QFrame {
                        background-color: #C0C0C0;
                        }
                    """)
            self.parent.selected_element_index = self.index
            self.parent.open_pdf_file(self.index)
            self.parent.set_image()

        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            range_list = range(self.parent.selected_element_index,
                               self.index + 1) if self.index > self.parent.selected_element_index else reversed(
                range(self.index, self.parent.selected_element_index + 1))
            print(range_list)
            for i in range_list:
                self.parent.widget_layout1.itemAt(i).widget().checkbox.toggle()
                print('состояние переключено')

        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Обрабатываем событие наведения мыши."""
        if self.parent.selected_element_index != self.index:
            self.setStyleSheet("""
            QFrame {
                background-color: #E3E3E3;
                outline: 1px solid black;
                border-radius: 4px;
                }
            """)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Меняем курсор
        super().enterEvent(event)  # Вызов родительского метода

    def leaveEvent(self, event):
        """Обрабатываем событие ухода мыши."""
        if self.parent.selected_element_index != self.index:
            self.setStyleSheet("""
                QFrame {
                    background-color: #F7F7F7;
                    outline: none;
                    border-radius: 0px;
                }
            """)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))  # Возвращаем стандартный курсор
        super().leaveEvent(event)  # Вызов родительского метода
