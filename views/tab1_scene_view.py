# views/tab1_scene_view.py
import os
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QListWidgetItem, QMessageBox, QFileDialog

from service.image_manage import ImageManage
from service.project_struct import Point, Rectangle
from service.scene_clusterer import SceneClassifier
from views.image_click_dialog import ImageClickDialog


class Tab1SceneView(QWidget):
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
        self.sorted_scenes = []

        self.init_signals()

    def init_signals(self):
        # 绑定信号与槽（从 MainView 移过来的）
        self.ui.button_open_image_dir.clicked.connect(self.handle_open_image_dir)
        self.ui.button_remove_image.clicked.connect(self.handle_remove_image)
        self.ui.button_add_rect.clicked.connect(self.handle_add_rect)
        self.ui.button_del_rect.clicked.connect(self.handle_del_rect)
        self.ui.button_start.clicked.connect(self.handle_start_task)
        self.ui.button_export_images.clicked.connect(self.handle_export_images)
        self.ui.button_image_picker.clicked.connect(self.handle_open_image_dialog)

    def handle_open_image_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.window, "选择图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            return

        dialog = ImageClickDialog(file_path, max_points=2, connect_points=False, parent=self.window)
        dialog.points_selected.connect(self.handle_coordinates)
        dialog.exec()

    def handle_coordinates(self, points):
        print(f"Tab1 收到坐标: {points}")
        region = Rectangle(points[0], points[1])
        item = QListWidgetItem(str(region))
        item.setData(Qt.ItemDataRole.UserRole, region)
        self.ui.listWidget_rect.addItem(item)

    def handle_open_image_dir(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self.window, "请选择一个文件夹", self.last_image_dir_path, QFileDialog.Option.ShowDirsOnly
        )
        self.image_dir_path = selected_dir
        if selected_dir:
            self.last_image_dir_path = selected_dir
            self.ui.button_start.setEnabled(True)
            self.ui.button_remove_image.setEnabled(True)
            self.ui.label_image_dir_path.setText(f"已选择路径:{selected_dir}")
        else:
            self.ui.button_start.setEnabled(False)
            self.ui.button_remove_image.setEnabled(False)
            self.ui.label_image_dir_path.setText("操作已取消")

    def handle_remove_image(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self.window, "请选择一个文件夹", self.last_image_dir_path, QFileDialog.Option.ShowDirsOnly
        )
        if selected_dir:
            match_prefix = self.ui.checkBox_remove_image_match_prefix.isChecked()
            image_srv = ImageManage(self.image_dir_path)
            del_count, error_files = image_srv.delete_duplicates(selected_dir, match_prefix)
            msg = f"成功移除{del_count}文件,移除失败{len(error_files)}个"
            QMessageBox.information(self.window, "提示", msg)
            if error_files:
                print(error_files)

    def handle_add_rect(self):
        start_point_x = int(self.ui.input_start_point_x.text() or 0)
        start_point_y = int(self.ui.input_start_point_y.text() or 0)
        end_point_x = int(self.ui.input_end_point_x.text() or 1)
        end_point_y = int(self.ui.input_end_point_y.text() or 1)

        region = Rectangle(Point(start_point_x, start_point_y), Point(end_point_x, end_point_y))
        item = QListWidgetItem(str(region))
        item.setData(Qt.ItemDataRole.UserRole, region)
        self.ui.listWidget_rect.addItem(item)

    def handle_del_rect(self):
        current_item = self.ui.listWidget_rect.currentItem()
        if current_item is None:
            QMessageBox.warning(self.window, "提示", "请先在列表中选择要删除的行！")
            return

        current_row = self.ui.listWidget_rect.row(current_item)
        self.ui.listWidget_rect.takeItem(current_row)
        QMessageBox.information(self.window, "成功", "该行数据已成功删除！")

    def handle_start_task(self):
        self.ui.button_export_images.setEnabled(False)
        self.window.statusBar().showMessage("任务执行中")

        my_regions = []
        for i in range(self.ui.listWidget_rect.count()):
            item = self.ui.listWidget_rect.item(i)
            rect = item.data(Qt.ItemDataRole.UserRole)
            my_regions.append(rect)

        types = ["ignore", "only_scan"]
        current_mode = types[self.ui.selector_match_type.currentIndex()]
        nfeatures = int(self.ui.input_nfeatures.text())
        similarity_thresh = int(self.ui.input_similarity_thresh.text())
        match_distance_thresh = int(self.ui.input_match_distance_thresh.text())

        classifier = SceneClassifier(
            regions=my_regions,
            region_mode=current_mode,
            nfeatures=nfeatures,
            match_distance_thresh=match_distance_thresh,
            similarity_thresh=similarity_thresh
        )

        self.sorted_scenes = classifier.classify(source_dir=self.image_dir_path)

        self.window.statusBar().showMessage("任务执行完成")
        self.ui.button_export_images.setEnabled(True)

    def handle_export_images(self):
        if not self.sorted_scenes:
            QMessageBox.information(self.window, "错误", "还没处理图片！")
            return

        match_quantity = int(self.ui.input_match_quantity.text())
        image_srv = ImageManage(self.image_dir_path)
        target_dir = image_srv.copy_images(self.sorted_scenes, match_quantity)
        reply = QMessageBox.information(
            self.window, "提示", "复制成功，是否立即打开目标特定目录？",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Ok
        )
        if reply == QMessageBox.StandardButton.Ok:
            if os.path.exists(target_dir):
                QDesktopServices.openUrl(QUrl.fromLocalFile(target_dir))
            else:
                QMessageBox.warning(self.window, "错误", "找不到指定的目录！")