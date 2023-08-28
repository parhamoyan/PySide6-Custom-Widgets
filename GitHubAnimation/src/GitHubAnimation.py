# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Shubham Singh
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////
from typing import Optional

from PySide6.QtCore import QPointF, Qt, QVariantAnimation, QTimer
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QPainterPath, QPen
from PySide6.QtWidgets import QWidget

from TrimmablePainterPath import TrimmablePainterPath


class GitHubAnimation(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedSize(500, 500)
        self.github_path = self.create_github_path()
        self.github_path_rect = self.github_path.boundingRect()
        self.end_percentage = 0
        self.start_animation()
        self.timer = QTimer()
        self.timer.setInterval(3.5 * 1000)
        self.timer.timeout.connect(self.start_animation)
        self.timer.start()

    def create_github_path(self) -> QPainterPath:
        path = QPainterPath()
        path.moveTo(QPointF(243.77, 483.38))

        # right leg
        path.lineTo(QPointF(243.77, 441.77))
        path.lineTo(QPointF(243.79, 441.46))
        path.cubicTo(QPointF(244.53, 431), QPointF(240.68, 420.73), QPointF(233.25, 413.32))

        # right arc
        path.cubicTo(QPointF(267.46, 409.95), QPointF(303, 397.16), QPointF(303, 338.47))
        path.cubicTo(QPointF(303, 323.32), QPointF(297.11, 308.76), QPointF(286.56, 297.86))

        # right ear
        path.cubicTo(QPointF(291.84, 284.47), QPointF(291.33, 269.84), QPointF(285.57, 256.94))
        path.moveTo(QPointF(285.88, 257.63))
        path.cubicTo(QPointF(285.88, 257.63), QPointF(273.17, 253.87), QPointF(243.77, 273.54))

        # top head
        path.lineTo(QPointF(243.37, 273.43))
        path.cubicTo(QPointF(218.94, 266.9), QPointF(193.21, 266.9), QPointF(168.78, 273.43))

        # left ear
        path.cubicTo(QPointF(138.98, 253.87), QPointF(126.28, 257.63), QPointF(126.28, 257.63))
        path.cubicTo(QPointF(120.67, 270.81), QPointF(120.42, 285.45), QPointF(125.49, 298.63))

        # left arc
        path.cubicTo(QPointF(115.05, 308.76), QPointF(109.15, 323.33), QPointF(109.15, 338.48))
        path.cubicTo(QPointF(109.15, 397.06), QPointF(144.69, 409.85), QPointF(178.51, 414.04))

        # left leg
        path.lineTo(QPointF(178.48, 414.07))
        path.cubicTo(QPointF(171.34, 421.45), QPointF(167.67, 431.52), QPointF(168.38, 441.76))
        path.lineTo(QPointF(168.38, 483.38))

        # tail
        path.moveTo(QPointF(166, 451.13))
        path.cubicTo(QPointF(114.54, 467.25), QPointF(114.54, 424.25), QPointF(93, 418.88))

        return path

    def start_animation(self) -> None:
        animation = QVariantAnimation(self)
        animation.setDuration(3 * 1000)
        animation.valueChanged.connect(self.update_end_percentage)
        animation.setStartValue(0)
        animation.setEndValue(150)
        animation.start()

    def update_end_percentage(self, newValue) -> None:
        self.end_percentage = newValue
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen()
        pen.setWidth(6)
        pen.setColor(QColor("#414141"))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        translation = self.rect().center().toPointF() - self.github_path_rect.center()
        painter.translate(translation)

        # DRAW BACKGROUND
        painter.drawPath(self.github_path)

        # DRAW BLACK CIRCLE OR HORIZONTAL ROUNDED RECT
        pen.setColor(QColor("white"))
        pen.setWidth(8)
        painter.setPen(pen)
        _start = max(0, self.end_percentage/100-0.5)
        _end = min(self.end_percentage/100, 1)
        painter.drawPath(TrimmablePainterPath.trim(self.github_path, _start, _end))

        painter.end()
