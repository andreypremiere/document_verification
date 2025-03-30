from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QHBoxLayout, \
    QGraphicsDropShadowEffect, QCheckBox, QComboBox
import sys

from fonts.getting_font import get_font


class RowItem(QHBoxLayout):
    def __init__(self, parent, main_item, rectangles):
        super().__init__()
        self.parent = parent
        self.main_item = main_item
        self.rectangles = rectangles
        self.final_task = []
        self.remains_rectangles = []

        # self.rectangles[0].remove(self.main_item)

        self.init_ui()

    def init_ui(self):
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setContentsMargins(2, 2, 2, 2)
        self.setSpacing(2)

        self.label = QLabel(f"Main #{self.main_item['index'] + 1}", self.parent)
        self.label.setFont(QFont(get_font('Nono Sans'), 12, 600))
        self.label.setStyleSheet("""
            background-color: rgba({}, {}, {}, 32);
            border: none;
            border-radius: 6px;
            padding: 4px 10px;
        """.format(*self.main_item['color']))

        self.label.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=8, xOffset=0, yOffset=0, color=QColor(0, 0, 0, 64)))

        self.checkbox_layout = QHBoxLayout(self.parent)
        self.checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.checkbox_layout.setContentsMargins(0, 0, 0, 0)
        self.checkbox_layout.setSpacing(2)

        self.addWidget(self.label)
        self.addLayout(self.checkbox_layout)
        self.generate_new_checkbox()

    def generate_new_checkbox(self):
        """
        Генерирует новый чекбокс, если другой заполнен.
        :return: chechbox из оставшихся значений.
        """

        checkbox = QComboBox(self.parent)
        res_list = []
        count = 0

        for sublist in self.rectangles:
            for item in sublist:
                if count == 0:
                    res_list.append(f"Main  #{item['index'] + 1}")
                if count >= 1:
                    res_list.append(f"Path {count} #{item['index'] + 1}")
            count += 1

        print(f'main_item: {self.main_item}, \nres_list: {res_list}')
        checkbox.addItems(['Выберите'] + res_list)
        self.checkbox_layout.addWidget(checkbox)

    def get_task(self):
        """
        Возвращает готовые задачи для main_item в final_task.
        :return: final_task.
        """
        index_rectangles = []

        for i in range(self.checkbox_layout.count()):
            widget = self.checkbox_layout.itemAt(i).widget()
            index_checkbox = widget.currentIndex()
            if index_checkbox != 0:
                value = widget.itemData() - 1
                index_rectangles.append(value)

        for i in index_rectangles:
            for j in self.rectangles:
                if j['index'] == i:
                    self.final_task.append(j)


class TaskModal(QDialog):
    def __init__(self, parent=None, managing_class=None, number_task=None):
        super().__init__()
        self.managing_class = managing_class
        self.number_task = number_task

        self.all_widgets = []
        self.all_rectangles_of_widgets = []

        for i in range(self.managing_class.stacked_widget.count()):
            self.all_widgets.append(self.managing_class.stacked_widget.widget(i))

        for i in range(len(self.all_widgets)):
            self.all_rectangles_of_widgets.append(self.all_widgets[i].right_panel.middle_panel.rectangles.copy())

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

        # формируем строку для каждого значения окна main
        for i in self.all_rectangles_of_widgets[0]:
            row = RowItem(self.frame_area, i, self.all_rectangles_of_widgets)
            self.frame_layout.addLayout(row)


    # def generate_row(self):
    #     layout = QHBoxLayout(self.frame_area)
    #     layout.setContentsMargins(0, 0, 0, 0)
    #     layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    #
    #     label = QLabel(f"Main [{item['index'] + 1}]")




