from queue import Queue, Empty
import threading
from dataclasses import dataclass
from typing import Any, Callable, Optional
from enum import Enum
from pathlib import Path

class TaskType(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"

@dataclass
class FileTask:
    task_id: str
    task_type: TaskType
    file_path: str
    data: Any = None
    binary: bool = False
    callback: Optional[Callable] = None
    result_queue: Optional[Queue] = None

class FileMessageBroker:
    def __init__(self, num_workers=4):
        self.task_queue = Queue()
        self.workers = []
        self.results = {}
        self.file_locks = {}
        self.lock = threading.Lock()
        
        # 워커 스레드들 시작
        for i in range(num_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def _worker(self):
        while True:
            try:
                task = self.task_queue.get(timeout=1)
                if task is None:  # 종료 신호
                    break
                self._execute_task(task)
                self.task_queue.task_done()
            except Empty:
                continue
    
    def _execute_task(self, task: FileTask):
        # 파일별 락 획득
        with self.lock:
            if task.file_path not in self.file_locks:
                self.file_locks[task.file_path] = threading.RLock()
        
        file_lock = self.file_locks[task.file_path]
        
        try:
            with file_lock:
                result = self._do_file_operation(task)
                
            # 결과 처리
            if task.result_queue:
                task.result_queue.put(result)
            elif task.callback:
                task.callback(result)
                
        except Exception as e:
            error_result = f"ERROR: {e}"
            if task.result_queue:
                task.result_queue.put(error_result)
            elif task.callback:
                task.callback(error_result)
    
    def _do_file_operation(self, task: FileTask):
        path = Path(task.file_path)
        
        if task.task_type == TaskType.READ:
            mode = "rb" if task.binary else "r"
            with open(path, mode) as f:
                return f.read()
                
        elif task.task_type == TaskType.WRITE:
            mode = "wb" if task.binary else "w"
            with open(path, mode) as f:
                f.write(task.data)
            return "SUCCESS"
            
        elif task.task_type == TaskType.DELETE:
            path.unlink()
            return "DELETED"
    
    def submit_task(self, task: FileTask):
        self.task_queue.put(task)
    
    def read_sync(self, file_path: str, binary=False):
        result_queue = Queue()
        task = FileTask(
            task_id=f"read_{id(result_queue)}",
            task_type=TaskType.READ,
            file_path=file_path,
            binary=binary,
            result_queue=result_queue
        )
        self.submit_task(task)
        result = result_queue.get()
        if isinstance(result, str) and result.startswith("ERROR:"):
            raise IOError(result[7:])
        return result
    
    def write_async(self, file_path: str, data, binary=False, callback=None):
        task = FileTask(
            task_id=f"write_{id(data)}",
            task_type=TaskType.WRITE,
            file_path=file_path,
            data=data,
            binary=binary,
            callback=callback
        )
        self.submit_task(task)
    
    def shutdown(self):
        # 모든 작업 완료 대기
        self.task_queue.join()
        
        # 워커들에게 종료 신호
        for _ in self.workers:
            self.task_queue.put(None)

# 전역 브로커
file_broker = FileMessageBroker(num_workers=4)

class ManagedPath:
    """Path-like wrapper that uses the file broker for operations"""
    
    def __init__(self, path):
        self._path = Path(path)
    
    def __str__(self):
        return str(self._path)
    
    def __repr__(self):
        return f"ManagedPath({self._path!r})"
    
    def __fspath__(self):
        return str(self._path)
    
    def __truediv__(self, other):
        return ManagedPath(self._path / other)
    
    def __rtruediv__(self, other):
        return ManagedPath(other / self._path)
    
    @property
    def name(self):
        return self._path.name
    
    @property
    def suffix(self):
        return self._path.suffix
    
    @property
    def parent(self):
        return ManagedPath(self._path.parent)
    
    @property
    def stem(self):
        return self._path.stem
    
    def exists(self):
        return self._path.exists()
    
    def is_file(self):
        return self._path.is_file()
    
    def is_dir(self):
        return self._path.is_dir()
    
    def mkdir(self, parents=False, exist_ok=False):
        return self._path.mkdir(parents=parents, exist_ok=exist_ok)
    
    def read_text(self, encoding='utf-8'):
        return file_broker.read_sync(str(self._path), binary=False)
    
    def write_text(self, data, callback=None, encoding='utf-8'):
        file_broker.write_async(str(self._path), data, binary=False, callback=callback)
    
    def read_bytes(self):
        return file_broker.read_sync(str(self._path), binary=True)
    
    def write_bytes(self, data, callback=None):
        file_broker.write_async(str(self._path), data, binary=True, callback=callback)