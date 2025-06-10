from apimanager import HttpxAPIManager



async def get_stock_related_bond_disposal(
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
        "stkrtbd_kndn": "주권 관련 사채권의 종류",
        "tm": "주권 관련 사채권의 종류(회차)",
        "knd": "주권 관련 사채권의 종류(종류)",
        "aqd": "취득일자",
        "bdiscmp_cmpnm": "사채권 발행회사(회사명)",
        "bdiscmp_nt": "사채권 발행회사(국적)",
        "bdiscmp_rp": "사채권 발행회사(대표자)",
        "bdiscmp_cpt": "사채권 발행회사(자본금(원))",
        "bdiscmp_rl_cmpn": "사채권 발행회사(회사와 관계)",
        "bdiscmp_tisstk": "사채권 발행회사(발행주식 총수(주))",
        "bdiscmp_mbsn": "사채권 발행회사(주요사업)",
        "trfdtl_bd_fta": "양도내역(사채의 권면(전자등록)총액(원))",
        "trfdtl_trfprc": "양도내역(양도금액(원)(A))",
        "trfdtl_tast": "양도내역(총자산(원)(B))",
        "trfdtl_tast_vs": "양도내역(총자산대비(%)(A/B))",
        "trfdtl_ecpt": "양도내역(자기자본(원)(C))",
        "trfdtl_ecpt_vs": "양도내역(자기자본대비(%)(A/C))",
        "trf_pp": "양도목적",
        "trf_prd": "양도예정일자",
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
        "od_a_at_t": "사외이사 참석여부(참석(명))",
        "od_a_at_b": "사외이사 참석여부(불참(명))",
        "adt_a_atn": "감사(사외이사가 아닌 감사위원) 참석여부",
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

    
    