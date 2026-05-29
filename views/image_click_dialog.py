from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtWidgets import (
    QVBoxLayout,
    QDialog
)

from .clickable_label import ClickableLabel


class ImageClickDialog(QDialog):
    points_selected = Signal(list)

    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("请点击选择两个点")

        self.pixmap = QPixmap(image_path)
        self.points = []
        self.is_completed = False  # 防止延迟期间重复点击

        layout = QVBoxLayout(self)

        # 使用我们自定义的 ClickableLabel
        self.image_label = ClickableLabel(self)
        self.image_label.setPixmap(self.pixmap)

        # 设置鼠标为十字准星
        self.image_label.setCursor(QCursor(Qt.CursorShape.CrossCursor))

        layout.addWidget(self.image_label)
        self.setLayout(layout)
        self.adjustSize()

    def mousePressEvent(self, event):
        if self.is_completed:
            return

        # 获取鼠标相对于 image_label 的坐标
        label_pos = self.image_label.mapFrom(self, event.pos())

        # 确保点击在图片有效范围内
        if self.image_label.rect().contains(label_pos):
            self.points.append(label_pos)

            # 把坐标同步给 Label，让它立刻在自己身上画出红点
            self.image_label.set_points(self.points)

            if len(self.points) == 2:
                self.is_completed = True
                # 延迟 500 毫秒关闭，让用户看清第二个红点
                QTimer.singleShot(500, self.finish_and_close)

    def finish_and_close(self):
        # 转换为普通元组列表传回主窗口
        points_list = [(p.x(), p.y()) for p in self.points]
        self.points_selected.emit(points_list)
        self.accept()
