from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

from src.logic.factory import ShapeFactory
from src.logic.tools import SelectionTool, CreationTool


class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setMouseTracking(True)

        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600)

        self.setRenderHint(self.renderHints() | QPainter.RenderHint.Antialiasing)
        self.setAlignment(Qt.AlignCenter)

        self.tools = {
            "select": SelectionTool(self),
            "rect": CreationTool(self, "rect"),
            "line": CreationTool(self, "line"),
            "ellipse": CreationTool(self, "ellipse")
        }
        self.active_tool = self.tools["select"]
        self.active_color = "black"

        self.start_point = None

    def set_tool(self, tool_name):
        if tool_name in self.tools:
            self.active_tool = self.tools[tool_name]

            if tool_name == "select":
                self.setCursor(Qt.ArrowCursor)
            else:
                self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, event):
        self.active_tool.mouse_press(event)

    def mouseMoveEvent(self, event):
        self.active_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.active_tool.mouse_release(event)


