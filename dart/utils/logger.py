import os
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import zipfile
import glob
import time

# 로그 파일 설정 함수
def setup_logger(LOG_DIR, now):
    """
    INFO, DEBUG, ERROR 로그를 각각 다른 파일에 저장하도록 설정.
    """
    # 로그 파일 경로 설정
    INFO_LOG_FILE = os.path.join(LOG_DIR, f"{now}_info.log")
    DEBUG_LOG_FILE = os.path.join(LOG_DIR, f"{now}_debug.log")
    ERROR_LOG_FILE = os.path.join(LOG_DIR, f"{now}_error.log")
    
    # 기본 포맷 설정
    formatter = logging.Formatter('{asctime} | {levelname} | {message}', 
                                 '%Y-%m-%d %H:%M:%S', 
                                 style='{')
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # 기본 레벨은 가장 낮은 레벨로 설정
    
    # 기존 핸들러 제거 (여러번 호출 시 중복 방지)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # INFO 로그 핸들러
    info_handler = TimedRotatingFileHandler(
        INFO_LOG_FILE,
        when='midnight',     # 매일 자정에 로테이션
        interval=1,          # 1일 간격으로
        backupCount=7,       # 7일 보관
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    info_handler.suffix = "%Y%m%d"
    root_logger.addHandler(info_handler)
    
    # DEBUG 로그 핸들러
    debug_handler = TimedRotatingFileHandler(
        DEBUG_LOG_FILE,
        when='midnight',
        interval=1,
        backupCount=7,
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    debug_handler.suffix = "%Y%m%d"
    root_logger.addHandler(debug_handler)
    
    # ERROR 로그 핸들러
    error_handler = TimedRotatingFileHandler(
        ERROR_LOG_FILE,
        when='midnight',
        interval=1,
        backupCount=30,      # 오류 로그는 30일 보관
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler.suffix = "%Y%m%d"
    root_logger.addHandler(error_handler)
    
    # 콘솔 출력 핸들러도 추가
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 콘솔에는 INFO 이상만 출력
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 압축 기능 추가를 위한 리스너 등록
    # (기본 logging에는 rotation에 대한 압축이 내장되어 있지 않아 직접 구현)
    def namer(name):
        return name + ".zip"
    
    def rotator(source, dest):
        with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(source, os.path.basename(source))
        os.remove(source)
    
    info_handler.rotator = rotator
    debug_handler.rotator = rotator
    error_handler.rotator = rotator
    
    return root_logger

# 테스트용 코드
if __name__ == "__main__":
    # python -m src.utils.logging_setup
    from dotenv import load_dotenv
    load_dotenv(verbose=False)
    
    import sys
    sys.path.append('.')  # 상대 임포트 문제 해결을 위한 경로 추가
    
    try:
        from src.utils.now import get_now  # 절대 경로 임포트로 변경
    except ImportError:
        # 임포트 실패 시 기본값 사용
        def get_now(timezone):
            return time.strftime("%Y%m%d_%H%M%S")

    # 로그 디렉토리 및 파일 설정
    LOG_DIR = os.getenv("PATH_LOG_VIRTUAL", "./logs")  # 기본값 추가
    
    # 로그 디렉토리가 없으면 생성
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        
    now = get_now("Asia/Seoul")
    logger = setup_logger(LOG_DIR, now)
    
    # 로그 테스트
    logging.info("This is an INFO log.")
    logging.debug("This is a DEBUG log.")
    logging.error("This is an ERROR log.")