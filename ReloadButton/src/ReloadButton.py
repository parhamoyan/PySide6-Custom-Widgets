# ///////////////////////////////////////////////////////////////
#
# Copyright 2021 by Parham Oyan and Margarita Ivanchikova
# All rights reserved.
#
# ///////////////////////////////////////////////////////////////

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class ReloadButton(QPushButton):
    def __init__(
            self,
            parent = None,
            animationDuration = 1000,
            animationEasingCurve = QEasingCurve.InOutSine
            ):
        QPushButton.__init__(self, parent=parent)
        self.setFixedSize(240, 100)
        self.setCursor(Qt.PointingHandCursor)

        # INIT ATTRIBUTES
        self.backgroundColor = QColor("#fefefe")
        self.iconColor = QColor("#094873")
        self.length = 6
        self.currentPercentage = .8
        self.animationDuration = animationDuration
        self.animationEasingCurve = animationEasingCurve

        self.clicked.connect(self.startAnimations)
    
    def enterEvent(self, e):
        self.backgroundColor = QColor("#dafcdb")

    def leaveEvent(self, e):
        self.backgroundColor = QColor("#fefefe")
    
    def initHideArrowAnimation(self):
        self.hideArrowAnimation = QVariantAnimation(self)
        self.hideArrowAnimation.setDuration(.2*self.animationDuration)
        self.hideArrowAnimation.setStartValue(6)
        self.hideArrowAnimation.setEndValue(0)
        self.hideArrowAnimation.setEasingCurve(self.animationEasingCurve)
        self.hideArrowAnimation.valueChanged.connect(self.updateLength)

    def initTransitionAnimation(self):
        self.transitionAnimation = QVariantAnimation(self)
        self.transitionAnimation.setDuration(.6*self.animationDuration)
        self.transitionAnimation.setStartValue(self.currentPercentage)
        self.transitionAnimation.setEndValue(self.currentPercentage-.5)
        self.transitionAnimation.setEasingCurve(self.animationEasingCurve)
        self.transitionAnimation.valueChanged.connect(self.updatePercentage)

    def initShowArrowAnimation(self):
        self.showArrowAnimation = QVariantAnimation(self)
        self.showArrowAnimation.setDuration(.2*self.animationDuration)
        self.showArrowAnimation.setStartValue(0)
        self.showArrowAnimation.setEndValue(6)
        self.showArrowAnimation.setEasingCurve(self.animationEasingCurve)
        self.showArrowAnimation.valueChanged.connect(self.updateLength)
        
    def startAnimations(self):
        self.initHideArrowAnimation()
        self.initTransitionAnimation()
        self.initShowArrowAnimation()
        self.seqGroup = QSequentialAnimationGroup(self)
        self.seqGroup.addAnimation(self.hideArrowAnimation)
        self.seqGroup.addAnimation(self.transitionAnimation)
        self.seqGroup.addAnimation(self.showArrowAnimation)
        self.seqGroup.start()
    
    def updateLength(self, newValue):
        self.length = newValue
        self.update()
    
    def updatePercentage(self, newPercentage):
        self.currentPercentage = newPercentage
        if self.currentPercentage < 0:
            self.currentPercentage += 1
        if self.currentPercentage > 1:
            self.currentPercentage -= 1
        self.update()
    
    def trim(self, path, start):
        newPath = QPainterPath()
        newPath.moveTo(path.pointAtPercent(start))
        for i in range(1, 101):
            newPath.lineTo(path.pointAtPercent(start))
            start += .38/100
            if start > 1:
                start -= 1
        return newPath
        
    
    def paintEvent(self, e):
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
        x, y = (100-w)/2, (self.height()-h)/2
        path.addRoundedRect(x, y, w, h, w/2, w/2)
        
        percentage = self.currentPercentage
        animatedPath1 = self.trim(path, percentage)
        painter.drawPath(animatedPath1)

        point = path.pointAtPercent(.8)
        painter.drawLine(point.x(), point.y(), point.x()-self.length, point.y()-self.length)
        painter.drawLine(point.x(), point.y(), point.x()+self.length, point.y()-self.length)

        percentage = self.currentPercentage-.5
        if percentage < 0:
            percentage += 1
        if percentage > 1:
            percentage -= 1

        animatedPath2 = self.trim(path, percentage)
        painter.drawPath(animatedPath2)

        point = path.pointAtPercent(.3)
        point.setX(point.x()+1)
        painter.drawLine(point.x(), point.y(), point.x()-self.length, point.y()+self.length)
        painter.drawLine(point.x(), point.y(), point.x()+self.length, point.y()+self.length)

        font = QFont()
        font.setPointSize(30)
        painter.setFont(font)

        painter.drawText(0, 0, self.width()-30, self.height(), Qt.AlignRight|Qt.AlignVCenter, "Reload")

        painter.end()