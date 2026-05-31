import os
from collections import defaultdict
from PySide6.QtCore import QThread, QWaitCondition, QMutex, Signal

class SceneClassificationThread(QThread):
    # 信号：每处理完一张图发送一次，传递当前进度和状态
    progress_signal = Signal(dict)
    # 信号：整个任务彻底完成后发送，传回最终的排序结果
    task_finished = Signal(list)

    def __init__(self, classifier, source_dir, valid_exts=('.jpg', '.jpeg', '.png', '.webp', '.bmp')):
        super().__init__()
        self._mutex = QMutex()
        self._wait_condition = QWaitCondition()
        self._is_running = True
        self._is_paused = False

        self.classifier = classifier
        self.source_dir = source_dir
        self.valid_exts = valid_exts

    def run(self):
        # 1. 获取文件列表
        files = [f for f in os.listdir(self.source_dir) if f.lower().endswith(self.valid_exts)]
        total_files = len(files)

        # 2. 初始化分类容器（原本在 classify 里的变量）
        scene_reps = {}
        scene_files = defaultdict(list)

        print(f"--- 正在分析图片并归类场景（总数: {total_files}） ---")

        for index, filename in enumerate(files):
            # ================== 核心控制锁开始 ==================
            self._mutex.lock()
            # 检查是否停止
            if not self._is_running:
                self._mutex.unlock()
                print("线程已收到停止信号，安全退出")
                return # 直接退出 run，任务终止

            # 如果暂停，等待唤醒
            while self._is_paused:
                print("线程已暂停，等待恢复...")
                self._wait_condition.wait(self._mutex)
                # 被唤醒后，再次检查是否在暂停期间收到了停止信号
                if not self._is_running:
                    self._mutex.unlock()
                    print("线程在暂停状态中收到停止信号，安全退出")
                    return
            self._mutex.unlock()
            # ================== 核心控制锁结束 ==================

            # 发送进度给 UI（通知主界面现在处理到第几张了）
            self.progress_signal.emit({
                "current": index + 1,
                "total": total_files,
                "filename": filename,
                "status": "processing"
            })

            # 3. 开始处理单张图片（调用 classifier 的方法）
            path = os.path.join(self.source_dir, filename)
            _, des_curr = self.classifier.extract_features(path)

            if des_curr is None or len(des_curr) < 5:
                print(f"[{filename}] -> 跳过，特征点过少")
                continue

            matched_id = None
            for s_id, des_rep in scene_reps.items():
                if self.classifier.are_images_similar(des_curr, des_rep):
                    matched_id = s_id
                    break

            if matched_id is None:
                matched_id = len(scene_reps) + 1
                scene_reps[matched_id] = des_curr
                print(f"[{filename}] -> 新场景 {matched_id}")
            else:
                print(f"[{filename}] -> 匹配到场景 {matched_id}")

            scene_files[matched_id].append(filename)

        # 4. 当循环正常结束（未被中途 stop），进行排序并发送最终结果
        sorted_scenes = sorted(scene_files.items(), key=lambda item: len(item[1]), reverse=True)
        self.task_finished.emit(sorted_scenes)

    # ================== 外部控制方法 ==================
    def pause(self):
        self._mutex.lock()
        self._is_paused = True
        self._mutex.unlock()
        print("线程已设置为暂停")

    def resume(self):
        self._mutex.lock()
        self._is_paused = False
        self._wait_condition.wakeAll()
        self._mutex.unlock()
        print("线程已恢复")

    def stop(self):
        self._mutex.lock()
        self._is_running = False
        self._wait_condition.wakeAll()  # 确保如果线程在暂停中也能被唤醒并退出
        self._mutex.unlock()
        print("线程已设置为停止")