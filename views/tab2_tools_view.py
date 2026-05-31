# views/tab1_scene_view.py
import os
from pathlib import Path

from PySide6.QtWidgets import QWidget, QFileDialog

from service.perspective_transformer import PerspectiveTransformer
from views.image_click_dialog import ImageClickDialog


class Tab2ToolsView(QWidget):
    def __init__(self, ui, parent_window):
        """
        ui: 传入的 Ui_Widget 实例，方便直接访问 tab1 内部的控件
        parent_window: 传入的 MainView 实例，方便调用 statusBar() 或作为 Dialog 的 parent
        """
        super().__init__()
        self.ui = ui
        self.window = parent_window

        self.image_dir_path = ""
        self.last_image_dir_path = "./"

        self.init_signals()
        self.image_path = ""
        self.np_points = []

    def init_signals(self):
        # 绑定信号与槽
        self.ui.button_select_skewed_image.clicked.connect(self.handle_open_image_dialog)
        self.ui.button_start_conv_images.clicked.connect(self.handle_start_task)

    def handle_open_image_dialog(self):
        image_path, _ = QFileDialog.getOpenFileName(
            self.window, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if not image_path:
            return
        self.image_path = image_path

        dialog = ImageClickDialog(image_path, max_points=4, connect_points=True, parent=self.window)
        dialog.points_selected.connect(self.handle_coordinates)
        dialog.exec()

    def handle_coordinates(self, points):
        print(f"Tab1 收到坐标: {points}")
        self.np_points = []
        for point in points:
            self.np_points.append((point.x, point.y))

        input_dir =os.path.dirname(self.image_path)
        self.window.statusBar().showMessage("透视点位采集完成: "+input_dir)
        self.ui.button_start_conv_images.setEnabled(True)

    def handle_start_task(self):
        input_dir =os.path.dirname(self.image_path)
        output_dir = os.path.join(input_dir, "processed_images")
        perspective_srv = PerspectiveTransformer(self.np_points, output_dir=output_dir)
        perspective_srv.transform_dir(input_dir)
