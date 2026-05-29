from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import (
    QLabel
)


# 1. 自定义一个 QLabel，让它自己负责显示图片和画红点
class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []

    def set_points(self, points):
        self.points = points
        self.update()  # 触发自身的重绘

    def paintEvent(self, event):
        super().paintEvent(event)  # 先让 QLabel 正常绘制底图

        if not self.points:
            return

        # 直接在 QLabel 自身表面绘制红点
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # 抗锯齿

        pen = QPen(QColor(255, 0, 0), 12)  # 红色，粗细为 12 像素
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        for point in self.points:
            # 这里的坐标直接对应 Label 内部，不需要任何坐标转换
            painter.drawPoint(point)
