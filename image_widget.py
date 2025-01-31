import random
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QImage, QPixmap, QPen, QColor, QFont
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItemGroup


class ImageViewer(QGraphicsView):
    """
    Виджет вывода изображения, находится в right_panel (middle_widget).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_color = None
        self.zoom_factor = 1.3
        self.current_scale = None
        self.space_pressed = False
        self.drawing = False
        self.start_point = None
        self.current_rect = None
        self.rectangles = {}
        self.rect_counter = 0

        self.scene = QGraphicsScene(self)
        self.setStyleSheet('background-color: #FBFBFB;')
        self.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def set_image(self, cv2_image):
        height, width, channel = cv2_image.shape
        print(width, height)
        bytes_per_line = channel * width
        q_image = QImage(cv2_image.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)

        self.pixmap_item.setPixmap(pixmap)

        try:
            print(self.parent.parent.current_page)
            if self.parent.parent.current_page in self.rectangles:
                for item in self.rectangles[self.parent.parent.current_page]:
                    self.scene.addItem(item['group'])
                    self.add_rect_to_top_panel(item)
        except Exception as e:
            print(e)

        if self.current_scale is None:
            self.current_scale = 1
            cf_height = self.parent.height() / height
            cf_width = self.parent.width() / width
            self.scale(min(cf_width, cf_height), min(cf_width, cf_height))

        self.setSceneRect(0, 0, pixmap.width(), pixmap.height())

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            # Увеличиваем масштаб
            self.scale(self.zoom_factor, self.zoom_factor)
            self.current_scale *= self.zoom_factor
        else:
            # Уменьшаем масштаб
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)
            self.current_scale /= self.zoom_factor

    def mousePressEvent(self, event):
        """Включение режима перетаскивания при зажатой клавише Space и ЛКМ."""
        if event.button() == Qt.MouseButton.LeftButton and self.space_pressed:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)

        if event.button() == Qt.MouseButton.LeftButton and not self.space_pressed:
            try:
                self.drawing = True
                self.start_point = self.mapToScene(event.pos())
                self.current_rect = QGraphicsRectItem()
                self.current_color = self.random_rgb_color()
                self.current_rect.setPen(QPen(QColor(*self.current_color), 2))
                self.scene.addItem(self.current_rect)
            except Exception as e:
                print('Ошибка при клике:', e)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Обновление прямоугольника при движении мыши."""
        try:
            if self.drawing and self.start_point:
                end_point = self.mapToScene(event.pos())
                rect = QRectF(self.start_point,
                              end_point).normalized()
                self.current_rect.setRect(rect)
        except Exception as e:
            print('Ошибка при передвижении:', e)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Выключение режима перетаскивания после отпускания ЛКМ."""
        if event.button() == Qt.MouseButton.LeftButton and self.space_pressed:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)

        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            self.start_point = None

            if self.current_rect is not None and self.parent.parent.current_page is not None:
                rect = self.current_rect.rect()
                x, y = rect.x(), rect.y()
                width, height = rect.width(), rect.height()
                print(f"Координаты: ({x}, {y}), ширина: {width}, высота: {height}")
                print(self.current_rect.rect())

                if width * height > 4000:
                    # Создаём текстовую метку с номером
                    text_item = QGraphicsTextItem(str(self.rect_counter + 1))
                    text_item.setDefaultTextColor(QColor(*self.current_color))
                    text_item.setFont(QFont("Arial", 60))

                    # Устанавливаем позицию текста около верхнего левого угла прямоугольника
                    text_item.setPos(rect.x() - 100, rect.y() - 80)
                    group = QGraphicsItemGroup()
                    group.addToGroup(self.current_rect)
                    group.addToGroup(text_item)
                    group.setFlags(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable)
                    self.scene.addItem(group)

                    val = {'index': self.rect_counter, 'rect': rect, 'group': group, 'color': self.current_color}

                    self.add_rectangle(val)
                    print(self.rectangles)

                    self.rect_counter += 1

                    try:
                        self.parent.parent.edit_element()
                    except Exception as e:
                        print(e)
                else:
                    self.scene.removeItem(self.current_rect)

            self.current_rect = None
            self.current_color = None
        super().mouseReleaseEvent(event)

    def add_rectangle(self, rect):
        """Добавляет прямоугольник для текущего изображения."""
        if self.parent.parent.current_page is None:
            return

        if self.parent.parent.current_page not in self.rectangles:
            self.rectangles[self.parent.parent.current_page] = []

        self.rectangles[self.parent.parent.current_page].append(rect)
        self.add_rect_to_top_panel(rect)

    def clear_rectangles(self):
        print(self.parent.parent.current_page)
        try:
            """Удаляет текущие прямоугольники со сцены."""
            if self.parent.parent.current_page in self.rectangles:
                for item in self.rectangles[self.parent.parent.current_page]:
                    self.scene.removeItem(item['group'])

            self.clear_top_panel()
        except Exception:
            print('Ошибка очистки.')

    def keyPressEvent(self, event):
        """Обработка нажатия клавиш."""
        if event.key() == Qt.Key.Key_Space:
            self.space_pressed = True
            self.viewport().setCursor(Qt.CursorShape.OpenHandCursor)
        elif event.key() == Qt.Key.Key_Delete:
            self.delete_selected_group()
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Обработка отпускания клавиш."""
        if event.key() == Qt.Key.Key_Space:
            self.space_pressed = False
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        super().keyReleaseEvent(event)

    def random_rgb_color(self):
        r = random.randint(0, 233)
        g = random.randint(0, 236)
        b = random.randint(0, 230)
        return r, g, b

    def add_rect_to_top_panel(self, rect):
        self.parent.top_panel.generate_frame_icon(rect)

    def clear_top_panel(self):
        self.parent.top_panel.clear_panel()

    def remove_by_group(self, group):
        try:
            for key, sublist in self.rectangles.items():
                for sub in sublist:
                    if sub['group'] == group:
                        sublist.remove(sub)
                        self.scene.removeItem(group)
        except Exception as e:
            print(f'Ошибка удаления по группе. {e}')
        print(self.rectangles)

    # def delete_selected_group(self):
    #     """Удаляет выделенную группу и ее запись из self.rectangles."""
    #     selected_items = self.scene.selectedItems()
    #     if not selected_items:
    #         return
    #
    #     for item in selected_items:
    #         for key, sublist in self.rectangles.items():
    #             for rect in sublist:
    #                 if rect['group'] == item:
    #                     self.scene.removeItem(item)  # Удаление из сцены
    #                     sublist.remove(rect)  # Удаление из списка
    #                     self.parent.top_panel.remove_by_index(rect['index'])
    #                     break  # Прекращаем поиск, так как нашли нужный элемент

        print(self.rectangles)

# class MainWidget(QWidget):
#     """Главное окно с отображением изображения."""
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         # Основной макет
#         self.layout = QVBoxLayout(self)
#         self.layout.setContentsMargins(0, 0, 0, 0)
#
#         # Виджет для отображения изображения
#         self.image_viewer = ImageViewer(self)
#         self.layout.addWidget(self.image_viewer)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_widget = MainWidget()
#     main_widget.resize(800, 600)
#     main_widget.show()
#     image_path = "page_1.jpg"  # Укажите путь к вашему изображению
#     cv2_image = cv2.imread(image_path)
#     input()
#     main_widget.image_viewer.set_image(cv2_image)
#
#     print(main_widget.size())
#     sys.exit(app.exec())
