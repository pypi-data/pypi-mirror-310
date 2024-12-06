from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TaskID
from rich.console import Console
from typing import Dict
import threading

class MultiProgressBar:
    def __init__(self):
        self.console = Console()
        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[description]}", justify="right"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            TimeRemainingColumn(),
            console=self.console,
            transient=False,
        )
        self.tasks: Dict[str, TaskID] = {}
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._run_progress, daemon=True)
        self.thread.start()

    def _run_progress(self):
        self.progress.start()

    def add_task(self, task_id: str, description: str, total: int = 100):
        with self.lock:
            if task_id in self.tasks:
                raise ValueError(f"Task '{task_id}' already exists.")
            self.tasks[task_id] = self.progress.add_task(
                description=description, total=total, description=description
            )

    def update_task(self, task_id: str, advance: int = 1):
        with self.lock:
            if task_id not in self.tasks:
                raise ValueError(f"Task '{task_id}' does not exist.")
            self.progress.update(self.tasks[task_id], advance=advance)

    def remove_task(self, task_id: str):
        with self.lock:
            if task_id in self.tasks:
                self.progress.remove_task(self.tasks[task_id])
                del self.tasks[task_id]

    def finish(self):
        self.progress.stop()
        self.thread.join()
