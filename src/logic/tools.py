from abc import ABC, abstractmethod
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsView

from src.constants import DEFAULT_COLOR
from src.logic.commands import AddShapeCommand, MoveCommand
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
    def __init__(self, view, shape_type, undo_stack, color=DEFAULT_COLOR):
        super().__init__(view)
        self.shape_type = shape_type
        self.color = color
        self.start_pos = None
        self.temp_shape = None
        self.undo_stack = undo_stack

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
            self.scene.removeItem(self.temp_shape)
            self.temp_shape = None

            end_pos = self.view.mapToScene(event.pos())
            try:
                final_shape = ShapeFactory.create_shape(
                    self.shape_type, self.start_pos, end_pos, DEFAULT_COLOR
                )

                command = AddShapeCommand(self.scene, final_shape)
                self.undo_stack.push(command)

            except ValueError:
                pass

            self.start_pos = None
        else:
            QGraphicsView.mouseReleaseEvent(self.view, event)


class SelectionTool(Tool):
    def __init__(self, view, undo_stack):
        super().__init__(view)
        self.undo_stack = undo_stack

        self.item_positions = {}

    def mouse_press(self, event):
        super(type(self.view), self.view).mousePressEvent(event)

        self.item_positions.clear()
        for item in self.scene.selectedItems():
            self.item_positions[item] = item.pos()

    def mouse_move(self, event):
        super(type(self.view), self.view).mouseMoveEvent(event)

    def mouse_release(self, event):
        super(type(self.view), self.view).mouseReleaseEvent(event)

        moved_items = []
        for item, old_pos in self.item_positions.items():
            new_pos = item.pos()
            if new_pos != old_pos:
                moved_items.append((item, old_pos, new_pos))

        if moved_items:
            self.undo_stack.beginMacro("Move Items")

            for item, old_pos, new_pos in moved_items:
                cmd = MoveCommand(item, old_pos, new_pos)
                self.undo_stack.push(cmd)

            self.undo_stack.endMacro()

        # Очищаем память
        self.item_positions.clear()