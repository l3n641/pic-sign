import os

import cv2
import numpy as np


class PerspectiveTransformer:

    def __init__(self, src_points: list, output_dir: str, output_size: tuple = None):
        """核心方法：执行透视变换

        :param src_points: 原图中的 4 个顶点坐标
        :param output_size: 目标图片的尺寸 (宽, 高)
        :param output_dir: 统一的图片输出目录
        """
        self.src_points = src_points
        self.output_dir = output_dir  # 👈 保持在实例属性中

        # 👈 直接调用封装好的函数，动态获取正确的、不失真的尺寸
        self.output_size = self.calculate_perspective_output_size(self.src_points, output_size)

        # 顺便在初始化时就把目录建好，省得每次 transform 都要判断
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def transform(self, image_path: str) -> str:
        """执行透视变换，并将结果图片以相同的文件名保存到初始化时指定的目录。

        :param image_path: 原图路径
        :return: 保存后的新图片完整路径
        """
        width, height = self.output_size

        # 1. 读取图片
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"无法读取图片: {image_path}")

        # 2. 转换数据类型与定义顶点
        pts1 = np.float32(self.src_points)
        pts2 = np.float32(
            [[0, 0], [width, 0], [width, height], [0, height]]
        )

        # 3. 计算变换矩阵并应用
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        dst_image = cv2.warpPerspective(image, matrix, (width, height))

        # 4. 提取文件名并拼接路径
        file_name = os.path.basename(image_path)
        save_path = os.path.join(self.output_dir, file_name)  # 👈 使用 self.output_dir

        # 5. 保存图片
        success = cv2.imwrite(save_path, dst_image)
        if not success:
            raise IOError(f"图片保存失败: {save_path}")

        return save_path

    def transform_dir(self, source_dir: str, valid_exts=('.jpg', '.jpeg', '.png', '.webp', '.bmp')):

        files = [f for f in os.listdir(source_dir) if f.lower().endswith(valid_exts)]
        for filename in files:
            path = os.path.join(source_dir, filename)
            print(f"正在透视转换: {filename}", end=" ")
            self.transform(path)

    @staticmethod
    def calculate_perspective_output_size(src_points: list, preset_size: tuple = None) -> tuple:
        """
        根据四点透视坐标，逆向估算物体在三维空间中的真实长宽像素尺寸（消除近大远小畸变）

        :param src_points: 原图中的 4 个顶点坐标，顺序必须为: [左上, 右上, 右下, 左下]
        :param preset_size: 可选，外部指定的固定目标尺寸 (宽, 高)。若传入则直接返回该尺寸。
        :return: 经过几何矫正的目标图片尺寸 (max_width, max_height)
        """
        # 1. 如果外部直接传了预设尺寸，直接使用
        if preset_size:
            return preset_size

        pts = np.array(src_points, dtype="float32")
        (tl, tr, br, bl) = pts

        # 计算四条边的平面像素长度（欧氏距离），用于备用和基准线
        width_a = np.linalg.norm(br - bl)  # 底边
        width_b = np.linalg.norm(tr - tl)  # 顶边
        height_a = np.linalg.norm(tr - br)  # 右边
        height_b = np.linalg.norm(tl - bl)  # 左边

        # 找到当前投影下最长的一条边，以此作为缩放基准，避免生成的图片分辨率过低模糊
        max_side = max(width_a, width_b, height_a, height_b)

        # 2. 将坐标中心化，减少大数值计算时的浮点数精度误差
        mx = (tl[0] + tr[0] + br[0] + bl[0]) / 4
        my = (tl[1] + tr[1] + br[1] + bl[1]) / 4

        u0, v0 = tl[0] - mx, tl[1] - my
        u1, v1 = tr[0] - mx, tr[1] - my
        u2, v2 = br[0] - mx, br[1] - my
        u3, v3 = bl[0] - mx, bl[1] - my

        # 3. 利用透视矩阵的行列式关系，逆向估算真实空间中的纵横比 (Aspect Ratio)
        # 计算一阶几何行列式
        w1 = (u1 - u2) * (v3 - v2) - (u3 - u2) * (v1 - v2)
        w2 = (u0 - u1) * (v3 - v0) - (u3 - u0) * (v1 - v0)
        w3 = (u0 - u3) * (v1 - v2) - (u1 - u2) * (v0 - v3)

        # 安全边界检查：如果点位退化（比如三点共线或极度扭曲），降级使用原平面算法
        if abs(w2) < 1e-5 or abs(w3) < 1e-5:
            return (max(int(width_a), int(width_b)), max(int(height_a), int(height_b)))

        # 计算透视投影常数
        n2 = ((u1 - u0) * (v2 - v0) - (u2 - u0) * (v1 - v0)) / w2
        n3 = ((u1 - u0) * (v3 - v0) - (u3 - u0) * (v1 - v0)) / w3

        # 基于针孔相机模型推导的长宽比平方
        try:
            a_sq = ((u1 - u0) ** 2 + (v1 - v0) ** 2) / ((u3 - u0) ** 2 + (v3 - v0) ** 2) * (1 + (n2 ** 2) / (n3 ** 2))
            aspect_ratio = np.sqrt(a_sq)
        except:
            # 异常保险机制
            return (max(int(width_a), int(width_b)), max(int(height_a), int(height_b)))

        # 4. 根据估算出的真实纵横比，配合最长边，等比例缩放生成最终像素尺寸
        if aspect_ratio >= 1.0:
            # 属于宽图：宽度锁定为最长边，高度按比例缩放
            max_width = int(max_side)
            max_height = int(max_width / aspect_ratio)
        else:
            # 属于长图：高度锁定为最长边，宽度按比例缩放
            max_height = int(max_side)
            max_width = int(max_height * aspect_ratio)

        return (max_width, max_height)
