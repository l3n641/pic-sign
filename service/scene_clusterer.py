import os
import shutil
import time
from collections import defaultdict
from typing import List, Tuple, Optional

import cv2
import numpy as np

from service.struct import Point, Rectangle


# ==========================================
#  增强型场景分类器封装
# ==========================================

class SceneClassifier:
    """基于 ORB 特征的图像场景聚类分类器（支持ROI提取/区域忽略、Top-N过滤）"""

    def __init__(
            self,
            regions: Optional[List[Rectangle]] = None,
            region_mode: str = "only_scan",
            nfeatures: int = 2000,
            match_distance_thresh: int = 45,
            similarity_thresh: int = 40
    ):
        """
        :param regions: Rectangle 区域对象列表
        :param region_mode: 区域处理模式 -> 'only_scan'(只扫描这些区域) 或 'ignore'(忽略这些区域)
        :param nfeatures: ORB 最大特征点数量
        :param match_distance_thresh: 判定为高质量匹配的汉明距离阈值
        :param similarity_thresh: 判定为同一场景所需的高质量匹配点数量阈值
        """
        if region_mode not in ("only_scan", "ignore"):
            raise ValueError("region_mode 必须是 'only_scan' 或 'ignore'")

        self.regions = regions
        self.region_mode = region_mode
        self.similarity_thresh = similarity_thresh
        self.match_distance_thresh = match_distance_thresh

        # 初始化选中的 OpenCV 算子
        self.orb = cv2.ORB_create(nfeatures=nfeatures)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def _preprocess_image(self, img_path: str) -> Optional[np.ndarray]:
        """读取并预处理图片（自适应处理透明通道并转灰度）"""
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            return None

        # 处理透明通道：将透明背景填充为白色，防止边缘产生干扰点
        if len(img.shape) == 3 and img.shape[2] == 4:
            alpha = img[:, :, 3] / 255.0
            bgr = img[:, :, :3]
            white_bg = np.ones_like(bgr, dtype=np.uint8) * 255
            img = (bgr * alpha[..., np.newaxis] + white_bg * (1 - alpha[..., np.newaxis])).astype(np.uint8)
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

    def _generate_mask(self, gray_img: np.ndarray) -> Optional[np.ndarray]:
        """根据指定的模式核心生成对应的 Mask 掩膜"""
        if not self.regions:
            return None

        h, w = gray_img.shape

        if self.region_mode == "only_scan":
            # 模式 1：只扫描选定区域（全黑背景，选定区域为白）
            mask = np.zeros((h, w), dtype=np.uint8)
            fill_value = 255
        else:
            # 模式 2：忽略选定区域（全白背景，选定区域为黑）
            mask = np.full((h, w), 255, dtype=np.uint8)
            fill_value = 0

        for rect in self.regions:
            x1, y1, x2, y2 = rect.get_coords(w, h)
            mask[y1:y2, x1:x2] = fill_value

        return mask

    def extract_features(self, img_path: str) -> Tuple[Optional[list], Optional[np.ndarray]]:
        """提取单张图片的特征点和描述符"""
        gray = self._preprocess_image(img_path)
        if gray is None:
            return None, None

        mask = self._generate_mask(gray)
        kp, des = self.orb.detectAndCompute(gray, mask=mask)
        return kp, des

    def are_images_similar(self, des1: np.ndarray, des2: np.ndarray) -> bool:
        """比对两个特征集以评估其是否属于同一场景"""
        if des1 is None or des2 is None:
            return False

        try:
            matches = self.bf.match(des1, des2)
            good_matches = [m for m in matches if m.distance < self.match_distance_thresh]
            return len(good_matches) > self.similarity_thresh
        except cv2.error:
            return False

    def classify(self, source_dir: str, output_dir: str, n_top: int = 0,
                 valid_exts=('.jpg', '.jpeg', '.png', '.webp', '.bmp')):
        """
        核心分类流
        :param source_dir: 输入图片文件夹
        :param output_dir: 分类结果输出主文件夹
        :param n_top: 限制只输出数量最多的前 N 个场景。<= 0 则输出全部。
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        files = [f for f in os.listdir(source_dir) if f.lower().endswith(valid_exts)]

        scene_reps = {}
        scene_files = defaultdict(list)

        print(f"--- 第一阶段：正在分析图片并归类场景（区域模式: {self.region_mode}） ---")
        for filename in files:
            path = os.path.join(source_dir, filename)
            print(f"正在分析: {filename}", end=" ")

            _, des_curr = self.extract_features(path)

            if des_curr is None or len(des_curr) < 5:
                print(" -> [跳过] 特征点过少")
                continue

            matched_id = None
            for s_id, des_rep in scene_reps.items():
                if self.are_images_similar(des_curr, des_rep):
                    matched_id = s_id
                    break

            if matched_id is None:
                matched_id = len(scene_reps) + 1
                scene_reps[matched_id] = des_curr
                print(f" -> [新场景 {matched_id}]")
            else:
                print(f" -> [匹配到场景 {matched_id}]")

            scene_files[matched_id].append(filename)

        # 排序阶段
        sorted_scenes = sorted(scene_files.items(), key=lambda item: len(item[1]), reverse=True)

        print("\n--- 第二阶段：统计并筛选结果 ---")
        if n_top <= 0:
            print(f"[n_top 设为 {n_top}] 将保留并复制全部 {len(sorted_scenes)} 个场景")
            top_scenes = sorted_scenes
        else:
            print(f"将仅筛选并保留数量排名前 {n_top} 的场景")
            top_scenes = sorted_scenes[:n_top]

        print("场景数量完整排名如下：")
        for rank, (s_id, f_list) in enumerate(sorted_scenes, 1):
            status = "[保留并复制]" if (n_top <= 0 or rank <= n_top) else "[舍弃]"
            print(f"  排名 {rank}: 场景 {s_id} -> 包含 {len(f_list)} 张图片 {status}")

        print("\n--- 第三阶段：执行文件分区复制 ---")
        for rank, (s_id, f_list) in enumerate(top_scenes, 1):
            target_dir = os.path.join(output_dir, f"rank_{rank}_scene_{s_id}")
            os.makedirs(target_dir, exist_ok=True)

            print(f"正在复制 场景 {s_id} 的图片到: {target_dir}")
            for filename in f_list:
                src_path = os.path.join(source_dir, filename)
                shutil.copy(src_path, os.path.join(target_dir, filename))


# ==========================================
#  统一运行测试入口
# ==========================================

if __name__ == "__main__":
    # 路径配置
    SRC_FOLDER = r'D:\code\test\images'
    OUT_FOLDER = f'D:\code\\test\images\\output_{time.time()}'

    # 定义目标矩形区域
    my_regions = [
        Rectangle(Point(60, 190), width=675, length=850)
    ]

    # --- 参数控制面板 ---

    # 💥 控制开关：'only_scan'（只扫描矩形内） 或 'ignore'（抠除矩形，扫描矩形外）
    CURRENT_MODE = "ignore"

    # 保留数量前 N 的场景数 (0 代表保留所有)
    N_TOP_SCENES = 1

    # 相似匹配阈值
    # 注意：如果是 'only_scan' 局部，提取点较少，阈值建议设低点（如 30~50）；
    # 如果是 'ignore' 仅抠除一小块，大部分全图都被扫描，阈值可以设高点（如 400~1000）。
    SIMILARITY_THRES = 1000

    # 实例化并运行
    classifier = SceneClassifier(
        regions=my_regions,
        region_mode=CURRENT_MODE,
        nfeatures=2000,
        similarity_thresh=SIMILARITY_THRES
    )

    classifier.classify(
        source_dir=SRC_FOLDER,
        output_dir=OUT_FOLDER,
        n_top=N_TOP_SCENES
    )

    print("\n所有图片处理完毕。")
