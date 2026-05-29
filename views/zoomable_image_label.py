import sys
from PySide6.QtCore import Qt, QPoint, Signal, QTimer
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QCursor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QDialog, QLabel, QScrollArea, QSpinBox, QCheckBox
)


# 1. 支持缩放、自定义打点数及连线的自定义 Label
class ZoomableImageLabel(QLabel):
    points_updated = Signal()

    def __init__(self, max_points, connect_points=True, parent=None):
        super().__init__(parent)
        self.max_points = max_points  # 最大允许点数
        self.connect_points = connect_points  # 是否连线

        self.orig_pixmap = QPixmap()
        self.scale_factor = 1.0
        self.raw_points = []  # 存储图片【原始像素】坐标

    def set_orig_pixmap(self, pixmap):
        self.orig_pixmap = pixmap
        self.scale_factor = 1.0
        self.raw_points = []
        self.update_size()

    def update_size(self):
        if self.orig_pixmap.isNull():
            return
        new_width = int(self.orig_pixmap.width() * self.scale_factor)
        new_height = int(self.orig_pixmap.height() * self.scale_factor)

        scaled_pixmap = self.orig_pixmap.scaled(
            new_width, new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)
        self.setFixedSize(scaled_pixmap.size())

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            angle_delta = event.angleDelta().y()
            if angle_delta > 0:
                self.scale_factor *= 1.1
            else:
                self.scale_factor /= 1.1

            self.scale_factor = max(0.1, min(self.scale_factor, 5.0))
            self.update_size()
            event.accept()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 动态判断：如果已经达到了设定的最大点数，则不再响应
            if len(self.raw_points) >= self.max_points:
                return

                # 使用 Qt 6 推荐的 position().toPoint() 规避 DeprecationWarning
            click_pos = event.position().toPoint()

            raw_x = int(click_pos.x() / self.scale_factor)
            raw_y = int(click_pos.y() / self.scale_factor)

            raw_x = max(0, min(raw_x, self.orig_pixmap.width() - 1))
            raw_y = max(0, min(raw_y, self.orig_pixmap.height() - 1))

            self.raw_points.append(QPoint(raw_x, raw_y))
            self.update()

            self.points_updated.emit()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.raw_points:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. 如果开启了连线配置，先画线段（让线处于点的下方，视觉效果更好）
        if self.connect_points and len(self.raw_points) > 1:
            line_pen = QPen(QColor(0, 150, 255), 3)  # 蓝色的线，粗细为 3
            line_pen.setStyle(Qt.PenStyle.SolidLine)
            painter.setPen(line_pen)

            # 将原始坐标转为当前缩放视图坐标，并依次连线
            for i in range(len(self.raw_points) - 1):
                p1 = self.raw_points[i]
                p2 = self.raw_points[i + 1]
                pt1 = QPoint(int(p1.x() * self.scale_factor), int(p1.y() * self.scale_factor))
                pt2 = QPoint(int(p2.x() * self.scale_factor), int(p2.y() * self.scale_factor))
                painter.drawLine(pt1, pt2)

        # 2. 绘制红点
        point_pen = QPen(QColor(255, 0, 0), 12)
        point_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(point_pen)

        for raw_p in self.raw_points:
            display_x = int(raw_p.x() * self.scale_factor)
            display_y = int(raw_p.y() * self.scale_factor)
            painter.drawPoint(QPoint(display_x, display_y))