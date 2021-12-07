# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Oleg Frolov
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class ToggleButton(QCheckBox):
    def __init__(
            self,
            parent = None,
            leftIconColor = QColor("#ffffff"),
            rightIconColor = QColor("#333333"),
            animationDuration = 800
            ):
        QCheckBox.__init__(self, parent=parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(200, 100)
        self.addShadow()
        self.stateChanged.connect(self.startAnimations)
        self.blackRectWidth = self.height()
        self.blackRectXPos = 0
        self.leftIconColor = leftIconColor
        self.rightIconColor = rightIconColor
        self.animationDuration = animationDuration

    def newQVariantAnimation(self):
        animation = QVariantAnimation(self)
        animation.setDuration(self.animationDuration)
        animation.setEasingCurve(QEasingCurve.InOutExpo)
        return animation

    def initBlackRectWidthAnimation(self):
        self.blackRectWidthAnimation = self.newQVariantAnimation()
        self.blackRectWidthAnimation.setStartValue(self.blackRectWidth)
        self.blackRectWidthAnimation.setEndValue([self.width(), self.height()][not self.isChecked()])
        self.blackRectWidthAnimation.valueChanged.connect(self.updateBlackRectWidth)
    
    def initBlackRectXPosAnimation(self):
        self.blackRectXPosAnimation = self.newQVariantAnimation()
        self.blackRectXPosAnimation.setStartValue(self.blackRectXPos)
        self.blackRectXPosAnimation.setEndValue([self.width()//2, 0][not self.isChecked()])
        self.blackRectXPosAnimation.setDuration(self.animationDuration)
        self.blackRectXPosAnimation.valueChanged.connect(self.updateBlackRectXPos)

    def initLeftIconColorAnimation(self):
        self.leftIconColorAnimation = QVariantAnimation(self)
        self.leftIconColorAnimation.setStartValue(self.leftIconColor)
        self.leftIconColorAnimation.setEndValue(QColor(["#333333", "#ffffff"][not self.isChecked()]))
        self.leftIconColorAnimation.setDuration(self.animationDuration)
        self.leftIconColorAnimation.setEasingCurve(QEasingCurve.InOutExpo)
        self.leftIconColorAnimation.valueChanged.connect(self.updateLeftIconColor)

    def initRightIconColorAnimation(self):
        self.rightIconColorAnimation = QVariantAnimation(self)
        self.rightIconColorAnimation.setStartValue(self.rightIconColor)
        self.rightIconColorAnimation.setEndValue(QColor(["#333333", "#ffffff"][self.isChecked()]))
        self.rightIconColorAnimation.setDuration(self.animationDuration)
        self.rightIconColorAnimation.setEasingCurve(QEasingCurve.InOutExpo)
        self.rightIconColorAnimation.valueChanged.connect(self.updateRightIconColor)

    def startAnimations(self):
        self.setDisabled(True)
        self.initBlackRectWidthAnimation()
        self.initBlackRectXPosAnimation()
        self.initLeftIconColorAnimation()
        self.initLeftIconColorAnimation()
        self.initRightIconColorAnimation()

        parGroup1 = QParallelAnimationGroup(self)
        parGroup1.addAnimation([self.blackRectXPosAnimation, self.blackRectWidthAnimation][self.isChecked()])

        parGroup2 = QParallelAnimationGroup(self)
        parGroup2.addAnimation([self.blackRectXPosAnimation, self.blackRectWidthAnimation][not self.isChecked()])  
        parGroup2.addAnimation(self.leftIconColorAnimation)
        parGroup2.addAnimation(self.rightIconColorAnimation)

        secGroup = QSequentialAnimationGroup(self)
        secGroup.addAnimation(parGroup1)
        secGroup.addAnimation(parGroup2)
        secGroup.finished.connect(lambda: self.setDisabled(False))
        secGroup.start()
    
    def updateBlackRectWidth(self, newValue):
        self.blackRectWidth = newValue
        self.update()

    def updateBlackRectXPos(self, newValue):
        self.blackRectXPos = newValue
        self.update()

    def updateLeftIconColor(self, newColor):
        self.leftIconColor = newColor
        self.update()
    
    def updateRightIconColor(self, newColor):
        self.rightIconColor = newColor
        self.update()

    def addShadow(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setXOffset(3)
        self.shadow.setYOffset(3)
        self.shadow.setBlurRadius(80)
        self.shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(self.shadow)
    
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        # DRAW BACKGROUND
        p.setBrush(QBrush(QColor("white")))
        x, y = 0, 0
        w, h = self.width(), self.height()
        radius = self.height()/2
        p.drawRoundedRect(x, y, w, h, radius, radius)
        
        # DRAW BLACK CIRCLE OR HORIZONTAL ROUNDED RECT
        p.setBrush(QBrush(QColor("#333333")))
        p.drawRoundedRect(x+self.blackRectXPos, y, (self.blackRectWidth-self.blackRectXPos), \
            self.height(), self.height()/2, self.height()/2)

        # DRAW WHITE CIRCLE
        p.setBrush(QBrush(self.leftIconColor))
        r1 = 24
        p.drawEllipse(x+(self.height()-r1)/2, y+(self.height()-r1)/2, r1, r1)

        # DRAW VERTICAL BLACK ROUNDED RECT
        p.setBrush(QBrush(self.rightIconColor))
        p.drawRoundedRect(x+self.width()*.75-6, y+(self.height()-40)/2, \
             12, 40, 6, 6)
        p.end()