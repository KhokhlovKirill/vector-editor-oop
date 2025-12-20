# src/constants.py

# Настройки окна
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Vector Editor"

# Настройки сцены
DEFAULT_SCENE_WIDTH = 800
DEFAULT_SCENE_HEIGHT = 600

# Настройки фигур
DEFAULT_STROKE_WIDTH = 2
MIN_STROKE_WIDTH = 1
MAX_STROKE_WIDTH = 50
DEFAULT_COLOR = "black"
DEFAULT_COLOR_HEX = "#000000"

# Типы фигур (чтобы не писать строки вручную и не опечатываться)
TYPE_LINE = "line"
TYPE_RECT = "rect"
TYPE_ELLIPSE = "ellipse"
TYPE_GROUP = "group"
TYPE_SELECT = "select"

# Цвета фона
BG_COLOR_WHITE = "white"
BG_COLOR_TRANSPARENT = "transparent"
PANEL_BG_COLOR = "#f0f0f0"

# Размеры панелей
TOOLS_PANEL_WIDTH = 120
PROPERTIES_PANEL_WIDTH = 200

# Настройки Undo/Redo
UNDO_STACK_LIMIT = 50

# Настройки файлов
PROJECT_VERSION = "1.0"
PROJECT_FILE_EXTENSIONS = "Vector Project (*.json *.vec)"
IMAGE_FILTERS = "PNG Image (*.png);;JPEG Image (*.jpg)"
SAVE_FILTERS = f"Vector Project (*.json);;{IMAGE_FILTERS}"

# Настройки координат (для SpinBox в properties)
MIN_COORDINATE = -10000
MAX_COORDINATE = 10000

# Стили приложения
APP_STYLE = "Fusion"


