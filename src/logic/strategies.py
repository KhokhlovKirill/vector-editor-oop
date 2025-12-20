import json
from abc import ABC, abstractmethod

from PySide6.QtCore import QRectF
from PySide6.QtGui import QImage, QColor, QPainter

from src.constants import PROJECT_VERSION, BG_COLOR_WHITE


class SaveStrategy(ABC):
    @abstractmethod
    def save(self, filename: str, scene):
        """
        :param filename: Путь сохранения
        :param scene: Ссылка на QGraphicsScene (источник данных)
        """
        pass


class JsonSaveStrategy(SaveStrategy):
    def save(self, filename, scene):
        data = {
            "version": PROJECT_VERSION,
            "scene": {
                "width": scene.width(),
                "height": scene.height()
            },
            "shapes": []
        }

        items = scene.items()[::-1]

        for item in items:
            if hasattr(item, "to_dict"):
                data["shapes"].append(item.to_dict())

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)


class ImageSaveStrategy(SaveStrategy):
    def __init__(self, format_name="PNG", background_color=BG_COLOR_WHITE):
        self.format_name = format_name  # PNG, JPG
        self.bg_color = background_color

    def save(self, filename, scene):
        rect = scene.sceneRect()
        width = int(rect.width())
        height = int(rect.height())

        image = QImage(width, height, QImage.Format_ARGB32)

        if self.bg_color == "transparent":
            image.fill(QColor(0, 0, 0, 0))
        else:
            image.fill(QColor(self.bg_color))

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        scene.render(painter, QRectF(image.rect()), rect)

        painter.end()  # Важно завершить рисование перед сохранением

        image.save(filename, self.format_name)