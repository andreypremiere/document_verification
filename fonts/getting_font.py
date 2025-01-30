from PyQt6.QtGui import QFontDatabase


def get_font(family):
    path_font = None

    if family == "Noto Sans":
        path_font = 'fonts/NotoSans-VariableFont_wdth,wght.ttf'

    font_id = QFontDatabase.addApplicationFont(path_font)

    if font_id == -1:
        print("Не удалось загрузить шрифт.")
        return None

    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    return font_family

