import sys
from PySide6.QtCore import Qt, QPoint, Signal, QTimer
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QCursor, QKeyEvent
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QDialog, QLabel, QScrollArea, QSpinBox, QCheckBox
)


# 1. 支持缩放、自定义打点数、连线以及 Ctrl+Z 回退的自定义 Label
class ZoomableImageLabel(QLabel):
    points_updated = Signal()

    def __init__(self, max_points, connect_points=True, parent=None):
        super().__init__(parent)
        self.max_points = max_points  # 最大允许点数
        self.connect_points = connect_points  # 是否连线

        self.orig_pixmap = QPixmap()
        self.scale_factor = 1.0
        self.raw_points = []  # 存储图片【原始像素】坐标

        # 【关键改动】让 Label 可以接收键盘焦点，否则 keyPressEvent 不会触发
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

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
        # 点击时让组件主动获取焦点，确保接下来的键盘快捷键生效
        self.setFocus()

        if event.button() == Qt.MouseButton.LeftButton:
            # 如果已经达到了设定的最大点数，则不再响应
            if len(self.raw_points) >= self.max_points:
                return

            click_pos = event.position().toPoint()

            raw_x = int(click_pos.x() / self.scale_factor)
            raw_y = int(click_pos.y() / self.scale_factor)

            raw_x = max(0, min(raw_x, self.orig_pixmap.width() - 1))
            raw_y = max(0, min(raw_y, self.orig_pixmap.height() - 1))

            self.raw_points.append(QPoint(raw_x, raw_y))
            self.update()

            self.points_updated.emit()

    # 【新增功能】监听键盘事件，实现 Ctrl + Z 回退
    def keyPressEvent(self, event: QKeyEvent):
        # 检查是否按下了 Ctrl 键（或 Mac 上的 Command 键）并且按键是 Z
        if event.key() == Qt.Key.Key_Z and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            if self.raw_points:
                self.raw_points.pop()  # 移除最后一个点
                self.update()  # 触发重绘（红点和连线会自动更新）
                self.points_updated.emit()  # 通知外部点位更新
                event.accept()  # 标记该事件已被处理
                return

        # 其他按键交给父类默认处理
        super().keyPressEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.raw_points:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. 如果开启了连线配置，先画线段
        if self.connect_points and len(self.raw_points) > 1:
            line_pen = QPen(QColor(0, 150, 255), 3)
            line_pen.setStyle(Qt.PenStyle.SolidLine)
            painter.setPen(line_pen)

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