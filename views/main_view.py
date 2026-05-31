# views/main_view.py
from PySide6.QtWidgets import QMainWindow

from ui_py.main_ui import Ui_Widget
# 导入拆分后的组件
from views.tab1_scene_view import Tab1SceneView
from views.tab2_tools_view import Tab2ToolsView


class MainView(QMainWindow, Ui_Widget):
    def __init__(self):
        super().__init__()

        # 1. 初始化 UI
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.statusBar().showMessage("准备就绪")

        # 2. 实例化并挂载各个 Tab 的业务逻辑控制器
        # 把 self.ui 和 self(主窗口) 传进去，子模块就能自由控制其对应的控件和状态栏
        self.tab1_controller = Tab1SceneView(self.ui, self)
        self.tab2_controller = Tab2ToolsView(self.ui, self)

        # 3. 如果需要处理 Tab 切换事件，可以在这里统一监听
        self.ui.tabWidget.currentChanged.connect(self.handle_tab_changed)

    def handle_tab_changed(self, index):
        """当用户切换 Tab 时触发的全局响应（可选）"""
        tab_title = self.ui.tabWidget.tabText(index)
        self.statusBar().showMessage(f"当前处于: {tab_title}")
