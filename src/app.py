from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFrame, QVBoxLayout, QPushButton
from PySide6.QtGui import QAction, QKeySequence

from src.widgets.canvas import EditorCanvas
from src.widgets.properties import PropertiesPanel


class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vector Editor")
        self.resize(1000, 800)

        self._init_ui()

    def _init_ui(self):
        self.statusBar().showMessage("Готов к работе")

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Close the application")
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

        self._setup_layout()

        self.current_tool = "line"

        group_action = QAction("Group", self)
        group_action.setShortcut(QKeySequence("Ctrl+G"))
        group_action.triggered.connect(self.canvas.group_selection)

        ungroup_action = QAction("Ungroup", self)
        ungroup_action.setShortcut(QKeySequence("Ctrl+U"))
        ungroup_action.triggered.connect(self.canvas.ungroup_selection)

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction(group_action)
        edit_menu.addAction(ungroup_action)

        stack = self.canvas.undo_stack

        undo_action = stack.createUndoAction(self, "&Undo")
        undo_action.setShortcut(QKeySequence.Undo)

        redo_action = stack.createRedoAction(self, "&Redo")
        redo_action.setShortcut(QKeySequence.Redo)

        delete_action = QAction("Delete", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.canvas.delete_selected)

        self.menuBar().addAction(delete_action)
        self.addAction(delete_action)

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

    def _setup_layout(self):
        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        tools_panel = QFrame()
        tools_panel.setFixedWidth(120)
        tools_panel.setStyleSheet("background-color: #f0f0f0;")

        tools_layout = QVBoxLayout(tools_panel)
        self.btn_select = QPushButton("Select")
        self.btn_line = QPushButton("Line")
        self.btn_rect = QPushButton("Rect")
        self.btn_ellipse = QPushButton("Ellipse")

        self.btn_select.setCheckable(True)
        self.btn_line.setCheckable(True)
        self.btn_rect.setCheckable(True)
        self.btn_ellipse.setCheckable(True)

        self.btn_line.setChecked(True)

        self.btn_select.clicked.connect(lambda: self.on_change_tool("select"))
        self.btn_line.clicked.connect(lambda: self.on_change_tool("line"))
        self.btn_rect.clicked.connect(lambda: self.on_change_tool("rect"))
        self.btn_ellipse.clicked.connect(lambda: self.on_change_tool("ellipse"))

        tools_layout.addWidget(self.btn_select)
        tools_layout.addWidget(self.btn_line)
        tools_layout.addWidget(self.btn_rect)
        tools_layout.addWidget(self.btn_ellipse)
        tools_layout.addStretch()

        self.canvas = EditorCanvas()
        main_layout.addWidget(tools_panel)
        main_layout.addWidget(self.canvas)
        self.on_change_tool('line')

        self.props_panel = PropertiesPanel(self.canvas.scene, self.canvas.undo_stack)

        main_layout.addWidget(self.props_panel)



    def on_change_tool(self, tool_name):
        self.current_tool = tool_name
        print(f"Выбран инструмент: {tool_name}")

        if tool_name == "line":
            self.btn_select.setChecked(False)
            self.btn_line.setChecked(True)
            self.btn_rect.setChecked(False)
            self.btn_ellipse.setChecked(False)
        elif tool_name == "rect":
            self.btn_select.setChecked(False)
            self.btn_line.setChecked(False)
            self.btn_rect.setChecked(True)
            self.btn_ellipse.setChecked(False)
        elif tool_name == "select":
            self.btn_select.setChecked(True)
            self.btn_line.setChecked(False)
            self.btn_rect.setChecked(False)
            self.btn_ellipse.setChecked(False)
        else:
            self.btn_select.setChecked(False)
            self.btn_line.setChecked(False)
            self.btn_rect.setChecked(False)
            self.btn_ellipse.setChecked(True)

        self.canvas.set_tool(tool_name)