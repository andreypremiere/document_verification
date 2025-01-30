from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout

from image_widget import ImageViewer
from sub_top_panel import SubTopPanel


class RightPanel(QWidget):
    """
    Основная панель, которая содержит виджеты о выделенных признаках, изображении и запуска программы.
    """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                border: 1px solid #7E7E7E;
                background-color: 
            }
        """)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(4)
        self.main_layout.setContentsMargins(4, 4, 4, 4)

        # Верхняя панель
        self.top_panel = SubTopPanel(self)

        self.main_layout.addWidget(self.top_panel)

        # средняя панель
        self.middle_panel = ImageViewer(self)
        self.main_layout.addWidget(self.middle_panel)

        # нижняя панель
        self.button_panel = QFrame(self)
        self.button_panel.setStyleSheet('background-color: orange;')
        self.button_panel_layout = QHBoxLayout(self.button_panel)
        self.button_panel.setFixedHeight(60)
        self.main_layout.addWidget(self.button_panel)

    def set_image(self, index):
        self.middle_panel.set_image(self.parent.images_cv2[index])
