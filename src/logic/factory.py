from src.constants import TYPE_LINE, TYPE_RECT, TYPE_ELLIPSE, TYPE_GROUP, DEFAULT_COLOR
from src.logic.Ellipse import Ellipse
from src.logic.Group import Group
from src.logic.Line import Line
from src.logic.Rectangle import Rectangle


class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str, start_point, end_point, color: str):
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()

        if shape_type == TYPE_LINE:
            return Line(x1, y1, x2, y2, color)

        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)

        if shape_type == TYPE_RECT:
            return Rectangle(x, y, w, h, color)
        elif shape_type == TYPE_ELLIPSE:
            return Ellipse(x, y, w, h, color)
        else:
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")

    @staticmethod
    def from_dict(data: dict):
        """
        Восстанавливает объект (или дерево объектов) из словаря.
        """
        shape_type = data.get("type")

        if shape_type == TYPE_GROUP:
            return ShapeFactory._create_group(data)
        elif shape_type in [TYPE_RECT, TYPE_LINE, TYPE_ELLIPSE]:
            return ShapeFactory._create_primitive(data)
        else:
            raise ValueError(f"Unknown type: {shape_type}")

    @staticmethod
    def _create_primitive(data: dict):
        props = data.get("props", {})
        shape_type = data.get("type")

        if shape_type == TYPE_RECT:
            color = props.get("color", DEFAULT_COLOR)
            obj = Rectangle(props['x'], props['y'], props['w'], props['h'], color)

        elif shape_type == TYPE_LINE:
            color = props.get("color", DEFAULT_COLOR)
            obj = Line(props['x1'], props['y1'], props['x2'], props['y2'], color)

        elif shape_type == TYPE_ELLIPSE:
            color = props.get("color", DEFAULT_COLOR)
            obj = Ellipse(props['x'], props['y'], props['w'], props['h'], color)

        if "pos" in data:
            obj.setPos(data["pos"][0], data["pos"][1])

        return obj

    @staticmethod
    def _create_group(data: dict):
        group = Group()

        x, y = data.get("pos", [0, 0])
        group.setPos(x, y)

        children_data = data.get("children", [])
        for child_dict in children_data:
            child_item = ShapeFactory.from_dict(child_dict)

            group.addToGroup(child_item)

            if "pos" in child_dict:
                cx, cy = child_dict["pos"]
                child_item.setPos(cx, cy)

        return group