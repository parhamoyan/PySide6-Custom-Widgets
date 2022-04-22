# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Oleg Frolov
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////
from typing import Optional

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ToggleButton(QCheckBox):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        QCheckBox.__init__(self, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(200, 100)
        self.addShadow()
        self.stateChanged.connect(self.startAnimations)
        self.blackRectWidth = self.height()
        self.blackRectXPos = 0
        self.leftIconColor = QColor("#ffffff")
        self.rightIconColor = QColor("#333333")
        self.animationDuration = 800

    def newQVariantAnimation(self) -> QVariantAnimation:
        animation = QVariantAnimation(self)
        animation.setDuration(self.animationDuration)
        animation.setEasingCurve(QEasingCurve.InOutExpo)
        return animation

    def getBlackRectWidthAnimation(self) -> QVariantAnimation:
        blackRectWidthAnimation = self.newQVariantAnimation()
        blackRectWidthAnimation.setStartValue(self.blackRectWidth)
        blackRectWidthAnimation.setEndValue(
            [self.width(), self.height()][not self.isChecked()])
        blackRectWidthAnimation.valueChanged.connect(
            self.updateBlackRectWidth)
        return blackRectWidthAnimation

    def getBlackRectXPosAnimation(self) -> QVariantAnimation:
        blackRectXPosAnimation = self.newQVariantAnimation()
        blackRectXPosAnimation.setStartValue(self.blackRectXPos)
        blackRectXPosAnimation.setEndValue(
            [self.width() // 2, 0][not self.isChecked()])
        blackRectXPosAnimation.setDuration(self.animationDuration)
        blackRectXPosAnimation.valueChanged.connect(
            self.updateBlackRectXPos)
        return blackRectXPosAnimation

    def getLeftIconColorAnimation(self) -> QVariantAnimation:
        leftIconColorAnimation = QVariantAnimation(self)
        leftIconColorAnimation.setStartValue(self.leftIconColor)
        leftIconColorAnimation.setEndValue(
            QColor(["#333333", "#ffffff"][not self.isChecked()]))
        leftIconColorAnimation.setDuration(self.animationDuration)
        leftIconColorAnimation.setEasingCurve(QEasingCurve.InOutExpo)
        leftIconColorAnimation.valueChanged.connect(
            self.updateLeftIconColor)
        return leftIconColorAnimation

    def getRightIconColorAnimation(self) -> QVariantAnimation:
        rightIconColorAnimation = QVariantAnimation(self)
        rightIconColorAnimation.setStartValue(self.rightIconColor)
        rightIconColorAnimation.setEndValue(
            QColor(["#333333", "#ffffff"][self.isChecked()]))
        rightIconColorAnimation.setDuration(self.animationDuration)
        rightIconColorAnimation.setEasingCurve(QEasingCurve.InOutExpo)
        rightIconColorAnimation.valueChanged.connect(
            self.updateRightIconColor)
        return rightIconColorAnimation

    def startAnimations(self) -> None:
        parGroup1 = QParallelAnimationGroup(self)
        match self.isChecked():
            case True:
                parGroup1.addAnimation(self.getBlackRectWidthAnimation())
            case False:
                parGroup1.addAnimation(self.getBlackRectXPosAnimation())

        parGroup2 = QParallelAnimationGroup(self)
        match self.isChecked():
            case True:
                parGroup2.addAnimation(self.getBlackRectXPosAnimation())
            case False:
                parGroup2.addAnimation(self.getBlackRectWidthAnimation())
        parGroup2.addAnimation(self.getLeftIconColorAnimation())
        parGroup2.addAnimation(self.getRightIconColorAnimation())

        secGroup = QSequentialAnimationGroup(self)
        secGroup.addAnimation(parGroup1)
        secGroup.addAnimation(parGroup2)
        secGroup.finished.connect(lambda: self.setDisabled(False))
        secGroup.start()

    def updateBlackRectWidth(self, newValue) -> None:
        self.blackRectWidth = newValue
        self.update()

    def updateBlackRectXPos(self, newValue) -> None:
        self.blackRectXPos = newValue
        self.update()

    def updateLeftIconColor(self, newColor) -> None:
        self.leftIconColor = newColor
        self.update()

    def updateRightIconColor(self, newColor) -> None:
        self.rightIconColor = newColor
        self.update()

    def addShadow(self) -> None:
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setXOffset(3)
        self.shadow.setYOffset(3)
        self.shadow.setBlurRadius(80)
        self.shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(self.shadow)

    def hitButton(self, pos: QPoint) -> None:
        return self.contentsRect().contains(pos)

    def paintEvent(self, event: QPaintEvent) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        # DRAW BACKGROUND
        p.setBrush(QBrush(QColor("white")))
        x, y = 0, 0
        w, h = self.width(), self.height()
        radius = self.height() / 2
        p.drawRoundedRect(x, y, w, h, radius, radius)

        # DRAW BLACK CIRCLE OR HORIZONTAL ROUNDED RECT
        p.setBrush(QBrush(QColor("#333333")))
        p.drawRoundedRect(x + self.blackRectXPos, y,
                          (self.blackRectWidth - self.blackRectXPos),
                          self.height(), self.height() / 2, self.height() / 2)

        # DRAW WHITE CIRCLE
        p.setBrush(QBrush(self.leftIconColor))
        r1 = 24
        p.drawEllipse(x + (self.height() - r1) / 2,
                      y + (self.height() - r1) / 2, r1, r1)

        # DRAW VERTICAL BLACK ROUNDED RECT
        p.setBrush(QBrush(self.rightIconColor))
        p.drawRoundedRect(x + self.width() * .75 - 6,
                          y + (self.height() - 40) / 2,
                          12, 40, 6, 6)
        p.end()
