from PySide6.QtCore import QTimer
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtWidgets import (
    QVBoxLayout,
    QDialog, QScrollArea
)

from service.project_struct import Point
from .zoomable_image_label import ZoomableImageLabel


class ImageClickDialog(QDialog):
    points_selected = Signal(list)

    def __init__(self, image_path, max_points, connect_points=False, parent=None, window_size=None):
        super().__init__(parent)
        self.setWindowTitle(f"请点击 {max_points} 个点 | Ctrl+滚轮缩放")
        # 2. 判断是否传递了 size 参数
        if window_size is not None:
            # 如果传的是元组或列表，如 (800, 600)
            if isinstance(window_size, (tuple, list)) and len(window_size) == 2:
                self.resize(window_size[0], window_size[1])
            # 如果传的是 QSize 对象
            else:
                self.resize(window_size)
        else:
            # 3. 如果没传，则默认窗口最大化
            self.setWindowState(Qt.WindowMaximized)

        layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(False)

        # 将配置参数透传给自定义 Label
        self.image_label = ZoomableImageLabel(max_points, connect_points, self)
        pixmap = QPixmap(image_path)
        self.image_label.set_orig_pixmap(pixmap)
        self.image_label.setCursor(QCursor(Qt.CursorShape.CrossCursor))

        self.image_label.points_updated.connect(self.check_points_count)

        self.scroll_area.setWidget(self.image_label)
        layout.addWidget(self.scroll_area)

    def check_points_count(self):
        # 满足用户指定的自定义点数时自动关闭
        if len(self.image_label.raw_points) == self.image_label.max_points:
            QTimer.singleShot(400, self.finish_and_close)

    def finish_and_close(self):
        points_list = [Point(p.x(), p.y()) for p in self.image_label.raw_points]
        self.points_selected.emit(points_list)
        self.accept()
