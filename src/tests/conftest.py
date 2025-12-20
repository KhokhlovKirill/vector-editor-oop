import pytest
import sys
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session", autouse=True)
def qapp():
    """
    Создает экземпляр QApplication один раз на весь запуск тестов.
    Это необходимо для работы любых классов Qt (цвета, геометрия, шрифты).
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app