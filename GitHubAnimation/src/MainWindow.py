# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Shubham Singh
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////
from typing import Optional

from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtWidgets import QGridLayout, QMainWindow, QWidget
from GitHubAnimation import GitHubAnimation


class MainWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        QMainWindow.__init__(self, parent)
        self.setStyleSheet("background: #111111;")
        self.centralWidget = QWidget(self)

        self.gitHubAnimation = GitHubAnimation(self.centralWidget)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.addWidget(self.gitHubAnimation)

        self.setCentralWidget(self.centralWidget)
        self.resize(600, 600)
        self.center()

    def center(self):
        screen = QGuiApplication.screenAt(QCursor().pos())
        fg = self.frameGeometry()
        fg.moveCenter(screen.geometry().center())
        self.move(fg.topLeft())
