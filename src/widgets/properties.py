from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QSpinBox, QPushButton, QFrame, QColorDialog, QHBoxLayout, QDoubleSpinBox)
from PySide6.QtCore import Qt

from src.constants import (
    PROPERTIES_PANEL_WIDTH, PANEL_BG_COLOR, MIN_STROKE_WIDTH, MAX_STROKE_WIDTH,
    DEFAULT_COLOR_HEX, MIN_COORDINATE, MAX_COORDINATE
)
from src.logic.commands import ChangeColorCommand, ChangeWidthCommand


class PropertiesPanel(QWidget):
    def __init__(self, scene, undo_stack):
        super().__init__()
        self.scene = scene
        self.undo_stack = undo_stack

        self._init_ui()

        self.scene.selectionChanged.connect(self.on_selection_changed)

    def _init_ui(self):
        self.setFixedWidth(PROPERTIES_PANEL_WIDTH)
        self.setStyleSheet(f"background-color: {PANEL_BG_COLOR}; border-left: 1px solid #ccc;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Свойства")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self.lbl_type = QLabel("")
        self.lbl_type.setStyleSheet("font-style: italic; color: #666;")
        layout.addWidget(self.lbl_type)

        layout.addWidget(QLabel("Толщина обводки:"))
        self.spin_width = QSpinBox()
        self.spin_width.setRange(MIN_STROKE_WIDTH, MAX_STROKE_WIDTH)
        self.spin_width.valueChanged.connect(self.on_width_changed)
        layout.addWidget(self.spin_width)

        self.btn_color = QPushButton("Pick Color")
        self.btn_color.setFixedHeight(30)
        self.btn_color.clicked.connect(self.on_color_clicked)

        geo_layout = QHBoxLayout()

        self.spin_x = QDoubleSpinBox()
        self.spin_x.setRange(MIN_COORDINATE, MAX_COORDINATE)
        self.spin_x.setPrefix("X: ")
        self.spin_x.valueChanged.connect(self.on_geo_changed)

        self.spin_y = QDoubleSpinBox()
        self.spin_y.setRange(MIN_COORDINATE, MAX_COORDINATE)
        self.spin_y.setPrefix("Y: ")
        self.spin_y.valueChanged.connect(self.on_geo_changed)

        layout.addLayout(geo_layout)

        layout.addWidget(QLabel("Цвет линии:"))

        layout.addWidget(self.btn_color)
        geo_layout.addWidget(self.spin_x)
        geo_layout.addWidget(self.spin_y)

        layout.addStretch()

        self.setEnabled(False)

    def on_selection_changed(self):
        """Вызывается автоматически при клике по фигурам"""
        selected_items = self.scene.selectedItems()

        if not selected_items:
            self.setEnabled(False)
            self.spin_width.setValue(MIN_STROKE_WIDTH)
            self.btn_color.setStyleSheet("background-color: transparent")
            return

        self.setEnabled(True)

        item = selected_items[0]

        current_width = MIN_STROKE_WIDTH
        current_color = DEFAULT_COLOR_HEX

        if hasattr(item, "pen") and item.pen() is not None:
            current_width = item.pen().width()
            current_color = item.pen().color().name()

        self.spin_width.blockSignals(True)
        self.spin_width.setValue(current_width)
        self.spin_width.blockSignals(False)

        self.btn_color.setStyleSheet(f"background-color: {current_color}; border: 1px solid gray;")

        self.spin_x.blockSignals(True)
        self.spin_y.blockSignals(True)

        self.spin_x.setValue(item.pos().x())
        self.spin_y.setValue(item.pos().y())

        self.spin_x.blockSignals(False)
        self.spin_y.blockSignals(False)

        if hasattr(item, "type_name"):
            type_text = item.type_name.capitalize()
        else:
            type_text = type(item).__name__

        if len(selected_items) > 1:
            type_text += f" (+{len(selected_items) - 1})"

        self.lbl_type.setText(type_text)
        self.update_width_ui(selected_items)

    def on_width_changed(self, value):
        selected_items = self.scene.selectedItems()
        if not selected_items:
            return

        self.undo_stack.beginMacro("Change Width All")

        for item in selected_items:
            cmd = ChangeWidthCommand(item, value)
            self.undo_stack.push(cmd)

        self.undo_stack.endMacro()
        self.scene.update()

    def on_geo_changed(self, value):
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            new_x = self.spin_x.value()
            new_y = self.spin_y.value()
            item.setPos(new_x, new_y)

        self.scene.update()

    def on_color_clicked(self):
        color = QColorDialog.getColor()

        if color.isValid():
            hex_color = color.name()
            self.btn_color.setStyleSheet(f"background-color: {hex_color};")

            selected_items = self.scene.selectedItems()
            if not selected_items:
                return

            self.undo_stack.beginMacro("Change Color All")

            for item in selected_items:
                cmd = ChangeColorCommand(item, hex_color)
                self.undo_stack.push(cmd)

            self.undo_stack.endMacro()

    def update_width_ui(self, selected_items):
        self.spin_width.blockSignals(True)

        first_width = -1
        is_mixed = False

        def get_width(item):
            """Получить толщину объекта, учитывая Group"""
            if hasattr(item, "pen") and item.pen() is not None:
                return item.pen().width()
            # Для Group пытаемся получить толщину от первого ребенка
            if hasattr(item, "childItems"):
                children = item.childItems()
            if children:
                return get_width(children[0])
            return MIN_STROKE_WIDTH

        for i, item in enumerate(selected_items):
            w = get_width(item)

            if i == 0:
                first_width = w
            else:
                if w != first_width:
                    is_mixed = True
                    break

        if first_width > 0:
            if is_mixed:
                self.spin_width.setValue(first_width)
                self.spin_width.setStyleSheet("background-color: #fffacd;")
                self.spin_width.setToolTip("Выбраны объекты с разной толщиной")
            else:
                self.spin_width.setValue(first_width)
                self.spin_width.setStyleSheet("")
                self.spin_width.setToolTip("")

        self.spin_width.blockSignals(False)