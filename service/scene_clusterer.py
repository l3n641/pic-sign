import os
from collections import defaultdict
from typing import List, Tuple, Optional

import cv2
import numpy as np

from service.project_struct import Rectangle


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

    def classify(self, source_dir: str, valid_exts=('.jpg', '.jpeg', '.png', '.webp', '.bmp')):
        """
        核心分类流
        :param source_dir: 输入图片文件夹
        """

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

        return sorted_scenes
