from dataclasses import dataclass

from .base import Terminology  # 별도 파일에 선언된 dataclass



@dataclass    
class TerminologyCorpInfo(Terminology):
    corp_name: str = "정식회사명칭"
    corp_name_eng: str = "영문정식회사명칭"
    stock_name: str = "종목명(상장사) 또는 약식명칭(기타법인)"
    stock_code: str = "상장회사인 경우 주식의 종목코드(6자리)"
    ceo_nm: str = "대표자명"
    corp_cls: str = "법인구분(Y(유가), K(코스닥), N(코넥스), E(기타))"
    jurir_no: str = "법인등록번호"
    bizr_no: str = "사업자등록번호"
    adres: str = "주소"
    hm_url: str = "홈페이지"
    ir_url: str = "IR홈페이지"
    phn_no: str = "전화번호"
    fax_no: str = "팩스번호"
    induty_code: str = "업종코드"
    est_dt: str = "설립일"
    acc_mt: str = "결산월"