import os
import logging
from logging.handlers import TimedRotatingFileHandler
import zipfile

from .now import get_now



def rotator(source, dest):
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(source, os.path.basename(source))
    os.remove(source)


def setup_logging(LOG_DIR, log_level="DEBUG", retention_days=7):
    """
    모든 로거가 같은 파일에 로그를 남기도록 설정하는 함수
    """

    now = get_now(form = "%Y%m%d%H%M%S")

    # 로그 파일 경로 설정 (하나의 통합 파일)
    LOG_FILE = os.path.join(LOG_DIR, f"{now}.log")
    
    # 기본 포맷 설정 - 로거 이름 포함
    formatter = logging.Formatter('{asctime} | {name} | {levelname} | {message}', 
                                 '%Y-%m-%d %H:%M:%S', 
                                 style='{')
    
    # 파일 핸들러 설정
    file_handler = TimedRotatingFileHandler(
        LOG_FILE,
        when='midnight',
        interval=1,
        backupCount=retention_days,
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y%m%d"
    
    # 압축 기능을 위한 rotator 설정
    
    file_handler.rotator = rotator
    
    # 콘솔 출력 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
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
        
    # 통합 로깅 설정
    root_logger = setup_logging(LOG_DIR)
    
    # 각 로거 사용 예
    root_logger.info("Data processing started")
    root_logger.debug("Raw data received: XYZ")
    root_logger.error("Data validation error")
