import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget

from bottom_action_panel import BottomActionPanel
from top_left_group_layout import TopLeftGroupLayout
from main_splitter import MainSplitter
from top_right_group_layout import TopRightGroupLayout


class MainWindow(QWidget):
    """
    Главный класс, где выполняется сборка всех выджетов и запуск программы.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Окно выполнения")
        self.resize(900, 600)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('background-color: #FBFBFB;')

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(0)

        # Верхняя панель
        self.top_panel_frame = QFrame(self)
        self.top_panel_frame.setStyleSheet('border-bottom: 1px solid #7E7E7E;')
        # self.top_panel_frame.setContentsMargins(0, 0, 0, 0)
        self.top_panel_layout = QHBoxLayout(self.top_panel_frame)
        self.top_panel_layout.setContentsMargins(8, 8, 8, 8)

        self.top_left_group_layout = TopLeftGroupLayout(self.top_panel_frame, self)
        self.top_right_group_layout = TopRightGroupLayout(self.top_panel_frame)

        self.top_panel_layout.addLayout(self.top_left_group_layout.main_layout)
        self.top_panel_layout.addStretch()
        self.top_panel_layout.addLayout(self.top_right_group_layout.main_layout)

        main_layout.addWidget(self.top_panel_frame)

        self.stacked_widget = QStackedWidget(self)
        # self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget.setStyleSheet('background-color: #FFEEEE;')

        self.add_new_path()

        main_layout.addWidget(self.stacked_widget)

        self.button_panel = BottomActionPanel(self)
        self.button_panel.setStyleSheet('border-top: 1px solid #7E7E7E;')
        main_layout.addWidget(self.button_panel)

        self.setLayout(main_layout)

        shortcut = QShortcut(QKeySequence("Shift+F"), self)
        shortcut.activated.connect(self.next_widget)

    def add_new_path(self):
        new_path = MainSplitter(self.stacked_widget)
        self.stacked_widget.addWidget(new_path)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)

        print(self.stacked_widget.currentIndex())

    def next_widget(self):
        index = self.stacked_widget.currentIndex()
        if index + 1 >= self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(0)
            self.top_left_group_layout.change_color_button(index, 0)
        else:
            self.stacked_widget.setCurrentIndex(index + 1)
            self.top_left_group_layout.change_color_button(index, index + 1)
        print(self.stacked_widget.currentIndex())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    # window.show()  # Для обычного отображения окна без максимизации
    sys.exit(app.exec())
