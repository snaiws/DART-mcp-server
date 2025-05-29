from apimanager import HttpxAPIManager



async def get_debt_securities_registration(
    base_url:str,
    endpoint:str,
    api_key:str, 
    corp_code:str, 
    bgn_de:str, 
    end_de:str
    )->list:
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bgn_de': bgn_de,
        'end_de': end_de
    }

    client = HttpxAPIManager(base_url)

    # 클라이언트로 API 요청 보내기
    response = await client.get(endpoint, params=params)
    
    # 후처리
    data = response.json()
    transform1 = {
        "rcept_no": "접수번호(14자리) - 공시뷰어 연결용",
        "corp_cls": "법인구분 (Y:유가, K:코스닥, N:코넥스, E:기타)",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "tm": "회차",
        "bdnmn": "채무증권 명칭",
        "slmth": "모집(매출)방법",
        "fta": "권면(전자등록)총액",
        "slta": "모집(매출)총액",
        "isprc": "발행가액",
        "intr": "이자율",
        "isrr": "발행수익률",
        "rpd": "상환기일",
        "print_pymint": "원리금지급대행기관",
        "mngt_cmp": "(사채)관리회사",
        "cdrt_int": "신용등급(신용평가기관)",
        "sbd": "청약기일",
        "pymd": "납입기일",
        "sband": "청약공고일",
        "asand": "배정공고일",
        "asstd": "배정기준일",
        "dpcrn": "표시통화",
        "dpcr_amt": "표시통화기준발행규모",
        "usarn": "사용지역",
        "usntn": "사용국가",
        "wnexpl_at": "원화 교환 예정 여부",
        "udtintnm": "인수기관명",
        "grt_int": "보증기관",
        "grt_amt": "보증금액",
        "icmg_mgknd": "담보의 종류",
        "icmg_mgamt": "담보금액",
        "estk_exstk": "지분증권 연계 시 행사대상증권",
        "estk_exrt": "지분증권 연계 시 권리행사비율",
        "estk_exprc": "지분증권 연계 시 권리행사가격",
        "estk_expd": "지분증권 연계 시 권리행사기간",
        "rpt_rcpn": "주요사항보고서 접수번호",
        "drcb_at": "파생결합사채해당여부",
        "drcb_uast": "파생결합사채 기초자산",
        "drcb_optknd": "파생결합사채 옵션종류",
        "drcb_mtd": "파생결합사채 만기일"
    }



    transform2 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "stksen": "증권의종류",
        "stkcnt": "증권수량",
        "fv": "액면가액",
        "slprc": "모집(매출)가액",
        "slta": "모집(매출)총액",
        "slmthn": "모집(매출)방법"
    }
    
    transform3 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "actsen": "인수인구분",
        "actnmn": "인수인명",
        "stksen": "증권의종류",
        "udtcnt": "인수수량",
        "udtamt": "인수금액",
        "udtprc": "인수대가",
        "udtmth": "인수방법"
    }
    
    transform4 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "se": "구분",
        "amt": "금액"
    }

    transform5 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "hdr": "보유자",
        "rl_cmp": "회사와의관계",
        "bfsl_hdstk": "매출전보유증권수",
        "slstk": "매출증권수",
        "atsl_hdstk": "매출후보유증권수"
    }

    transform6 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "grtrs": "부여사유",
        "exavivr": "행사가능 투자자",
        "grtcnt": "부여수량",
        "expd": "행사기간",
        "exprc": "행사가격"
    }

    transform7 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "kndn": "종류",
        "cnt": "수량",
        "fv": "액면가액",
        "slprc": "모집(매출)가액",
        "slta": "모집(매출)총액"
    }

    transform8 = {
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "cmpnm": "회사명",
        "sen": "구분",
        "tast": "총자산",
        "cpt": "자본금",
        "isstk_knd": "발행주식 종류",
        "isstk_cnt": "발행주식수"
    }

    transform9 = {
        "Y":"유가",
        "K":"코스닥",
        "N":"코넥스",
        "E":"기타",
    }
    transform10 = {
        '일반사항' : transform1,
        '증권의종류' : transform2,
        '인수인정보' : transform3,
        '자금의사용목적' : transform4,
        '매출인에관한사항' : transform5,
        '일반청약자환매청구권' : transform6,
        '발행증권' : transform7,
        '당사회사에관한사항' : transform8
    }

    result = []
    for group in data['group']:
        result_group = []
        title = group['title']
        for i, datum in enumerate(group['list']):
            result_group.append(f"{title}_{i+1}")
            # 법인구분처리
            datum['corp_cls'] = transform9[datum['corp_cls']]
            # dict to string
            datum = [f"{transform10[title][k]}: {datum.get(k,'-')}" for k in transform10[title]]
            datum = "\n".join(datum)
            result_group.append(datum)
        result.append('\n'.join(result_group))
    return result

    