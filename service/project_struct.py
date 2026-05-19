from typing import Tuple


class Point:
    """二维坐标点"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

class Rectangle:
    """矩形区域（支持正数绝对坐标，也支持负数倒数定位，由两个点定义）"""

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1  # 对角线上的第一个点
        self.p2 = p2  # 对角线上的第二个点

    def get_coords(self, img_w: int, img_h: int) -> Tuple[int, int, int, int]:
        """将逻辑坐标转换为实际像素切片坐标"""
        # 处理 p1：如果是负数，则从右侧/底部倒数
        x1_logic = self.p1.x if self.p1.x >= 0 else img_w + self.p1.x
        y1_logic = self.p1.y if self.p1.y >= 0 else img_h + self.p1.y

        # 处理 p2：如果是负数，则从右侧/底部倒数
        x2_logic = self.p2.x if self.p2.x >= 0 else img_w + self.p2.x
        y2_logic = self.p2.y if self.p2.y >= 0 else img_h + self.p2.y

        # 边界检查与排序，确保 x1 < x2 且 y1 < y2
        # 即使 p1 和 p2 的先后顺序颠倒，sorted 也会自动纠正为左上角和右下角
        x1, x2 = sorted([max(0, min(img_w, x1_logic)), max(0, min(img_w, x2_logic))])
        y1, y2 = sorted([max(0, min(img_h, y1_logic)), max(0, min(img_h, y2_logic))])

        return int(x1), int(y1), int(x2), int(y2)

    def __repr__(self):
        return f"Rectangle(p1={self.p1}, p2={self.p2})"