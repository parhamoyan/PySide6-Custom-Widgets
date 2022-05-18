# ///////////////////////////////////////////////////////////////
#
# https://www.youtube.com/watch?v=daVpOpvsCKQ&t=20s
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////

import math
import time

from perlin_noise import PerlinNoise as Noise
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

        self.start = 0
        self.step = 1
        self.rayon = 200
        self.message = "LOADING..."
        self.animation: Optional[QVariantAnimation] = None
        self.noise_generator1 = Noise(octaves=.8, seed=int(time.time()))
        self.noise_generator2 = Noise(octaves=.8, seed=int(time.time() + 1))
        self.start_animation()

    def start_animation(self) -> None:
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(60 * 1000)
        self.animation.setStartValue(self.start)
        self.animation.setEndValue(5000)
        self.animation.valueChanged.connect(self.update_start_angle)
        self.animation.start()

    def update_start_angle(self, new_value: float) -> None:
        self.start = new_value
        self.update()

    def get_deformed_point(self, angle: float, noise_generator: Noise) -> QPointF:
        radian_angle = math.radians(angle)
        _x = math.cos(radian_angle)
        _y = math.sin(radian_angle)
        offset = self.start / 100
        noise = noise_generator([_x + offset, _y + offset])
        c = self.rayon * (1 + noise/2.5)
        point = QPointF(_x * c, _y * c)
        return point

    def draw_deformed_circles(self, painter: QPainter) -> None:
        painter.save()

        painter.translate(self.rect().center())

        path1 = QPainterPath()
        path2 = QPainterPath()

        angle = 1
        path1.moveTo(self.get_deformed_point(angle, self.noise_generator1))
        path2.moveTo(self.get_deformed_point(angle, self.noise_generator2))
        while angle < 360:
            path1.lineTo(self.get_deformed_point(angle, self.noise_generator1))
            path2.lineTo(self.get_deformed_point(angle, self.noise_generator2))
            angle += self.step

        painter.drawPath(path1)
        painter.setBrush(QBrush(QColor("#ff2e63")))
        painter.drawPath(path2)
        painter.setBrush(QBrush(QColor("#082e63")))
        painter.drawPath(path2.intersected(path1))

        painter.restore()

    def draw_message(self, painter: QPainter) -> None:
        font = QFont("Ebrima", 30)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 10)
        painter.setFont(font)

        painter.setPen(QColor("white"))
        flags = Qt.AlignHCenter | Qt.AlignVCenter
        painter.restore()
        painter.drawText(self.rect(), flags, self.message)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor("#07d9d7")))
        painter.setPen(Qt.NoPen)

        self.draw_deformed_circles(painter)
        self.draw_message(painter)

        painter.end()
