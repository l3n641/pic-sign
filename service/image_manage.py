import os


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
