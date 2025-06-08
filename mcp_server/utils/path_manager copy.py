import asyncio
import threading
from pathlib import Path
from typing import Union, Literal
import weakref



class AsyncRWLock:
    """비동기 Reader-Writer 락 (writer 우선순위 포함)"""
    
    def __init__(self):
        self._readers = 0
        self._writers = 0
        self._waiting_writers = 0  # 대기 중인 writer 수
        self._lock = asyncio.Lock()
        self._condition = asyncio.Condition(self._lock)
    
    async def acquire_read(self):
        """읽기 락 획득"""
        async with self._condition:
            # writer가 있거나 대기 중인 writer가 있으면 대기 (writer 우선순위)
            while self._writers > 0 or self._waiting_writers > 0:
                await self._condition.wait()
            self._readers += 1
    
    async def release_read(self):
        """읽기 락 해제"""
        async with self._condition:
            self._readers -= 1
            if self._readers == 0:
                self._condition.notify_all()
    
    async def acquire_write(self):
        """쓰기 락 획득"""
        async with self._condition:
            self._waiting_writers += 1
            try:
                while self._writers > 0 or self._readers > 0:
                    await self._condition.wait()
                self._writers += 1
            finally:
                self._waiting_writers -= 1
    
    async def release_write(self):
        """쓰기 락 해제"""
        async with self._condition:
            self._writers -= 1
            self._condition.notify_all()


class PathManager:
    """간단한 Reader-Writer 패턴 기반 경로 관리자"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
            
        self._initialized = True
        self._path_locks: weakref.WeakValueDictionary[str, AsyncRWLock] = weakref.WeakValueDictionary()
        self._global_lock = asyncio.Lock()
    
    async def _get_path_lock(self, path_str: str) -> AsyncRWLock:
        async with self._global_lock:
            lock = self._path_locks.get(path_str)
            if lock is not None:
                return lock  # strong reference

            lock = AsyncRWLock()
            self._path_locks[path_str] = lock
            return lock 
    
    def __call__(self, path: Union[str, Path], mode: Literal["r", "w", "a"] = "r"):
        """편의 메서드"""
        if mode == "r":
            return PathReadContext(self, Path(path))
        elif mode in ("w", "a"):
            return PathWriteContext(self, Path(path), mode)
        else:
            raise ValueError(f"Invalid mode: {mode}")


class PathReadContext:
    """읽기 컨텍스트"""
    
    def __init__(self, manager: PathManager, path: Path):
        self.manager = manager
        self.path = path
        self.path_str = str(path.resolve())
        self.lock = None
    
    async def __aenter__(self):
        self.lock = await self.manager._get_path_lock(self.path_str)
        await self.lock.acquire_read()
        return self.path
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.lock.release_read()


class PathWriteContext:
    """쓰기 컨텍스트"""
    
    def __init__(self, manager: PathManager, path: Path, mode: str):
        self.manager = manager
        self.path = path
        self.path_str = str(path.resolve())
        self.mode = mode
        self.lock = None
    
    async def __aenter__(self):
        self.lock = await self.manager._get_path_lock(self.path_str)
        await self.lock.acquire_write()
        return self.path
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.lock.release_write()


# 사용 예시
async def example():
    manager = PathManager()
    
    # 읽기
    async with manager("test.txt", "r") as path:
        print(f"Reading {path}")
    
    # 쓰기
    async with manager("test.txt", "w") as path:
        print(f"Writing {path}")


if __name__ == "__main__":
    asyncio.run(example())