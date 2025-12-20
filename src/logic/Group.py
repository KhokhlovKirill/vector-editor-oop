from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsItem
from PySide6.QtCore import QPointF


class Group(QGraphicsItemGroup):
    def __init__(self):
        QGraphicsItemGroup.__init__(self)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

        self.setHandlesChildEvents(True)

    @property
    def type_name(self) -> str:
        return "group"

    def set_geometry(self, start: QPointF, end: QPointF):
        pass

    def set_active_color(self, color: str):
        """
        Рекурсивно меняет цвет всех детей.
        Внешний код (Canvas) просто вызывает group.set_active_color("red"),
        не зная, что внутри 50 объектов.
        """
        for child in self.childItems():
            if hasattr(child, 'set_active_color'):
                child.set_active_color(color)

    def to_dict(self) -> dict:
        """
        Рекурсивная сериализация.
        Группа сохраняет себя как список словарей своих детей.
        """
        children_data = []
        for child in self.childItems():
            # Проверяем наличие метода to_dict (duck typing)
            # Это работает для всех Shape и для вложенных Group
            if hasattr(child, 'to_dict'):
                children_data.append(child.to_dict())

        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "children": children_data
        }