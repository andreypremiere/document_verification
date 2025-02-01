from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
import sys

from fonts.getting_font import get_font


class TaskModal(QDialog):
    def __init__(self, parent=None, managing_class=None, number_task=None):
        super().__init__()
        self.managing_class = managing_class
        self.number_task = number_task

        self.all_widgets = []
        self.all_rectangles_of_widgets = []
        # [{0: [{'index': 0, 'rect': PyQt6.QtCore.QRectF(1397.1641421270663, 915.2718801434254, 701.8162473184568, 54.980996333703956), 'group': <PyQt6.QtWidgets.QGraphicsItemGroup object at 0x0000014C8F4884B0>, 'color': (185, 85, 45)}, {'index': 1, 'rect': PyQt6.QtCore.QRectF(1638.5466338274875, 1442.6457577720932, 113.23750061005444, 53.22162528672561), 'group': <PyQt6.QtWidgets.QGraphicsItemGroup object at 0x0000014C94006530>, 'color': (6, 109, 212)}]}, {0: [{'index': 0, 'rect': PyQt6.QtCore.QRectF(578.003376295639, 900.4684178079428, 1110.374907094254, 146.02190559047722), 'group': <PyQt6.QtWidgets.QGraphicsItemGroup object at 0x0000014C9400DD10>, 'color': (205, 61, 22)}, {'index': 1, 'rect': PyQt6.QtCore.QRectF(289.0016881478195, 1384.1659800763987, 258.5804578164701, 94.30581402718326), 'group': <PyQt6.QtWidgets.QGraphicsItemGroup object at 0x0000014C9400D6D0>, 'color': (65, 18, 218)}]}]

        for i in range(self.managing_class.stacked_widget.count()):
            self.all_widgets.append(self.managing_class.stacked_widget.widget(i))

        for i in range(len(self.all_widgets)):
            self.all_rectangles_of_widgets.append(self.all_widgets[i].right_panel.middle_panel.rectangles)

        print(self.all_rectangles_of_widgets)

        self.init_ui()

    def init_ui(self):
        self.resize(400, 300)
        self.setWindowTitle('Окно задачи')

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.label = QLabel(f'Задача {self.number_task}', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label.setFont(QFont(get_font('Noto Sans'), 12, 400))
        self.label.setContentsMargins(0, 6, 0, 6)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            border: none;
        """)
        self.frame_area = QFrame(self.scroll_area)
        self.frame_layout = QVBoxLayout(self.frame_area)
        self.frame_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.frame_layout.setContentsMargins(2, 2, 2, 2)
        self.frame_layout.setSpacing(2)

        self.scroll_area.setWidget(self.frame_area)


        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.scroll_area)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialog = TaskModal()
#     dialog.exec()  # Запуск окна в модальном режиме
