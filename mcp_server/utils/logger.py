import os
import logging
from logging.handlers import TimedRotatingFileHandler
import zipfile
import time
import re

from .now import get_now

def get_backup_name(default_name):
    """백업 파일 이름을 생성하는 함수. 현재 시간을 포함하여 이름 생성"""
    timestamp = get_now(form="%Y%m%d%H%M%S")
    dirname = os.path.dirname(default_name)
    basename = os.path.basename(default_name)
    root, ext = os.path.splitext(basename)
    return os.path.join(dirname, f"{root}_{timestamp}{ext}.zip")

def rotator(source, dest):
    """백업 파일을 압축하는 함수"""
    # dest 파일명 무시하고 타임스탬프 기반으로 새 이름 생성
    custom_dest = get_backup_name(source)
    
    with zipfile.ZipFile(custom_dest, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(source, os.path.basename(source))
    os.remove(source)
    
    # 원래 dest 대신 custom_dest를 사용했으므로, 원래 dest는 생성하지 않는다

class SizeTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    시간과 파일 크기 모두에 기반하여 로그 파일을 회전시키는 핸들러
    """
    def __init__(self, filename, when='h', interval=1, backupCount=0, 
                 encoding=None, delay=False, utc=False, atTime=None,
                 maxBytes=0):  # maxBytes 매개변수 추가
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
        if self.maxBytes > 0:                   # 크기 제한이 설정된 경우만
            msg = self.format(record)
            self.stream.seek(0, 2)              # 파일 끝으로 이동
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        return 0
    
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
    모든 로거가 같은 파일에 로그를 남기도록 설정하는 함수 (시간 및 크기 기반 로테이션)
    """
    # 고정 파일명 설정
    LOG_FILE = os.path.join(LOG_DIR, "application.log")
    
    # 기본 포맷 설정 - 로거 이름과 함수 이름 포함
    formatter = logging.Formatter('{asctime} | {name} | {funcName} | {levelname} | {message}', 
                                 '%Y-%m-%d %H:%M:%S', 
                                 style='{')
    
    # 커스텀 파일 핸들러 설정 (시간+크기 기반)
    file_handler = SizeTimedRotatingFileHandler(
        LOG_FILE,
        when='midnight',
        interval=1,
        backupCount=retention_days,
        maxBytes=max_bytes  # 최대 파일 크기 설정
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # 커스텀 로테이터 및 네이머 설정
    file_handler.rotator = rotator
    # namer 함수는 TimedRotatingFileHandler에서 사용되지만, 
    # 여기서는 rotator 함수 내에서 직접 파일명을 생성하므로 필요 없음
    
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
    from dotenv import load_dotenv
    load_dotenv(verbose=False)
    
    LOG_DIR = os.getenv("PATH_LOG_VIRTUAL", "./logs")
        
    # 통합 로깅 설정 (10MB 크기 제한)
    root_logger = setup_logger(LOG_DIR, max_bytes=10*1024*1024)  # 10MB
    
    # 각 로거 사용 예
    root_logger.info("Data processing started")
    root_logger.debug("Raw data received: XYZ")
    root_logger.error("Data validation error")