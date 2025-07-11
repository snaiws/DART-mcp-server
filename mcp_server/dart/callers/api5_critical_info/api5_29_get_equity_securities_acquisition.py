from apimanager import HttpxAPIManager



async def get_equity_securities_acquisition(
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
        "rcept_no": "접수번호(14자리)",
        "corp_cls": "법인구분",
        "corp_code": "공시대상회사의 고유번호(8자리)",
        "corp_name": "공시대상회사명",
        "iscmp_cmpnm": "발행회사(회사명)",
        "iscmp_nt": "발행회사(국적)",
        "iscmp_rp": "발행회사(대표자)",
        "iscmp_cpt": "발행회사(자본금(원))",
        "iscmp_rl_cmpn": "발행회사(회사와 관계)",
        "iscmp_tisstk": "발행회사(발행주식 총수(주))",
        "iscmp_mbsn": "발행회사(주요사업)",
        "l6m_tpa_nstkaq_atn": "최근 6월 이내 제3자 배정에 의한 신주취득 여부",
        "inhdtl_stkcnt": "양수내역(양수주식수(주))",
        "inhdtl_inhprc": "양수내역(양수금액(원)(A))",
        "inhdtl_tast": "양수내역(총자산(원)(B))",
        "inhdtl_tast_vs": "양수내역(총자산대비(%)(A/B))",
        "inhdtl_ecpt": "양수내역(자기자본(원)(C))",
        "inhdtl_ecpt_vs": "양수내역(자기자본대비(%)(A/C))",
        "atinh_owstkcnt": "양수후 소유주식수 및 지분비율(소유주식수(주))",
        "atinh_eqrt": "양수후 소유주식수 및 지분비율(지분비율(%))",
        "inh_pp": "양수목적",
        "inh_prd": "양수예정일자",
        "dlptn_cmpnm": "거래상대방(회사명(성명))",
        "dlptn_cpt": "거래상대방(자본금(원))",
        "dlptn_mbsn": "거래상대방(주요사업)",
        "dlptn_hoadd": "거래상대방(본점소재지(주소))",
        "dlptn_rl_cmpn": "거래상대방(회사와의 관계)",
        "dl_pym": "거래대금지급",
        "exevl_atn": "외부평가에 관한 사항(외부평가 여부)",
        "exevl_bs_rs": "외부평가에 관한 사항(근거 및 사유)",
        "exevl_intn": "외부평가에 관한 사항(외부평가기관의 명칭)",
        "exevl_pd": "외부평가에 관한 사항(외부평가 기간)",
        "exevl_op": "외부평가에 관한 사항(외부평가 의견)",
        "bddd": "이사회결의일(결정일)",
        "od_a_at_t": "사외이사참석여부(참석(명))",
        "od_a_at_b": "사외이사참석여부(불참(명))",
        "adt_a_atn": "감사(사외이사가 아닌 감사위원) 참석여부",
        "bdlst_atn": "우회상장 해당 여부",
        "n6m_tpai_plann": "향후 6월이내 제3자배정 증자 등 계획",
        "iscmp_bdlst_sf_atn": "발행회사(타법인)의 우회상장 요건 충족여부",
        "ftc_stt_atn": "공정거래위원회 신고대상 여부",
        "popt_ctr_atn": "풋옵션 등 계약 체결여부",
        "popt_ctr_cn": "계약내용"
    }

    transform2 = {
        "Y":"유가",
        "K":"코스닥",
        "N":"코넥스",
        "E":"기타",
    }
    

    result = []
    for datum in data['list']:
        # 법인구분처리
        datum['corp_cls'] = transform2[datum['corp_cls']]
        # dict to string
        datum = [f"{transform1[k]}: {datum.get(k,'-')}" for k in transform1]
        datum = "\n".join(datum)
        result.append(datum)
    return result

    