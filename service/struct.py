from typing import Tuple


class Point:
    """二维坐标点"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Rectangle:
    """矩形区域（支持正数绝对坐标，也支持负数倒数定位）"""

    def __init__(self, origin: Point, length: float, width: float):
        self.origin = origin  # 左上角的点
        self.length = length
        self.width = width

    def get_coords(self, img_w: int, img_h: int) -> Tuple[int, int, int, int]:
        """将逻辑坐标转换为实际像素切片坐标"""
        # 处理起点：如果是负数，则从右侧/底部倒数
        x_start = self.origin.x if self.origin.x >= 0 else img_w + self.origin.x
        y_start = self.origin.y if self.origin.y >= 0 else img_h + self.origin.y

        # 计算终点
        x_end = x_start + self.length
        y_end = y_start + self.width

        # 边界检查与排序，确保 x1 < x2 且 y1 < y2
        x1, x2 = sorted([max(0, min(img_w, x_start)), max(0, min(img_w, x_end))])
        y1, y2 = sorted([max(0, min(img_h, y_start)), max(0, min(img_h, y_end))])

        return int(x1), int(y1), int(x2), int(y2)

    def __repr__(self):
        return f"Rectangle(origin={self.origin}, width={self.length}, height={self.width})"
