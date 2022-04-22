# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Oleg Frolov
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////
from typing import Optional

from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtWidgets import QGridLayout, QMainWindow, QWidget
from ToggleButton import ToggleButton


class MainWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        QMainWindow.__init__(self, parent)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background: #f6f6ff;")
        self.centralWidget = QWidget(self)

        self.customCheckBox = ToggleButton(self.centralWidget)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.addWidget(self.customCheckBox)

        self.setCentralWidget(self.centralWidget)
        self.center()

    def center(self):
        screen = QGuiApplication.screenAt(QCursor().pos())
        fg = self.frameGeometry()
        fg.moveCenter(screen.geometry().center())
        self.move(fg.topLeft())
