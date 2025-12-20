from PySide6.QtGui import QPainterPath

from src.constants import DEFAULT_COLOR, DEFAULT_STROKE_WIDTH
from src.logic.Shape import Shape


class Rectangle(Shape):
    def __init__(self, x, y, w, h, color=DEFAULT_COLOR, stroke_width=DEFAULT_STROKE_WIDTH):
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
        from src.constants import TYPE_RECT
        return TYPE_RECT

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "props": {
                "x": self.x,
                "y": self.y,
                "w": self.w,
                "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
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