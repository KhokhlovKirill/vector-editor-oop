from abc import ABC, abstractmethod
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsView

from src.logic.factory import ShapeFactory


class Tool(ABC):
    def __init__(self, canvas_view):
        self.view = canvas_view
        self.scene = canvas_view.scene

    @abstractmethod
    def mouse_press(self, event): pass

    @abstractmethod
    def mouse_move(self, event): pass

    @abstractmethod
    def mouse_release(self, event): pass



class CreationTool(Tool):
    def __init__(self, view, shape_type, color="black"):
        super().__init__(view)
        self.shape_type = shape_type
        self.color = color
        self.start_pos = None
        self.temp_shape = None

    def mouse_press(self, event):
        if event.button() != Qt.LeftButton:
            QGraphicsView.mousePressEvent(self.view, event)
            return

        self.start_pos = self.view.mapToScene(event.pos())

        self.temp_shape = ShapeFactory.create_shape(
            self.shape_type,
            self.start_pos,
            self.start_pos,
            self.color
        )
        self.scene.addItem(self.temp_shape)

    def mouse_move(self, event):
        if self.temp_shape and (event.buttons() and Qt.LeftButton):
            current_pos = self.view.mapToScene(event.pos())
            self.temp_shape.set_geometry(self.start_pos, current_pos)
        else:
            QGraphicsView.mouseMoveEvent(self.view, event)

    def mouse_release(self, event):
        if self.temp_shape and event.button() == Qt.LeftButton:
            end_pos = self.view.mapToScene(event.pos())
            self.temp_shape.set_geometry(self.start_pos, end_pos)

            self.start_pos = None
            self.temp_shape = None
        else:
            QGraphicsView.mouseReleaseEvent(self.view, event)


class SelectionTool(Tool):
    def mouse_press(self, event):
        super(type(self.view), self.view).mousePressEvent(event)

    def mouse_move(self, event):
        QGraphicsView.mouseMoveEvent(self.view, event)

        item = self.view.itemAt(event.pos())

        if not (event.buttons() & Qt.LeftButton):
            if item:
                self.view.setCursor(Qt.OpenHandCursor)
            else:
                self.view.setCursor(Qt.ArrowCursor)

    def mouse_release(self, event):
        super(type(self.view), self.view).mouseReleaseEvent(event)