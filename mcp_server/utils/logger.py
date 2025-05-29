import os
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logger(LOG_DIR, log_level="DEBUG", retention_days=7):
    """
    기본 TimedRotatingFileHandler를 사용한 단순한 로깅 설정
    """
    # 고정 파일명 설정
    LOG_FILE = os.path.join(LOG_DIR, "application.log")
    
    # 기본 포맷 설정 - 로거 이름과 함수 이름 포함
    formatter = logging.Formatter('{asctime} | {name} | {funcName} | {levelname} | {message}', 
                                 '%Y-%m-%d %H:%M:%S', 
                                 style='{')
    
    # 기본 파일 핸들러 설정 (시간 기반만)
    file_handler = TimedRotatingFileHandler(
        LOG_FILE,
        when='midnight',
        interval=1,
        backupCount=retention_days
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
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
        
    # 단순한 로깅 설정
    root_logger = setup_logger(LOG_DIR)
    
    # 각 로거 사용 예
    root_logger.info("Data processing started")
    root_logger.debug("Raw data received: XYZ")
    root_logger.error("Data validation error")