import os


class ImageManage(object):
    def __init__(self, origin_image_dir):
        self.origin_image_dir = origin_image_dir

    def delete_duplicates(self, dir_b):

        if not os.path.exists(self.origin_image_dir) or not os.path.exists(dir_b):
            return False, []

            # 2. 安全检查：如果路径指向同一个目录，直接返回
        if os.path.samefile(self.origin_image_dir, dir_b):
            return False, []

        # 获取目录 b 中的所有文件名，并存入集合（set）中以提高查找效率
        # 这里用 os.path.isfile 过滤掉子目录，只保留文件
        files_in_b = {f for f in os.listdir(dir_b) if os.path.isfile(os.path.join(dir_b, f))}

        deleted_count = 0
        error_files = []
        # 遍历目录 a
        for filename in os.listdir(self.origin_image_dir):
            file_path_a = os.path.join(self.origin_image_dir, filename)

            # 确保处理的是文件而不是子目录
            if os.path.isfile(file_path_a):
                # 如果目录 a 的文件名存在于目录 b 的集合中
                if filename in files_in_b:
                    try:
                        os.remove(file_path_a)
                        deleted_count += 1
                    except Exception as e:
                        error_files.append(filename)

        return deleted_count, error_files
