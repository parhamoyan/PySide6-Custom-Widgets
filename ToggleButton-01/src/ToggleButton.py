# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Oleg Frolov
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////
from typing import Optional

from PySide6.QtGui import QColor, QPainterPath, QPen, QPainter
from PySide6.QtCore import Qt, QPoint, QEasingCurve, QParallelAnimationGroup, \
    QVariantAnimation
from PySide6.QtWidgets import QCheckBox, QWidget


class ToggleButton(QCheckBox):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        QCheckBox.__init__(self, parent)
        self.setFixedSize(200, 120)
        self.setCursor(Qt.PointingHandCursor)
        # INIT ATTRIBUTES
        self.percentage = .75
        self.animationDuration = 800
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
        match self.isChecked():
            case True:
                indicatorColorAnimation.setStartValue(QColor("#ffffff"))
                indicatorColorAnimation.setEndValue(QColor("#686868"))
            case False:
                indicatorColorAnimation.setStartValue(QColor("#ffffff"))
                indicatorColorAnimation.setEndValue(QColor("#686868"))
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
        animatedPath = QPainterPath()
        percentage = self.percentage
        animatedPath.moveTo(backgroundPath.pointAtPercent(percentage))
        for i in range(1, self.width() + 1):
            animatedPath.lineTo(backgroundPath.pointAtPercent(percentage))
            percentage += .5 / self.width()
            if percentage > 1:
                percentage -= 1
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
