import os
import logging
from logging.handlers import TimedRotatingFileHandler
import zipfile

from .now import get_now
from .path_manager import PathManager

pm = PathManager()

def get_backup_name(default_name):
    """백업 파일 이름을 생성하는 함수. 현재 시간을 포함하여 이름 생성"""
    timestamp = get_now(form="%Y%m%d%H%M%S")
    dirname = os.path.dirname(default_name)
    basename = os.path.basename(default_name)
    root, ext = os.path.splitext(basename)
    return os.path.join(dirname, f"{root}_{timestamp}{ext}.zip")

def path_managed_rotator(source, dest):
    """PathManager로 보호되는 rotator 함수"""
    custom_dest = get_backup_name(source)
    
    # rotator도 PathManager의 write 컨텍스트에서 실행
    with pm(source, "w").write(priority=0):
        with zipfile.ZipFile(custom_dest, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(source, os.path.basename(source))
        os.remove(source)

class PathManagedSizeTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    PathManager의 우선순위 큐를 사용하여 스레드 안전한 로그 파일 회전을 지원하는 핸들러
    """
    def __init__(self, filename, when='h', interval=1, backupCount=0, 
                 encoding=None, delay=False, utc=False, atTime=None,
                 maxBytes=0):
        TimedRotatingFileHandler.__init__(self, filename, when, interval,
                                         backupCount, encoding, delay, utc, atTime)
        self.maxBytes = maxBytes
        
    def shouldRollover(self, record):
        """
        시간 또는 크기 기준 중 하나라도 충족되면 로그 파일을 회전
        """
        # 먼저 시간 기반 검사 (부모 클래스 메서드 사용)
        if TimedRotatingFileHandler.shouldRollover(self, record):
            return 1
            
        # 이제 크기 기반 검사
        if self.maxBytes > 0:
            if self.stream is None:
                return 0
            msg = self.format(record)
            self.stream.seek(0, 2)  # 파일 끝으로 이동
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        return 0
    
    def emit(self, record):
        """PathManager의 write 큐를 통해 안전하게 로그 작성"""
        
        # 로테이션이 필요한지 먼저 체크
        needs_rollover = self.shouldRollover(record)
        
        if needs_rollover:
            # 로테이션은 높은 우선순위(0)로 write 모드
            with pm(self.baseFilename, "w").write(priority=0):
                self.doRollover()
        
        # 일반 로그 쓰기는 낮은 우선순위(1)로 write 모드  
        with pm(self.baseFilename, "w").write(priority=1):
            # 실제 파일 쓰기 (부모 클래스의 emit 호출)
            TimedRotatingFileHandler.emit(self, record)
    
    def getFilesToDelete(self):
        """백업 카운트 초과 시 삭제할 파일 목록을 반환"""
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        
        # 백업 파일 패턴: [로그명]_[타임스탬프].log.zip
        prefix = baseName + "_"
        suffix = ".zip"
        
        # 이 로거에 속한 백업 파일 찾기
        for fileName in fileNames:
            if fileName.startswith(prefix) and fileName.endswith(suffix):
                result.append(os.path.join(dirName, fileName))
        
        # 시간 기준으로 정렬 (가장 오래된 것 먼저)
        result.sort()
        
        # 백업 카운트를 초과하는 항목 반환
        if len(result) < self.backupCount:
            return []
        else:
            return result[:len(result) - self.backupCount]

def setup_logger(LOG_DIR, log_level="DEBUG", retention_days=7, max_bytes=10*1024*1024):
    """
    PathManager 기반 스레드 안전한 로거 설정 (시간 및 크기 기반 로테이션)
    """
    # 고정 파일명 설정
    LOG_FILE = os.path.join(LOG_DIR, "application.log")
    
    # 기본 포맷 설정 - 로거 이름과 함수 이름 포함
    formatter = logging.Formatter('{asctime} | {name} | {funcName} | {levelname} | {message}', 
                                 '%Y-%m-%d %H:%M:%S', 
                                 style='{')
    
    # PathManager 기반 파일 핸들러 설정 (시간+크기 기반)
    file_handler = PathManagedSizeTimedRotatingFileHandler(
        LOG_FILE,
        when='midnight',
        interval=1,
        backupCount=retention_days,
        maxBytes=max_bytes
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # PathManager 기반 로테이터 설정
    file_handler.rotator = path_managed_rotator
    
    # 콘솔 출력 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # 로그 디렉토리가 없으면 생성
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 기존 핸들러 제거
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 새 핸들러 추가
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger


# 테스트용 코드
if __name__ == "__main__":
    import threading
    import time
    from dotenv import load_dotenv
    
    load_dotenv(verbose=False)
    
    LOG_DIR = os.getenv("PATH_LOG_VIRTUAL", "./logs")
        
    # PathManager 기반 로깅 설정 (1MB 크기 제한으로 테스트)
    root_logger = setup_logger(LOG_DIR, max_bytes=1*1024*1024)
    
    def log_worker(worker_id):
        """여러 스레드에서 동시에 로그 기록"""
        for i in range(100):
            root_logger.info(f"Worker {worker_id} - Message {i} - " + "x" * 100)
            time.sleep(0.01)
    
    # 여러 스레드로 동시 로깅 테스트
    threads = []
    for i in range(5):
        t = threading.Thread(target=log_worker, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("PathManager 기반 로깅 테스트 완료")