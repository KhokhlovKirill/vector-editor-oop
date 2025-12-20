import json

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFrame, QVBoxLayout, QPushButton, QFileDialog, \
    QMessageBox
from PySide6.QtGui import QAction, QKeySequence

from src.logic.factory import ShapeFactory
from src.logic.strategies import ImageSaveStrategy, JsonSaveStrategy
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

        # Действие "Открыть"
        open_action = QAction("&Open", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.setStatusTip("Open an existing file")
        open_action.triggered.connect(self.on_open_clicked)
        file_menu.addAction(open_action)

        # Действие "Сохранить"
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setStatusTip("Save the current file")
        save_action.triggered.connect(self.on_save_clicked)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        # Действие "Выход"
        exit_action = QAction("E&xit", self)
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

    def on_save_clicked(self):
        filters = "Vector Project (*.json);;PNG Image (*.png);;JPEG Image (*.jpg)"
        filename, selected_filter = QFileDialog.getSaveFileName(
            self, "Save File", "", filters
        )

        if not filename:
            return

        strategy = None

        if filename.lower().endswith(".png"):
            strategy = ImageSaveStrategy("PNG", background_color="transparent")
        elif filename.lower().endswith(".jpg"):
            strategy = ImageSaveStrategy("JPG", background_color="white")  # JPG не умеет в прозрачность
        else:
            strategy = JsonSaveStrategy()

        # ВЫПОЛНЕНИЕ
        try:
            strategy.save(filename, self.canvas.scene)
            self.statusBar().showMessage(f"Successfully saved to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")

    def _collect_scene_data(self):
        project_data = {
            "version": "1.0",
            "scene": {
                "width": self.canvas.scene.width(),
                "height": self.canvas.scene.height()
            },
            "shapes": []
        }

        items_in_order = self.canvas.scene.items()[::-1]

        for item in items_in_order:
            if hasattr(item, "to_dict"):
                project_data["shapes"].append(item.to_dict())

        return project_data

    def on_open_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть проект",
            "",
            "Vector Project (*.json *.vec)"
        )

        if not path:
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "version" not in data or "shapes" not in data:
                raise ValueError("Некорректный формат файла")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Не удалось прочитать файл:\n{e}")
            return

        self.canvas.scene.clear()
        self.canvas.undo_stack.clear()

        scene_info = data.get("scene", {})
        width = scene_info.get("width", 800)
        height = scene_info.get("height", 600)
        self.canvas.scene.setSceneRect(0, 0, width, height)

        shapes_data = data.get("shapes", [])

        errors_count = 0

        for shape_dict in shapes_data:
            try:
                shape_obj = ShapeFactory.from_dict(shape_dict)

                # Добавляем на сцену
                self.canvas.scene.addItem(shape_obj)

            except Exception as e:
                print(f"Error loading shape: {e}")
                errors_count += 1

        if errors_count > 0:
            self.statusBar().showMessage(f"Загружено с ошибками ({errors_count} фигур пропущено)")
        else:
            self.statusBar().showMessage(f"Проект загружен: {path}")