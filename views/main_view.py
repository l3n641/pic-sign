# views/main_view.py

import os
import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtWidgets import QMessageBox

from service.image_manage import ImageManage
from service.scene_clusterer import SceneClassifier
from service.struct import Point, Rectangle
# 导入转换后的 UI 类（注意路径，因为 ui_py 是在根目录下的包）
from ui_py.main_ui import Ui_Widget


class MainView(QMainWindow, Ui_Widget):
    def __init__(self):
        super().__init__()

        self.image_dir_path = ""
        self.last_image_dir_path = "./"

        # 1. 实例化 UI 对象并挂载到 self.ui
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # --- 1. 初始化界面状态（比如按钮默认禁用，或者下拉框填入数据） ---
        self.statusBar().showMessage("")

        # --- 2. 绑定信号与槽（业务逻辑的核心） ---
        self.ui.button_open_image_dir.clicked.connect(self.handle_open_image_dir)
        self.ui.button_remove_image.clicked.connect(self.handle_remove_image)
        self.ui.button_add_rect.clicked.connect(self.handle_add_rect)
        self.ui.button_del_rect.clicked.connect(self.handle_del_rect)
        self.ui.button_start.clicked.connect(self.handle_start_task)

    # --- 打开图片目录 ---
    def handle_open_image_dir(self):
        # 弹出选择文件夹对话框
        selected_dir = QFileDialog.getExistingDirectory(
            self,
            "请选择一个文件夹",
            self.last_image_dir_path,  # 初始目录
            QFileDialog.Option.ShowDirsOnly
        )

        # 如果用户点击了“取消”，返回值会是空字符串 ""
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
        # 弹出选择文件夹对话框
        selected_dir = QFileDialog.getExistingDirectory(
            self,
            "请选择一个文件夹",
            self.last_image_dir_path,  # 初始目录
            QFileDialog.Option.ShowDirsOnly
        )

        if selected_dir:
            match_prefix = self.ui.checkBox_remove_image_match_prefix.isChecked()
            image_srv = ImageManage(self.image_dir_path)
            del_count, error_files = image_srv.delete_duplicates(selected_dir, match_prefix)
            msg = f"成功移除{del_count}文件,移除失败{len(error_files)}个"
            QMessageBox.information(self, "提示", msg)
            if error_files:
                print(error_files)

    def handle_add_rect(self):
        start_point_x = self.ui.input_start_point_x.text() or 0
        start_point_y = self.ui.input_start_point_y.text() or 0
        end_point_x = self.ui.input_end_point_x.text() or 1
        end_point_y = self.ui.input_end_point_y.text() or 1

        start_point_x = int(start_point_x)
        start_point_y = int(start_point_y)
        end_point_x = int(end_point_x)
        end_point_y = int(end_point_y)

        # 定义目标矩形区域
        region = Rectangle(Point(start_point_x, start_point_y), Point(end_point_x, end_point_y))

        # 2. 创建列表项，界面上只显示一个名字
        item = QListWidgetItem(str(region))

        # 3. 把整个 QRectF 对象塞进这一行里
        item.setData(Qt.ItemDataRole.UserRole, region)
        self.ui.listWidget_rect.addItem(item)

    def handle_del_rect(self):
        # 获取当前选中的 Item
        current_item = self.ui.listWidget_rect.currentItem()

        # 健壮性检查：如果用户没有选中任何行，弹出提示
        if current_item is None:
            QMessageBox.warning(self, "提示", "请先在列表中选择要删除的行！")
            return

        # 可选：如果你想在删除前获取一下这一行的数据做点别的事（比如记录日志）
        # rect_data = current_item.data(Qt.ItemDataRole.UserRole)
        # print(f"正在删除 {current_item.text()}，数据为: {rect_data}")

        # 获取当前选中的行号 (Row Index)
        current_row = self.ui.listWidget_rect.row(current_item)

        # 从列表中移除该行（界面和后台绑定的数据会一起被移除）
        self.ui.listWidget_rect.takeItem(current_row)

        # 提示用户删除成功
        QMessageBox.information(self, "成功", "该行数据已成功删除！")

    def handle_start_task(self):
        self.statusBar().showMessage("任务执行中")

        # 路径配置
        out_dir_name = f'output_{time.time()}'
        out_folder = os.path.join(self.image_dir_path, out_dir_name)

        # 定义目标矩形区域
        my_regions = []

        # 遍历 QListWidget 的每一行
        for i in range(self.ui.listWidget_rect.count()):
            item = self.ui.listWidget_rect.item(i)  # 获取当前的 Item 对象
            rect = item.data(Qt.ItemDataRole.UserRole)  # 提取出绑定的数据

            my_regions.append(rect)

        # 此时 all_rectangles 就是一个包含所有长方形对象的纯 Python 列表了
        print(f"一共读取了 {len(my_regions)} 个长方形数据")

        types = ["ignore", "only_scan"]
        default_type_index = self.ui.selector_match_type.currentIndex()

        # 💥 控制开关：'only_scan'（只扫描矩形内） 或 'ignore'（抠除矩形，扫描矩形外）
        current_mode = types[default_type_index]

        # 保留数量前 N 的场景数 (0 代表保留所有)
        match_quantity = int(self.ui.input_match_quantity.text())
        nfeatures = int(self.ui.input_nfeatures.text())

        # 相似匹配阈值
        # 注意：如果是 'only_scan' 局部，提取点较少，阈值建议设低点（如 30~50）；
        # 如果是 'ignore' 仅抠除一小块，大部分全图都被扫描，阈值可以设高点（如 400~1000）。
        similarity_thresh = int(self.ui.input_similarity_thresh.text())

        match_distance_thresh = int(self.ui.input_match_distance_thresh.text())

        # 实例化并运行
        classifier = SceneClassifier(
            regions=my_regions,
            region_mode=current_mode,
            nfeatures=nfeatures,
            match_distance_thresh=match_distance_thresh,
            similarity_thresh=similarity_thresh
        )

        classifier.classify(
            source_dir=self.image_dir_path,
            output_dir=out_folder,
            n_top=match_quantity
        )
        self.statusBar().showMessage("任务执行完成")

        print("\n所有图片处理完毕。")
