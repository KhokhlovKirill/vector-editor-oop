from PySide6.QtGui import QPainterPath
from src.logic.Shape import Shape


class Rectangle(Shape):
    def __init__(self, x, y, w, h, color="black", stroke_width=2):
        super().__init__(color, stroke_width)

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        path.addRect(self.x, self.y, self.w, self.h)

        self.setPath(path)


    @property
    def type_name(self) -> str:
        return "rect"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "props": {
                "x": self.rect().x(),
                "y": self.rect().y(),
                "w": self.rect().width(),
                "h": self.rect().height(),
                "color": self.pen().color().name()
            }
        }

    def set_geometry(self, start_point, end_point):
        self.x = min(start_point.x(), end_point.x())
        self.y = min(start_point.y(), end_point.y())
        self.w = abs(end_point.x() - start_point.x())
        self.h = abs(end_point.y() - start_point.y())

        path = QPainterPath()
        path.addRect(self.x, self.y, self.w, self.h)

        self.setPath(path)