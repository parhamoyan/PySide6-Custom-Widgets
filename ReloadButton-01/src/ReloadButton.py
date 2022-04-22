# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Margarita Ivanchikova
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////
from typing import Optional

from PySide6.QtCore import (QEasingCurve, QVariantAnimation,
                            QSequentialAnimationGroup)
from PySide6.QtGui import (QColor, Qt, QPainterPath, QPainter,
                           QBrush, QPen, QFont, QPaintEvent)
from PySide6.QtWidgets import QPushButton, QWidget


class ReloadButton(QPushButton):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        QPushButton.__init__(self, parent)
        self.setFixedSize(240, 100)
        self.setCursor(Qt.PointingHandCursor)

        # INIT ATTRIBUTES
        self.backgroundColor = QColor("#fefefe")
        self.iconColor = QColor("#094873")
        self.length = 6
        self.currentPercentage = .8
        self.animationDuration = 1000
        self.animationEasingCurve = QEasingCurve.InOutSine

        self.clicked.connect(self.startAnimations)

    def enterEvent(self, e) -> None:
        self.backgroundColor = QColor("#dafcdb")

    def leaveEvent(self, e) -> None:
        self.backgroundColor = QColor("#fefefe")

    def getHideArrowAnimation(self) -> QVariantAnimation:
        hideArrowAnimation = QVariantAnimation(self)
        hideArrowAnimation.setDuration(int(.2 * self.animationDuration))
        hideArrowAnimation.setStartValue(6)
        hideArrowAnimation.setEndValue(0)
        hideArrowAnimation.setEasingCurve(self.animationEasingCurve)
        hideArrowAnimation.valueChanged.connect(self.updateLength)
        return hideArrowAnimation

    def getTransitionAnimation(self) -> QVariantAnimation:
        transitionAnimation = QVariantAnimation(self)
        transitionAnimation.setDuration(int(.6 * self.animationDuration))
        transitionAnimation.setStartValue(self.currentPercentage)
        transitionAnimation.setEndValue(self.currentPercentage - .5)
        transitionAnimation.setEasingCurve(self.animationEasingCurve)
        transitionAnimation.valueChanged.connect(self.updatePercentage)
        return transitionAnimation

    def getShowArrowAnimation(self) -> QVariantAnimation:
        showArrowAnimation = QVariantAnimation(self)
        showArrowAnimation.setDuration(int(.2 * self.animationDuration))
        showArrowAnimation.setStartValue(0)
        showArrowAnimation.setEndValue(6)
        showArrowAnimation.setEasingCurve(self.animationEasingCurve)
        showArrowAnimation.valueChanged.connect(self.updateLength)
        return showArrowAnimation

    def startAnimations(self) -> None:
        seqGroup = QSequentialAnimationGroup(self)
        seqGroup.addAnimation(self.getHideArrowAnimation())
        seqGroup.addAnimation(self.getTransitionAnimation())
        seqGroup.addAnimation(self.getShowArrowAnimation())
        seqGroup.start()

    def updateLength(self, newValue: int) -> None:
        self.length = newValue
        self.update()

    def updatePercentage(self, newPercentage: float) -> None:
        self.currentPercentage = newPercentage
        if self.currentPercentage < 0:
            self.currentPercentage += 1
        if self.currentPercentage > 1:
            self.currentPercentage -= 1
        self.update()

    @staticmethod
    def trim(self, path: float, start: float) -> QPainterPath:
        newPath = QPainterPath()
        newPath.moveTo(int(path.pointAtPercent(start)))
        for i in range(1, 101):
            newPath.lineTo(int(path.pointAtPercent(start)))
            start += .38 / 100
            if start > 1:
                start -= 1
        return newPath

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.backgroundColor))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 20, 20)

        painter.setBrush(Qt.NoBrush)
        pen = QPen()
        pen.setColor(self.iconColor)
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        path = QPainterPath()
        w, h = 20, 40
        x, y = (100 - w) / 2, (self.height() - h) / 2
        path.addRoundedRect(x, y, w, h, w / 2, w / 2)

        percentage = self.currentPercentage
        animatedPath1 = self.trim(path, percentage)
        painter.drawPath(animatedPath1)

        point = path.pointAtPercent(.8)
        painter.drawLine(point.x(), point.y(), point.x() - self.length,
                         point.y() - self.length)
        painter.drawLine(point.x(), point.y(), point.x() + self.length,
                         point.y() - self.length)

        percentage = self.currentPercentage - .5
        if percentage < 0:
            percentage += 1
        if percentage > 1:
            percentage -= 1

        animatedPath2 = self.trim(path, percentage)
        painter.drawPath(animatedPath2)

        point = path.pointAtPercent(.3)
        point.setX(point.x() + 1)
        painter.drawLine(point.x(), point.y(), point.x() - self.length,
                         point.y() + self.length)
        painter.drawLine(point.x(), point.y(), point.x() + self.length,
                         point.y() + self.length)

        font = QFont()
        font.setPointSize(30)
        painter.setFont(font)

        painter.drawText(0, 0, self.width() - 30, self.height(),
                         Qt.AlignRight | Qt.AlignVCenter, "Reload")

        painter.end()
