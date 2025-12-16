from PySide6.QtGui import QPainterPath

from src.logic.Shape import Shape


class Ellipse(Shape):
    def __init__(self, x, y, w, h, color="black", stroke_width=2):
        super().__init__(color, stroke_width)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        # Отличие только в методе: addEllipse вместо addRect
        path.addEllipse(self.x, self.y, self.w, self.h)
        self.setPath(path)

    @property
    def type_name(self) -> str:
        return "ellipse"

    def to_dict(self) -> dict:
        # Код идентичен Rectangle, можно было бы вынести в общий класс-предок
        # RectangularShape, но для обучения копипаста допустима для наглядности.
        return {
            "type": self.type_name,
            "props": {
                "x": self.x, "y": self.y,
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }