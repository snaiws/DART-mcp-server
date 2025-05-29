from apimanager import HttpxAPIManager



async def get_depositary_receipts_registration(
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
        "rcept_no": "접수번호",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "sbd": "청약기일",
        "pymd": "납입기일",
        "sband": "청약공고일",
        "asand": "배정공고일",
        "asstd": "배정기준일",
        "exstk": "신주인수권 행사대상증권",
        "exprc": "신주인수권 행사가격",
        "expd": "신주인수권 행사기간",
        "rpt_rcpn": "주요사항보고서 접수번호"
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

    