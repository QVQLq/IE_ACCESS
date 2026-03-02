#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像加密与测评系统 - 主入口
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("图像加密与测评系统")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
