from src.logic.Ellipse import Ellipse
from src.logic.Line import Line
from src.logic.Rectangle import Rectangle

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str, start_point, end_point, color: str):
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()

        # Для линий нам нужны именно точки начала и конца (даже если тянем назад)
        if shape_type == 'line':
            return Line(x1, y1, x2, y2, color)

        # Для прямоугольных фигур (Rect, Ellipse) нужна нормализация
        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)

        if shape_type == 'rect':
            return Rectangle(x, y, w, h, color)
        elif shape_type == 'ellipse':
            return Ellipse(x, y, w, h, color)
        else:
            # Важно: Фабрика должна сообщать, если её попросили невозможного
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")
