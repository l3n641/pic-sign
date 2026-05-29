from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtWidgets import (
    QVBoxLayout,
    QDialog, QScrollArea
)

from .zoomable_image_label import ZoomableImageLabel
from service.project_struct import Point, Rectangle


class ImageClickDialog(QDialog):
    points_selected = Signal(list)

    def __init__(self, image_path, max_points, connect_points=False, parent=None ):
        super().__init__(parent)
        self.setWindowTitle(f"请点击 {max_points} 个点 | Ctrl+滚轮缩放")
        self.resize(800, 600)

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
