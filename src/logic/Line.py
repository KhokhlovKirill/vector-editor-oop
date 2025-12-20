from PySide6.QtGui import QPainterPath

from src.constants import DEFAULT_COLOR, DEFAULT_STROKE_WIDTH
from src.logic.Shape import Shape


class Line(Shape):
    def __init__(self, x1, y1, x2, y2, color=DEFAULT_COLOR, stroke_width=DEFAULT_STROKE_WIDTH):
        super().__init__(color, stroke_width)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        path.moveTo(self.x1, self.y1)
        path.lineTo(self.x2, self.y2)

        self.setPath(path)

    @property
    def type_name(self) -> str:
        from src.constants import TYPE_LINE
        return TYPE_LINE

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "props": {
                "x1": self.x1, "y1": self.y1,
                "x2": self.x2, "y2": self.y2,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

    def set_geometry(self, start_point, end_point):
         self.x1 = start_point.x()
         self.y1 = start_point.y()
         self.x2 = end_point.x()
         self.y2 = end_point.y()

         path = QPainterPath()
         path.moveTo(self.x1, self.y1)
         path.lineTo(self.x2, self.y2)

         self.setPath(path)