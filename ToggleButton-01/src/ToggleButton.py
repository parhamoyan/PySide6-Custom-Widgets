# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Oleg Frolov
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////
from dataclasses import dataclass
from typing import Optional

from PySide6.QtCore import QPointF, QLineF
from PySide6.QtCore import Qt, QPoint, QEasingCurve, QParallelAnimationGroup, \
    QVariantAnimation
from PySide6.QtGui import QColor, QPainterPath, QPen, QPainter
from PySide6.QtWidgets import QCheckBox, QWidget
from TrimmablePainterPath import TrimmablePainterPath


@dataclass
class Element:
    x: float
    y: float


class QBezier:
    def __init__(self, p0, p1, p2, p3):
        self.x1, self.y1 = p0.x, p0.y
        self.x2, self.y2 = p1.x, p1.y
        self.x3, self.y3 = p2.x, p2.y
        self.x4, self.y4 = p3.x, p3.y

    def length(self, error=0.01):
        length_list = [0.0]  # Initialize the list with the starting length value
        self.add_if_close(length_list, error)
        length = length_list[0]  # Retrieve the modified length value
        return length

    def add_if_close(self, length_list, error):
        len_arc = 0
        len_arc += QLineF(QPointF(self.x1, self.y1), QPointF(self.x2, self.y2)).length()
        len_arc += QLineF(QPointF(self.x2, self.y2), QPointF(self.x3, self.y3)).length()
        len_arc += QLineF(QPointF(self.x3, self.y3), QPointF(self.x4, self.y4)).length()
        chord = QLineF(QPointF(self.x1, self.y1), QPointF(self.x4, self.y4)).length()

        if (len_arc - chord) > error:
            halves = self.split()
            halves[0].add_if_close(length_list, error)
            halves[1].add_if_close(length_list, error)
            return

        length_list[0] += len_arc

    def split(self):
        mid1 = Element((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
        mid2 = Element((self.x2 + self.x3) / 2, (self.y2 + self.y3) / 2)
        mid3 = Element((self.x3 + self.x4) / 2, (self.y3 + self.y4) / 2)
        mid4 = Element((mid1.x + mid2.x) / 2, (mid1.y + mid2.y) / 2)
        mid5 = Element((mid2.x + mid3.x) / 2, (mid2.y + mid3.y) / 2)
        midpoint = Element((mid4.x + mid5.x) / 2, (mid4.y + mid5.y) / 2)

        first_half = QBezier(Element(self.x1, self.y1), mid1, mid4, midpoint)
        second_half = QBezier(midpoint, mid5, mid3, Element(self.x4, self.y4))

        return first_half, second_half


class ToggleButton(QCheckBox):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        QCheckBox.__init__(self, parent)
        self.setFixedSize(200, 120)
        self.setCursor(Qt.PointingHandCursor)
        # INIT ATTRIBUTES
        self.percentage = .75
        self.animationDuration = .6 * 1000
        self.backgroundColor = QColor("#414141")
        self.indicatorColor = QColor("#ffffff")
        self.borderWidth = 24
        # CONNECT SIGNAL
        self.stateChanged.connect(self.startAnimation)

    def hitButton(self, pos: QPoint) -> None:
        return self.contentsRect().contains(pos)

    def getIndicatorColorAnimation(self) -> QVariantAnimation:
        indicatorColorAnimation = self.getQVariantAnimation()
        indicatorColorAnimation.valueChanged.connect(self.updateIndicatorColor)
        if self.isChecked():
            indicatorColorAnimation.setStartValue(QColor("#ffffff"))
            indicatorColorAnimation.setEndValue(QColor("#686868"))
        else:
            indicatorColorAnimation.setStartValue(QColor("#686868"))
            indicatorColorAnimation.setEndValue(QColor("#ffffff"))
        return indicatorColorAnimation

    def updateIndicatorColor(self, newColor) -> None:
        self.indicatorColor = newColor
        self.update()

    def getQVariantAnimation(self) -> QVariantAnimation:
        animation = QVariantAnimation(self)
        animation.setEasingCurve(QEasingCurve.OutBack)
        animation.setDuration(self.animationDuration)
        return animation

    def getTransitionAnimation(self) -> QVariantAnimation:
        transitionAnimation = self.getQVariantAnimation()
        transitionAnimation.valueChanged.connect(self.updatePercentage)
        transitionAnimation.setStartValue(self.percentage)
        transitionAnimation.setEndValue(self.percentage + .5)
        return transitionAnimation

    def updatePercentage(self, newValue) -> None:
        self.percentage = newValue
        if self.percentage > 1:
            self.percentage -= 1
        self.update()

    def startAnimation(self) -> None:
        parGroup = QParallelAnimationGroup(self)
        parGroup.addAnimation(self.getTransitionAnimation())
        parGroup.addAnimation(self.getIndicatorColorAnimation())
        parGroup.start()

    def drawAnimatedPath(self, painter: QPainter,
                         backgroundPath: QPainterPath) -> None:
        if self.percentage + 0.5 > 1:
            path1 = TrimmablePainterPath.trim(backgroundPath, self.percentage, 1)
            path2 = TrimmablePainterPath.trim(backgroundPath, 0, self.percentage + 0.5 - 1)
            animatedPath = path1 + path2
        else:
            animatedPath = TrimmablePainterPath.trim(backgroundPath, self.percentage, self.percentage + 0.5)

        painter.drawPath(animatedPath)

    def paintEvent(self, event: QPainter) -> None:
        # INIT PEN AND BACKGROUND COLOR
        pen = QPen()
        pen.setWidth(self.borderWidth)
        pen.setColor(self.backgroundColor)

        # INIT PAINTER
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(pen)

        # INIT & DRAW BACKGROUND PATH
        backgroundPath = QPainterPath()
        x, y = pen.width(), pen.width()
        w, h = self.width() - pen.width() * 2, self.height() - pen.width() * 2
        backgroundPath.addRoundedRect(x, y, w, h, h / 2, h / 2)
        painter.drawPath(backgroundPath)

        # SET INDICATOR COLOR
        pen.setColor(self.indicatorColor)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        # DRAW ANIMATED PATH
        self.drawAnimatedPath(painter, backgroundPath)

        # END PAINTER
        painter.end()
