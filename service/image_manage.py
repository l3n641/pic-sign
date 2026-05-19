import os
import shutil
import time


class ImageManage(object):
    def __init__(self, origin_image_dir):
        self.origin_image_dir = origin_image_dir

    @staticmethod
    def get_file_prefix(filename):
        """
        辅助函数：获取文件名下划线之前的部分（自动忽略文件扩展名）
        例如: 'c259258157_2.jpg' -> 'c259258157'
              'c259258157.jpg'   -> 'c259258157'
        """
        # os.path.splitext 用于分离文件名和后缀，得到 ('c259258157_2', '.jpg')
        base_name, _ = os.path.splitext(filename)
        # 按下划线分割并取第一部分
        return base_name.split('_')[0]

    def delete_duplicates(self, dir_b, match_prefix=False):
        # 1. 安全检查：检查目录是否存在
        if not os.path.exists(self.origin_image_dir) or not os.path.exists(dir_b):
            return False, []

        # 2. 安全检查：防止相同物理目录误删
        if os.path.samefile(self.origin_image_dir, dir_b):
            return False, []

        # 3. 获取目录 b 中的所有文件
        files_in_b = {f for f in os.listdir(dir_b) if os.path.isfile(os.path.join(dir_b, f))}

        # 如果开启了前缀匹配，将目录 b 的文件名全部转换为“下划线前缀”集合
        if match_prefix:
            b_targets = {self.get_file_prefix(f) for f in files_in_b}
        else:
            b_targets = files_in_b

        deleted_count = 0
        error_files = []

        # 4. 遍历目录 a
        for filename in os.listdir(self.origin_image_dir):
            file_path_a = os.path.join(self.origin_image_dir, filename)

            if os.path.isfile(file_path_a):
                # 根据参数决定：是比对“前缀”还是比对“完整文件名”
                if match_prefix:
                    prefix_a = self.get_file_prefix(filename)
                    is_match = prefix_a in b_targets
                else:
                    is_match = filename in b_targets

                # 如果匹配成功，执行删除
                if is_match:
                    try:
                        os.remove(file_path_a)
                        deleted_count += 1
                    except Exception as e:
                        error_files.append(filename)

        return deleted_count, error_files

    def copy_images(self, sorted_scenes, n_top: int):
        # 路径配置
        out_dir_name = f'output_{time.time()}'
        output_dir = os.path.join(self.origin_image_dir, out_dir_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if n_top <= 0:
            top_scenes = sorted_scenes
        else:
            top_scenes = sorted_scenes[:n_top]

        for rank, (s_id, f_list) in enumerate(sorted_scenes, 1):
            status = "[保留并复制]" if (n_top <= 0 or rank <= n_top) else "[舍弃]"
            print(f"  排名 {rank}: 场景 {s_id} -> 包含 {len(f_list)} 张图片 {status}")

        print("\n--- 第三阶段：执行文件分区复制 ---")
        for rank, (s_id, f_list) in enumerate(top_scenes, 1):
            target_dir = os.path.join(output_dir, f"rank_{rank}_scene_{s_id}")
            os.makedirs(target_dir, exist_ok=True)

            print(f"正在复制 场景 {s_id} 的图片到: {target_dir}")
            for filename in f_list:
                src_path = os.path.join(self.origin_image_dir, filename)
                shutil.copy(src_path, os.path.join(target_dir, filename))

        return output_dir
