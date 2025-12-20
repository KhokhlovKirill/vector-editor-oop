from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QSpinBox, QPushButton, QFrame, QColorDialog, QHBoxLayout, QDoubleSpinBox)
from PySide6.QtCore import Qt


class PropertiesPanel(QWidget):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene

        self._init_ui()

        self.scene.selectionChanged.connect(self.on_selection_changed)

    def _init_ui(self):
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #f0f0f0; border-left: 1px solid #ccc;")

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
        self.spin_width.setRange(1, 50)  # Мин 1, Макс 50 пикселей
        self.spin_width.valueChanged.connect(self.on_width_changed)
        layout.addWidget(self.spin_width)

        layout.addWidget(QLabel("Цвет линии:"))
        self.btn_color = QPushButton("Pick Color")
        self.btn_color.setFixedHeight(30)
        self.btn_color.clicked.connect(self.on_color_clicked)

        geo_layout = QHBoxLayout()

        self.spin_x = QDoubleSpinBox()
        self.spin_x.setRange(-10000, 10000)
        self.spin_x.setPrefix("X: ")
        self.spin_x.valueChanged.connect(self.on_geo_changed)

        self.spin_y = QDoubleSpinBox()
        self.spin_y.setRange(-10000, 10000)
        self.spin_y.setPrefix("Y: ")
        self.spin_y.valueChanged.connect(self.on_geo_changed)

        geo_layout.addWidget(self.spin_x)
        geo_layout.addWidget(self.spin_y)
        layout.addLayout(geo_layout)

        layout.addWidget(self.btn_color)

        layout.addStretch()

        self.setEnabled(False)

    def on_selection_changed(self):
        """Вызывается автоматически при клике по фигурам"""
        selected_items = self.scene.selectedItems()

        if not selected_items:
            self.setEnabled(False)
            self.spin_width.setValue(1)
            self.btn_color.setStyleSheet("background-color: transparent")
            return

        self.setEnabled(True)

        item = selected_items[0]

        current_width = 1
        current_color = "#000000"

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
        """
        Вызывается, когда пользователь меняет значение в SpinBox.
        value: int (новая толщина)
        """
        selected_items = self.scene.selectedItems()

        for item in selected_items:
            if hasattr(item, "set_stroke_width"):
                item.set_stroke_width(value)
            elif hasattr(item, "pen") and item.pen() is not None:
                new_pen = item.pen()
                new_pen.setWidth(value)
                item.setPen(new_pen)

        self.scene.update()

    def on_geo_changed(self, value):
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            new_x = self.spin_x.value()
            new_y = self.spin_y.value()
            item.setPos(new_x, new_y)

        self.scene.update()

    def on_color_clicked(self):
        """Открывает диалог выбора цвета"""
        color = QColorDialog.getColor(title="Выберите цвет линии")

        if color.isValid():
            hex_color = color.name()

            self.btn_color.setStyleSheet(
                f"background-color: {hex_color}; border: 1px solid gray;"
            )

            selected_items = self.scene.selectedItems()
            for item in selected_items:
                if hasattr(item, "set_active_color"):
                    item.set_active_color(hex_color)
                elif hasattr(item, "setPen"):
                    pen = item.pen()
                    pen.setColor(color)
                    item.setPen(pen)

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
            return 1  # Дефолтное значение

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