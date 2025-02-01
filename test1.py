import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QListWidget, QListWidgetItem, QCheckBox


class MultiSelectComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)  # Разрешаем редактирование (чтобы отображать выбранные элементы)
        self.lineEdit().setReadOnly(True)  # Делаем поле ввода нередактируемым

        self.list_widget = QListWidget()  # Создаём список с чекбоксами
        self.setModel(self.list_widget.model())
        self.setView(self.list_widget)

        self.items = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
        self.selected_items = []

        for item in self.items:
            list_item = QListWidgetItem(self.list_widget)
            list_item.setText(item)
            list_item.setFlags(list_item.flags() |
                               Qt.ItemFlag.ItemIsUserCheckable)  # Разрешаем чекбоксы
            list_item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(list_item)

        self.list_widget.itemChanged.connect(self.update_selected_items)

    def update_selected_items(self):
        """Обновляет список выбранных элементов"""
        self.selected_items = [self.list_widget.item(i).text()
                               for i in range(self.list_widget.count())
                               if self.list_widget.item(i).checkState() == Qt.CheckState.Checked]
        self.lineEdit().setText(", ".join(self.selected_items))  # Обновляем текст в QComboBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Множественный выбор в QComboBox")
        self.resize(400, 200)

        layout = QVBoxLayout()
        self.multi_select_combo = MultiSelectComboBox()
        layout.addWidget(self.multi_select_combo)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
