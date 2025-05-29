from apimanager import HttpxAPIManager



async def get_bond_with_warrants_issuance(
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
        "bd_tm": "사채의 종류(회차)",
        "bd_knd": "사채의 종류(종류)",
        "bd_fta": "사채의 권면(전자등록)총액 (원)",
        "atcsc_rmislmt": "정관상 잔여 발행한도 (원)",
        "ovis_fta": "해외발행(권면(전자등록)총액)",
        "ovis_fta_crn": "해외발행(권면(전자등록)총액(통화단위))",
        "ovis_ster": "해외발행(기준환율등)",
        "ovis_isar": "해외발행(발행지역)",
        "ovis_mktnm": "해외발행(해외상장시 시장의 명칭)",
        "fdpp_fclt": "자금조달의 목적(시설자금 (원))",
        "fdpp_bsninh": "자금조달의 목적(영업양수자금 (원))",
        "fdpp_op": "자금조달의 목적(운영자금 (원))",
        "fdpp_dtrp": "자금조달의 목적(채무상환자금 (원))",
        "fdpp_ocsa": "자금조달의 목적(타법인 증권 취득자금 (원))",
        "fdpp_etc": "자금조달의 목적(기타자금 (원))",
        "bd_intr_ex": "사채의 이율(표면이자율 (%))",
        "bd_intr_sf": "사채의 이율(만기이자율 (%))",
        "bd_mtd": "사채만기일",
        "bdis_mthn": "사채발행방법",
        "ex_rt": "신주인수권에 관한 사항(행사비율 (%))",
        "ex_prc": "신주인수권에 관한 사항(행사가액 (원/주))",
        "ex_prc_dmth": "신주인수권에 관한 사항(행사가액 결정방법)",
        "bdwt_div_atn": "신주인수권에 관한 사항(사채와 인수권의 분리여부)",
        "nstk_pym_mth": "신주인수권에 관한 사항(신주대금 납입방법)",
        "nstk_isstk_knd": "신주인수권에 관한 사항(신주인수권 행사에 따라 발행할 주식(종류))",
        "nstk_isstk_cnt": "신주인수권에 관한 사항(신주인수권 행사에 따라 발행할 주식(주식수))",
        "nstk_isstk_tisstk_vs": "신주인수권에 관한 사항(신주인수권 행사에 따라 발행할 주식(주식총수 대비 비율(%)))",
        "expd_bgd": "신주인수권에 관한 사항(권리행사기간(시작일))",
        "expd_edd": "신주인수권에 관한 사항(권리행사기간(종료일))",
        "act_mktprcfl_cvprc_lwtrsprc": "신주인수권에 관한 사항(시가하락에 따른 행사가액 조정(최저 조정가액 (원)))",
        "act_mktprcfl_cvprc_lwtrsprc_bs": "신주인수권에 관한 사항(시가하락에 따른 행사가액 조정(최저 조정가액 근거))",
        "rmislmt_lt70p": "신주인수권에 관한 사항(시가하락에 따른 행사가액 조정(발행당시 행사가액의 70% 미만으로 조정가능한 잔여 발행한도 (원)))",
        "abmg": "합병 관련 사항",
        "sbd": "청약일",
        "pymd": "납입일",
        "rpmcmp": "대표주관회사",
        "grint": "보증기관",
        "bddd": "이사회결의일(결정일)",
        "od_a_at_t": "사외이사 참석여부(참석 (명))",
        "od_a_at_b": "사외이사 참석여부(불참 (명))",
        "adt_a_atn": "감사(감사위원) 참석여부",
        "rs_sm_atn": "증권신고서 제출대상 여부",
        "ex_sm_r": "제출을 면제받은 경우 그 사유",
        "ovis_ltdtl": "당해 사채의 해외발행과 연계된 대차거래 내역",
        "ftc_stt_atn": "공정거래위원회 신고대상 여부"
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

    