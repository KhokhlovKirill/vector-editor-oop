import sys
from PySide6.QtWidgets import QApplication

from src.constants import APP_STYLE
from src.app import VectorEditorWindow


def main():
    app = QApplication(sys.argv)

    app.setStyle(APP_STYLE)

    window = VectorEditorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
