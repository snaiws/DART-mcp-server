from dataclasses import dataclass

from .base import Terminology  # 별도 파일에 선언된 dataclass



@dataclass    
class TerminologyCapitalStatus(Terminology):
    rcept_no: str = "접수번호(14자리)"
    corp_cls: str = "법인구분(Y(유가), K(코스닥), N(코넥스), E(기타))"
    corp_code: str = "고유번호(8자리)"
    corp_name: str = "법인명"
    isu_dcrs_de: str = "주식발행 감소일자"
    isu_dcrs_stle: str = "발행 감소 형태"
    isu_dcrs_stock_knd: str = "발행 감소 주식 종류"
    isu_dcrs_qy: str = "발행 감소 수량"
    isu_dcrs_mstvdv_fval_amount: str = "발행 감소 주당 액면 가액"
    isu_dcrs_mstvdv_amount: str = "발행 감소 주당 가액"
    stlm_dt: str = "결산기준일"
        
