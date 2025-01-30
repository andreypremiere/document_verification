import os
from multiprocessing.pool import ThreadPool
import fitz
import cv2
import numpy as np
import pytesseract
# from pdf2image import convert_from_path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QSplitter, QScrollArea, QFileDialog
from pdf2image import convert_from_path

from fonts.getting_font import get_font
from right_panel import RightPanel
from scroll_item import ScrollItem


class MainSplitter(QSplitter):
    """
    Представляет вкладку (путь). Содержит боковую панель и основной виджет с изображением.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.right_panel = None
        self.images_cv2 = None
        self.widget_layout1 = None
        self.orientation = Qt.Orientation.Horizontal
        self.parent = parent

        self.current_page = None
        self.main_area_layout = None
        self.scroll_area2 = None
        self.scroll_area1 = None
        self.files_path = None

        self.selected_element_index = None

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QSplitter {
                background-color: #FBFBFB;
            }

            QSplitter::handle {
                background-color: transparent;  /* Цвет ручки */
                border-right: 1px solid #7E7E7E;  /* Цвет границы ручки */
                width: 1px;
            }
        """)

        self.left_panel = QWidget(self)
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)

        self.area_top_1_frame = QFrame(self.left_panel)
        self.area_top_1_frame.setStyleSheet("""
            background-color: #FBFBFB;
        """)
        self.area_top_1_layout = QVBoxLayout(self.area_top_1_frame)
        self.area_top_1_layout.setContentsMargins(0, 0, 0, 0)
        self.area_top_1_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.label_1 = QLabel('Файлы')
        self.label_1.setFont(QFont(get_font('Noto Sans'), 9, 400))
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_1.setContentsMargins(0, 10, 0, 10)

        self.scroll_area1 = QScrollArea(self.area_top_1_frame)
        self.scroll_area1.setStyleSheet("""
            border: none;
        """)
        self.scroll_area1.setWidgetResizable(True)

        self.widget_area1 = QWidget(self.scroll_area1)
        self.widget_layout1 = QVBoxLayout(self.widget_area1)
        self.widget_layout1.setContentsMargins(0, 0, 0, 0)
        self.widget_layout1.setSpacing(3)
        self.widget_layout1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget_area1.setLayout(self.widget_layout1)
        self.scroll_area1.setWidget(self.widget_area1)

        self.button_choosing_path = QPushButton('Выбрать путь', self.area_top_1_frame)
        self.button_choosing_path.setFont(QFont(get_font('Noto Sans'), 9, 400))
        self.button_choosing_path.clicked.connect(self.open_folder_dialog)
        self.button_choosing_path.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #7E7E7E;
                border-radius: 12px;
                padding: 4px 14px;
            }

            QPushButton:hover {
                background-color: #EAFFD5;
            }

            QPushButton:pressed {
                background-color: #DAFFB5;
            }
        """)

        self.area_top_1_layout.addWidget(self.label_1)
        if self.files_path is None:
            self.scroll_area1.hide()
        else:
            self.button_choosing_path.hide()
        self.area_top_1_layout.addWidget(self.scroll_area1)
        self.area_top_1_layout.addWidget(self.button_choosing_path, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.scroll_area2 = QScrollArea(self.left_panel)
        self.scroll_area2.setStyleSheet("""
            background-color: #FBFBFB;
        """)
        self.scroll_area2.setWidgetResizable(True)
        self.scroll_area2.setWidget(QLabel("Scroll area 2"))

        self.panel_splitter = QSplitter(Qt.Orientation.Vertical, self.left_panel)

        self.panel_splitter.setStyleSheet("""
            QSplitter {
                background-color: #E2FFC2;
            }

            QSplitter::handle {
                background-color: transparent;  /* Цвет ручки */
                border-top: 1px solid #7E7E7E;  /* Цвет границы ручки */
                width: 1px;
            }
        # """)
        self.panel_splitter.addWidget(self.area_top_1_frame)
        self.panel_splitter.addWidget(self.scroll_area2)
        self.panel_splitter.setStretchFactor(0, 1)  # Левый виджет занимает больше места
        self.panel_splitter.setStretchFactor(1, 1)  # Левый виджет занимает больше места

        self.left_layout.addWidget(self.panel_splitter)

        self.right_panel = RightPanel(self)
        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 4)

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку",
            r"C:\Users\andre\OneDrive\Рабочий стол\тестоввая",
        )
        if folder:
            print(f"Выбрана папка: {folder}")
            self.files_path = folder
            self.get_files_pdf()
            self.fills_files_area()
            self.button_choosing_path.hide()
            self.scroll_area1.show()

    def get_files_pdf(self):
        if os.path.isdir(self.files_path):
            self.all_files_pdf = [file for file in os.listdir(self.files_path) if file.endswith('.pdf')]
            print(self.all_files_pdf)

    def fills_files_area(self):
        for i in range(len(self.all_files_pdf)):
            self.widget_layout1.addWidget(ScrollItem(i, self, self.all_files_pdf[i], self.files_path))

    def process_page(self, pdf_path, page_number):
        """ Функция для обработки одной страницы """
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(page_number)
            pix = page.get_pixmap(matrix=fitz.Matrix(6, 6))  # Увеличиваем масштаб для лучшего качества
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

            if pix.n == 4:  # Преобразуем RGBA в RGB
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            return img
        except Exception as e:
            print(f"Ошибка при обработке страницы {page_number}: {e}")
            return None

    def open_pdf_file(self, index):
        """ Открываем PDF и конвертируем в изображения с помощью PyMuPDF (fitz) """
        pdf_path = f"{self.files_path}/{self.all_files_pdf[index]}"

        try:
            doc = fitz.open(pdf_path)
            num_pages = len(doc)
        except Exception as e:
            print(f"Ошибка при открытии PDF: {e}")
            return

        # Параллельная обработка страниц
        with ThreadPool(processes=num_pages) as pool:
            self.images_cv2 = pool.starmap(self.process_page, [(pdf_path, i) for i in range(num_pages)])

        # Удаляем None-значения
        self.images_cv2 = [img for img in self.images_cv2 if img is not None]

    # def process_page(self, page):
    #     """ Функция для обработки одной страницы """
    #     try:
    #         open_cv_image = np.array(page)
    #         open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    #         return open_cv_image
    #     except Exception as e:
    #         print(f"Ошибка при конвертации страницы: {e}")
    #         return None
    #
    # def open_pdf_file(self, index):
    #     """ Функция для открытия PDF и конвертации в изображения """
    #     poppler_path = r"Release-24.08.0-0/poppler-24.08.0/Library/bin"
    #
    #     try:
    #         images_pil = convert_from_path(self.files_path + '/' + self.all_files_pdf[index],
    #                                        dpi=300, poppler_path=poppler_path, thread_count=8)
    #         if not images_pil:
    #             print("Ошибка: PDF-файл пуст или не удалось извлечь страницы.")
    #             return
    #     except Exception as e:
    #         print(f"Ошибка чтения PDF: {e}")
    #         return
    #
    #     with ThreadPool(processes=len(images_pil)) as pool:
    #         self.images_cv2 = pool.map(self.process_page, images_pil)
    #
    #     # Удаляем None-значения, если обработка страниц не удалась
    #     self.images_cv2 = [img for img in self.images_cv2 if img is not None]


    def set_image(self):
        if self.current_page is None:
            self.current_page = 0
            self.right_panel.middle_panel.clear_rectangles()
            self.right_panel.set_image(0)
            self.right_panel.top_panel.set_current_page(self.current_page)

            return

        if self.current_page >= len(self.images_cv2) or self.current_page + 1 < 0:
            self.right_panel.middle_panel.clear_rectangles()
            self.current_page = 0
            self.right_panel.set_image(0)
            self.right_panel.top_panel.set_current_page(self.current_page)

            return

        self.right_panel.middle_panel.clear_rectangles()
        self.right_panel.set_image(self.current_page)
        self.right_panel.top_panel.set_current_page(self.current_page)

    def next_page(self):
        if self.current_page + 1 >= len(self.images_cv2) or self.current_page + 1 < 0:
            return
        self.right_panel.middle_panel.clear_rectangles()

        self.current_page = self.current_page + 1
        self.right_panel.set_image(self.current_page)
        self.right_panel.top_panel.set_current_page(self.current_page)


    def prev_page(self):
        if self.current_page - 1 >= len(self.images_cv2) or self.current_page - 1 < 0:
            return
        self.right_panel.middle_panel.clear_rectangles()

        self.current_page = self.current_page - 1
        self.right_panel.set_image(self.current_page)
        self.right_panel.top_panel.set_current_page(self.current_page)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_A:
            self.prev_page()
        elif event.key() == Qt.Key.Key_D:
            self.next_page()

    def improve_image_for_ocr(self, crop):
        """ Улучшение качества изображения для OCR с адаптивной бинаризацией """

        # Преобразование в серый цвет
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # Удаление шума
        denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

        # Повышение контраста
        contrast = cv2.convertScaleAbs(denoised, alpha=2.5, beta=0)  # alpha - контраст

        # Применение адаптивной бинаризации
        adaptive_threshold = cv2.adaptiveThreshold(
            contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Увлажнение и улучшение резкости
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # Фильтр для повышения резкости
        sharpened = cv2.filter2D(adaptive_threshold, -1, sharpen_kernel)

        return sharpened

    def edit_element(self):
        rect = self.right_panel.middle_panel.rectangles[self.current_page][-1]['rect']
        x, y, w, h = int(rect.x()), int(rect.y()), int(rect.width()), int(rect.height())
        crop = self.images_cv2[self.current_page][y:y + h, x:x + w]

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        pytesseract.pytesseract.tesseract_cmd = r"D:\tesseract\tesseract.exe"

        custom_config = r'--oem 1 --psm 6'
        text = pytesseract.image_to_string(gray, lang="rus", config=custom_config)

        print("текст: ")
        print(text)