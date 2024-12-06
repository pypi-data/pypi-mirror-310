import time
import threading
from .progress import MultiProgressBar

def worker(progress: MultiProgressBar, task_id: str, description: str, total: int, sleep_time: float):
    progress.add_task(task_id, description, total)
    for _ in range(total):
        time.sleep(sleep_time)
        progress.update_task(task_id, advance=1)
    progress.remove_task(task_id)

def main():
    progress = MultiProgressBar()

    # タスクの定義
    tasks = [
        {"task_id": "task1", "description": "タスク 1", "total": 50, "sleep_time": 0.1},
        {"task_id": "task2", "description": "タスク 2", "total": 80, "sleep_time": 0.05},
        {"task_id": "task3", "description": "タスク 3", "total": 30, "sleep_time": 0.2},
    ]

    threads = []
    for task in tasks:
        t = threading.Thread(
            target=worker,
            args=(
                progress,
                task["task_id"],
                task["description"],
                task["total"],
                task["sleep_time"],
            )
        )
        t.start()
        threads.append(t)

    # すべてのスレッドが完了するのを待つ
    for t in threads:
        t.join()

    # プログレスバーを終了する
    progress.finish()

if __name__ == "__main__":
    main()
