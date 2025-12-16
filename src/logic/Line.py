from PySide6.QtGui import QPainterPath

from src.logic.Shape import Shape


class Line(Shape):
    def __init__(self, x1, y1, x2, y2, color="black", stroke_width=2):
        super().__init__(color, stroke_width)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        # Инструкция: встань в начало
        path.moveTo(self.x1, self.y1)
        # Инструкция: проведи черту до конца
        path.lineTo(self.x2, self.y2)

        self.setPath(path)

    @property
    def type_name(self) -> str:
        return "line"

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