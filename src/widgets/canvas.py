from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QUndoStack

from src.constants import (
    DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT, UNDO_STACK_LIMIT,
    TYPE_SELECT, TYPE_RECT, TYPE_LINE, TYPE_ELLIPSE, DEFAULT_COLOR
)
from src.logic.Group import Group
from src.logic.commands import DeleteCommand
from src.logic.factory import ShapeFactory
from src.logic.tools import SelectionTool, CreationTool


class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setMouseTracking(True)

        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(UNDO_STACK_LIMIT)

        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT)

        self.setRenderHint(self.renderHints() | QPainter.RenderHint.Antialiasing)
        self.setAlignment(Qt.AlignCenter)

        self.tools = {
            TYPE_SELECT: SelectionTool(self, self.undo_stack),
            TYPE_RECT: CreationTool(self, TYPE_RECT, self.undo_stack),
            TYPE_LINE: CreationTool(self, TYPE_LINE, self.undo_stack),
            TYPE_ELLIPSE: CreationTool(self, TYPE_ELLIPSE, self.undo_stack)
        }
        self.active_tool = self.tools[TYPE_SELECT]
        self.active_color = DEFAULT_COLOR

        self.start_point = None

    def set_tool(self, tool_name):
        if tool_name in self.tools:
            self.active_tool = self.tools[tool_name]

            if tool_name == TYPE_SELECT:
                self.setCursor(Qt.ArrowCursor)
            else:
                self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, event):
        self.active_tool.mouse_press(event)

    def mouseMoveEvent(self, event):
        self.active_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.active_tool.mouse_release(event)

    def group_selection(self):
        """Создает группу из выделенных элементов"""
        selected_items = self.scene.selectedItems()

        if not selected_items:
            return

        group = Group()

        self.scene.addItem(group)

        for item in selected_items:
            item.setSelected(False)

            group.addToGroup(item)

        group.setSelected(True)

    def ungroup_selection(self):
        """Разбивает выделенные группы на отдельные элементы"""
        selected_items = self.scene.selectedItems()

        for item in selected_items:
            if isinstance(item, Group):
                self.scene.destroyGroup(item)

    def delete_selected(self):
        selected = self.scene.selectedItems()
        if not selected:
            return

        self.undo_stack.beginMacro("Delete Selection")

        for item in selected:
            cmd = DeleteCommand(self.scene, item)
            self.undo_stack.push(cmd)

        self.undo_stack.endMacro()