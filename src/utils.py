import sys
import os

def resource_path(relative_path):
    """
    Получает абсолютный путь к ресурсу.
    Работает и для dev-режима, и для PyInstaller.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)