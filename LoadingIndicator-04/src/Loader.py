# ///////////////////////////////////////////////////////////////
#
# https://www.youtube.com/watch?v=daVpOpvsCKQ&t=20s
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////

from typing import Optional

from PySide6.QtCore import QVariantAnimation, QPointF
from PySide6.QtGui import (QPainter, Qt, QPaintEvent, QColor, QBrush,
                           QPainterPath, QFont)
from PySide6.QtWidgets import QFrame, QWidget


class Loader(QFrame):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        QFrame.__init__(self, parent)

        self.setFrameShape(QFrame.NoFrame)
        self.setFixedSize(600, 600)

        self.step = 30
        self.rayon = 240
        self.side = 20
        self.start_angle = 0
        self.index = -1

        self.offsets = [0 for _ in range(12)]

        self.animation: Optional[QVariantAnimation] = None

        self.start_animation()

    def start_animation(self) -> None:
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(30 * 1000)
        self.animation.setStartValue(self.start_angle)
        self.animation.setEndValue(self.start_angle + 360)
        self.animation.valueChanged.connect(self.update_angle)
        self.animation.setLoopCount(-1)
        self.animation.start()

    def update_angle(self, new_value: float) -> None:
        self.start_angle = new_value
        if self.start_angle % 30 == 0:
            self.index = int(self.start_angle // 30) - 1
            self.start_offset_animation()
        self.update()

    def start_offset_animation(self):
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(2 * 1000)
        self.animation.setStartValue(self.offsets[self.index])
        self.animation.setEndValue(self.rayon - 20*(self.index+1))
        self.animation.valueChanged.connect(self.update_offset)
        self.animation.start()

    def update_offset(self, new_value):
        self.offsets[self.index] = new_value
        self.update()

    def draw_rectangles(self, painter: QPainter):
        painter.save()
        painter.translate(self.rect().center())
        painter.rotate(270)

        _y = -self.side // 2
        angle = self.index * 30
        painter.rotate(angle)
        while angle < 360:
            painter.rotate(self.step)
            i = angle // 30
            _x = self.rayon - self.side - int(self.offsets[i])
            if i != self.index:
                painter.drawRect(_x, _y, self.side, self.side)
            angle += self.step

        painter.restore()

        painter.save()
        painter.translate(self.rect().center())
        painter.rotate(self.start_angle)
        angle = 0
        while angle < self.index * 30:
            painter.rotate(self.step)
            i = angle // 30
            _x = self.rayon - self.side - int(self.offsets[i])
            if i != self.index:
                painter.drawRect(_x, _y, self.side, self.side)
            angle += self.step
        painter.drawRect(_x, _y, self.side, self.side)
        painter.restore()

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor("#fefefe")))
        painter.setPen(Qt.NoPen)

        # self.draw_rectangles(painter)

        painter.save()

        painter.translate(self.rect().center())

        painter.rotate(270)
        painter.rotate(self.start_angle)
        painter.setOpacity(.3)
        painter.drawRect(0, -self.side // 2, self.rayon, self.side)
        painter.setOpacity(1)

        painter.restore()

        painter.end()
