from datetime import datetime

import pytz



def get_now(timezone: str = "UTC", form = "%Y-%m-%d %H:%M:%S") -> str:
    """
    지정한 타임존의 현재 시간을 반환합니다.
    Args:
        timezone (str): 타임존 이름 (예: "Asia/Seoul", "UTC"). 기본값은 "UTC".
    Returns:
        str: 포맷된 현재 시간 (예: "2024-11-30 14:00:00").
    """
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time.strftime(form)



if __name__ == "__main__":
    now = get_now("Asia/Seoul")
    print(now)