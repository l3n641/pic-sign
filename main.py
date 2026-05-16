# main.py

import sys
from PySide6.QtWidgets import QApplication
# 从 views 包里导入你刚刚写好的逻辑类
from views.main_view import MainView


def main():
    # 1. 创建应用程序对象
    app = QApplication(sys.argv)

    # 2. 实例化业务逻辑窗口
    window = MainView()

    # 3. 显示窗口
    window.show()

    # 4. 进入 Qt 主事件循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()