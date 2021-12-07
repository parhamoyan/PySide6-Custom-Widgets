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
            backgroundColor = QColor("#414141"),
            indicatorColor = QColor("#ffffff"),
            borderWidth = 24,
            animationDuration = 800
            ):
        QCheckBox.__init__(self, parent=parent)
        self.setFixedSize(200, 120)
        self.setCursor(Qt.PointingHandCursor)
        # INIT ATTRIBUTES
        self.percentage = .75
        self.animationDuration = animationDuration
        self.backgroundColor = backgroundColor
        self.indicatorColor = indicatorColor
        self.borderWidth = borderWidth
        # INIT ANIMATIONS
        self.initTransitionAnimation()
        self.initIndicatorColorAnimation()
        # CONNECT SIGNAL
        self.stateChanged.connect(self.startAnimation)
    
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)
    
    def initIndicatorColorAnimation(self):
        self.indicatorColorAnimation = self.getQVariantAnimation()
        self.indicatorColorAnimation.valueChanged.connect(self.updateIndicatorColor)
    
    def reinitIndicatorColorAnimation(self):
        self.indicatorColorAnimation.setStartValue([QColor("#686868"), QColor("#ffffff")][self.isChecked()])
        self.indicatorColorAnimation.setEndValue([QColor("#686868"), QColor("#ffffff")][not self.isChecked()])
    
    def updateIndicatorColor(self, newColor):
        self.indicatorColor = newColor
        self.update()
    
    def getQVariantAnimation(self):
        animation = QVariantAnimation(self)
        animation.setEasingCurve(QEasingCurve.OutBack)
        animation.setDuration(self.animationDuration)
        return animation
    
    def initTransitionAnimation(self):
        self.transitionAnimation = self.getQVariantAnimation()
        self.transitionAnimation.valueChanged.connect(self.updatePercentage)
    
    def reinitTransitionAnimation(self):
        self.transitionAnimation.setStartValue(self.percentage)
        self.transitionAnimation.setEndValue(self.percentage+.5)

    def updatePercentage(self, newValue):
        self.percentage = newValue
        if self.percentage > 1:
            self.percentage -= 1
        self.update()

    def startAnimation(self, state):
        self.setDisabled(True)
        self.reinitTransitionAnimation()
        self.reinitIndicatorColorAnimation()
        parGroup = QParallelAnimationGroup(self)
        parGroup.addAnimation(self.transitionAnimation)
        parGroup.addAnimation(self.indicatorColorAnimation)
        parGroup.finished.connect(lambda: self.setDisabled(False))
        parGroup.start()
    
    def drawAnimatedPath(self):
        self.animatedPath = QPainterPath()
        percentage = self.percentage
        self.animatedPath.moveTo(self.backgroundPath.pointAtPercent(percentage))
        for i in range(1, self.width()+1):
            self.animatedPath.lineTo(self.backgroundPath.pointAtPercent(percentage))
            percentage += .5/self.width()
            if percentage > 1:
                percentage -= 1
        self.painter.drawPath(self.animatedPath)

    def paintEvent(self, e):
        # INIT PEN AND BACKGROUND COLOR
        pen = QPen()
        pen.setWidth(self.borderWidth)
        pen.setColor(self.backgroundColor)

        # INIT PAINTER
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.setPen(pen)

        # INIT & DRAW BACKGROUND PATH
        self.backgroundPath = QPainterPath()
        x, y = pen.width(), pen.width()
        w, h = self.width()-pen.width()*2, self.height()-pen.width()*2
        self.backgroundPath.addRoundedRect(x, y, w, h, h/2, h/2)
        self.painter.drawPath(self.backgroundPath)

        # SET INDICATOR COLOR
        pen.setColor(self.indicatorColor)
        pen.setCapStyle(Qt.RoundCap)
        self.painter.setPen(pen)

        # DRAW ANIMATED PATH
        self.drawAnimatedPath()
        
        # END PAINTER
        self.painter.end()