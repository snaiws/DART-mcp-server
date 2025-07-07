import os
from dataclasses import dataclass, field


@dataclass
class ToolDefine:
    '''
    api url endpoint 관리 클래스
    '''
    # 파서
    get_corpcode: dict = field(default_factory=lambda: {"name": "기업코드검색", "base_url": "", "endpoint": "", "path_corplist":os.getenv("PATH_CORPLIST")}) # 1-5 (임의추가)
    get_corp_candidates: dict = field(default_factory=lambda: {"name": "기업코드검색후보", "base_url": "", "endpoint": "", "path_corplist":os.getenv("PATH_CORPLIST")}) # 1-6 (임의추가)
    xmlparser_step1_structure: dict = field(default_factory=lambda: {"name": "xml구조파악"})
    xmlparser_step2_contents: dict = field(default_factory=lambda: {"name": "xml목차파악"})
    xmlparser_step3_query: dict = field(default_factory=lambda: {"name": "xml내용쿼리"})
    xmlparser_get_table_csv: dict = field(default_factory=lambda: {"name": "xml테이블파싱"})

    # 공시정보 (disclosure information)
    get_disclosurelist: dict = field(default_factory=lambda: {"name": "공시검색", "base_url": os.getenv("BASE_URL",""), "endpoint": "/list.json", "api_key": os.getenv("DART_API_KEY","")}) # 1-1
    get_corpinfo: dict = field(default_factory=lambda: {"name": "기업개황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/company.json", "api_key": os.getenv("DART_API_KEY","")}) # 1-2
    get_disclosure: dict = field(default_factory=lambda: {"name": "공시서류원본파일", "base_url": os.getenv("BASE_URL",""), "endpoint": "document.xml", "api_key": os.getenv("DART_API_KEY",""), "path_disclosures":os.getenv("PATH_DISCLOSURES")}) # 1-3
    update_corplist: dict = field(default_factory=lambda: {"name": "고유번호", "base_url": os.getenv("BASE_URL",""), "endpoint": "/corpCode.xml", "api_key": os.getenv("DART_API_KEY",""), "path_base":os.getenv("PATH_DATA")}) # 1-4
    
    # 정기보고서 주요정보 (Regular report key information)
    get_capitalstatus: dict = field(default_factory=lambda: {"name": "증자(감자) 현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/irdsSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-1
    get_dividend_info: dict = field(default_factory=lambda: {"name": "배당에 관한 사항", "base_url": os.getenv("BASE_URL",""), "endpoint": "/alotMatter.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-2
    get_treasury_stock: dict = field(default_factory=lambda: {"name": "자기주식 취득 및 처분 현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/tesstkAcqsDspsSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-3
    get_major_shareholders: dict = field(default_factory=lambda: {"name": "최대주주 현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/hyslrSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-4
    get_major_shareholders_changes: dict = field(default_factory=lambda: {"name": "최대주주 변동현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/hyslrChgSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-5
    get_minority_shareholders: dict = field(default_factory=lambda: {"name": "소액주주 현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/mrhlSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-6
    get_executives: dict = field(default_factory=lambda: {"name": "임원 현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/exctvSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-7
    get_employees: dict = field(default_factory=lambda: {"name": "직원 현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/empSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-8
    get_individual_compensation_over_500m: dict = field(default_factory=lambda: {"name": "이사·감사의 개인별 보수현황(5억원 이상)", "base_url": os.getenv("BASE_URL",""), "endpoint": "/hmvAuditIndvdlBySttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-9
    get_board_total_compensation: dict = field(default_factory=lambda: {"name": "이사·감사 전체의 보수현황(보수지급금액 - 이사·감사 전체)", "base_url": os.getenv("BASE_URL",""), "endpoint": "/hmvAuditAllSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-10
    get_top5_compensation_over_500m: dict = field(default_factory=lambda: {"name": "개인별 보수지급 금액(5억이상 상위5인)", "base_url": os.getenv("BASE_URL",""), "endpoint": "/indvdlByPay.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-11
    get_investment_in_other_corp: dict = field(default_factory=lambda: {"name": "타법인 출자현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/otrCprInvstmntSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-12
    get_total_shares: dict = field(default_factory=lambda: {"name": "주식의 총수 현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/stockTotqySttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-13
    get_debt_securities_issuance: dict = field(default_factory=lambda: {"name": "채무증권 발행실적", "base_url": os.getenv("BASE_URL",""), "endpoint": "/detScritsIsuAcmslt.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-14
    get_commercial_paper_balance: dict = field(default_factory=lambda: {"name": "기업어음증권 미상환 잔액", "base_url": os.getenv("BASE_URL",""), "endpoint": "/entrprsBilScritsNrdmpBlce.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-15
    get_short_term_bond_balance: dict = field(default_factory=lambda: {"name": "단기사채 미상환 잔액", "base_url": os.getenv("BASE_URL",""), "endpoint": "/srtpdPsndbtNrdmpBlce.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-16
    get_corporate_bond_balance: dict = field(default_factory=lambda: {"name": "회사채 미상환 잔액", "base_url": os.getenv("BASE_URL",""), "endpoint": "/cprndNrdmpBlce.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-17
    get_hybrid_securities_balance: dict = field(default_factory=lambda: {"name": "신종자본증권 미상환 잔액", "base_url": os.getenv("BASE_URL",""), "endpoint": "/newCaplScritsNrdmpBlce.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-18
    get_contingent_convertible_balance: dict = field(default_factory=lambda: {"name": "조건부 자본증권 미상환 잔액", "base_url": os.getenv("BASE_URL",""), "endpoint": "/cndlCaplScritsNrdmpBlce.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-19
    get_auditor_opinion: dict = field(default_factory=lambda: {"name": "회계감사인의 명칭 및 감사의견", "base_url": os.getenv("BASE_URL",""), "endpoint": "/accnutAdtorNmNdAdtOpinion.json	", "api_key": os.getenv("DART_API_KEY","")}) # 2-20
    get_audit_service_contract: dict = field(default_factory=lambda: {"name": "감사용역체결현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/adtServcCnclsSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-21
    get_non_audit_service_contract: dict = field(default_factory=lambda: {"name": "회계감사인과의 비감사용역 계약체결 현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/accnutAdtorNonAdtServcCnclsSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-22
    get_outside_directors: dict = field(default_factory=lambda: {"name": "사외이사 및 그 변동현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/outcmpnyDrctrNdChangeSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-23
    get_unregistered_executives_compensation: dict = field(default_factory=lambda: {"name": "미등기임원 보수현황", "base_url": os.getenv("BASE_URL",""), "endpoint": "/unrstExctvMendngSttus.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-24
    get_board_approved_compensation: dict = field(default_factory=lambda: {"name": "이사·감사 전체의 보수현황(주주총회 승인금액)", "base_url": os.getenv("BASE_URL",""), "endpoint": "/drctrAdtAllMendngSttusGmtsckConfmAmount.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-25
    get_board_compensation_by_type: dict = field(default_factory=lambda: {"name": "이사·감사 전체의 보수현황(보수지급금액 - 유형별)", "base_url": os.getenv("BASE_URL",""), "endpoint": "/drctrAdtAllMendngSttusMendngPymntamtTyCl.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-26
    get_public_fund_usage: dict = field(default_factory=lambda: {"name": "공모자금의 사용내역", "base_url": os.getenv("BASE_URL",""), "endpoint": "/pssrpCptalUseDtls.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-27
    get_private_fund_usage: dict = field(default_factory=lambda: {"name": "사모자금의 사용내역", "base_url": os.getenv("BASE_URL",""), "endpoint": "/prvsrpCptalUseDtls.json", "api_key": os.getenv("DART_API_KEY","")}) # 2-28

    # 정기보고서 재무정보 (Regular report financial information)
    get_single_company_accounts: dict = field(default_factory=lambda: {"name": "단일회사 주요계정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/fnlttSinglAcnt.json", "api_key": os.getenv("DART_API_KEY","")}) # 3-1
    get_multi_company_accounts: dict = field(default_factory=lambda: {"name": "다중회사 주요계정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/fnlttMultiAcnt.json", "api_key": os.getenv("DART_API_KEY","")}) # 3-2
    get_xbrl_financial_statements: dict = field(default_factory=lambda: {"name": "재무제표 원본파일(XBRL)", "base_url": os.getenv("BASE_URL",""), "endpoint": "/fnlttXbrl.xml", "api_key": os.getenv("DART_API_KEY",""), "path_finstats":os.getenv("PATH_FINSTATS")}) # 3-3
    get_complete_financial_statements: dict = field(default_factory=lambda: {"name": "단일회사 전체 재무제표", "base_url": os.getenv("BASE_URL",""), "endpoint": "/fnlttSinglAcntAll.json", "api_key": os.getenv("DART_API_KEY","")}) # 3-4
    get_xbrl_taxonomy_format: dict = field(default_factory=lambda: {"name": "XBRL택사노미재무제표양식", "base_url": os.getenv("BASE_URL",""), "endpoint": "/xbrlTaxonomy.json", "api_key": os.getenv("DART_API_KEY","")}) # 3-5
    get_single_company_key_indicators: dict = field(default_factory=lambda: {"name": "단일회사 주요 재무지표", "base_url": os.getenv("BASE_URL",""), "endpoint": "/fnlttSinglIndx.json", "api_key": os.getenv("DART_API_KEY","")}) # 3-6
    get_multi_company_key_indicators: dict = field(default_factory=lambda: {"name": "다중회사 주요 재무지표", "base_url": os.getenv("BASE_URL",""), "endpoint": "/fnlttCmpnyIndx.json", "api_key": os.getenv('DART_API_KEY')}) # 3-7

    # 지분공시 종합정보 (Comprehensive equity disclosure information)
    get_major_holding_reports: dict = field(default_factory=lambda: {"name": "대량보유 상황보고", "base_url": os.getenv("BASE_URL",""), "endpoint": "/majorstock.json", "api_key": os.getenv("DART_API_KEY","")}) # 4-1
    get_executive_major_shareholders_reports: dict = field(default_factory=lambda: {"name": "임원, 주요주주 소유보고", "base_url": os.getenv("BASE_URL",""), "endpoint": "/elestock.json", "api_key": os.getenv("DART_API_KEY","")}) # 4-2

    # 주요사항보고서 주요정보 (Key issues report information)
    get_asset_acquisition_disposal: dict = field(default_factory=lambda: {"name": "자산양수도(기타), 풋백옵션", "base_url": os.getenv("BASE_URL",""), "endpoint": "/astInhtrfEtcPtbkOpt.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-1
    get_default_occurrence: dict = field(default_factory=lambda: {"name": "부도발생", "base_url": os.getenv("BASE_URL",""), "endpoint": "/dfOcr.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-2
    get_business_suspension: dict = field(default_factory=lambda: {"name": "영업정지", "base_url": os.getenv("BASE_URL",""), "endpoint": "/bsnSp.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-3
    get_rehabilitation_filing: dict = field(default_factory=lambda: {"name": "회생절차 개시신청", "base_url": os.getenv("BASE_URL",""), "endpoint": "/ctrcvsBgrq.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-4
    get_dissolution_event: dict = field(default_factory=lambda: {"name": "해산사유 발생", "base_url": os.getenv("BASE_URL",""), "endpoint": "/dsRsOcr.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-5
    get_paid_capital_increase: dict = field(default_factory=lambda: {"name": "유상증자 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/piicDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-6
    get_free_capital_increase: dict = field(default_factory=lambda: {"name": "무상증자 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/fricDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-7
    get_mixed_capital_increase: dict = field(default_factory=lambda: {"name": "유무상증자 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/pifricDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-8
    get_capital_reduction: dict = field(default_factory=lambda: {"name": "감자 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/crDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-9
    get_creditor_management_start: dict = field(default_factory=lambda: {"name": "채권은행 등의 관리절차 개시", "base_url": os.getenv("BASE_URL",""), "endpoint": "/bnkMngtPcbg.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-10
    get_litigation_filing: dict = field(default_factory=lambda: {"name": "소송 등의 제기", "base_url": os.getenv("BASE_URL",""), "endpoint": "/lwstLg.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-11
    get_overseas_listing_decision: dict = field(default_factory=lambda: {"name": "해외 증권시장 주권등 상장 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/ovLstDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-12
    get_overseas_delisting_decision: dict = field(default_factory=lambda: {"name": "해외 증권시장 주권등 상장폐지 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/ovDlstDecsn.json", "api_key": os.getenv('DART_API_KEY')}) # 5-13
    get_overseas_listing: dict = field(default_factory=lambda: {"name": "해외 증권시장 주권등 상장", "base_url": os.getenv("BASE_URL",""), "endpoint": "/ctrcvsBgrq.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-14
    get_overseas_delisting: dict = field(default_factory=lambda: {"name": "해외 증권시장 주권등 상장폐지", "base_url": os.getenv("BASE_URL",""), "endpoint": "/dsRsOcr.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-15
    get_convertible_bond_issuance: dict = field(default_factory=lambda: {"name": "전환사채권 발행결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/cvbdIsDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-16
    get_bond_with_warrants_issuance: dict = field(default_factory=lambda: {"name": "신주인수권부사채권 발행결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/bdwtIsDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-17
    get_exchangeable_bond_issuance: dict = field(default_factory=lambda: {"name": "교환사채권 발행결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/exbdIsDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-18
    get_creditor_management_suspension: dict = field(default_factory=lambda: {"name": "채권은행 등의 관리절차 중단", "base_url": os.getenv("BASE_URL",""), "endpoint": "/bnkMngtPcsp.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-19
    get_contingent_capital_securities_issuance: dict = field(default_factory=lambda: {"name": "상각형 조건부자본증권 발행결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/wdCocobdIsDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-20
    get_treasury_stock_acquisition: dict = field(default_factory=lambda: {"name": "자기주식 취득 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/tsstkAqDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-21
    get_treasury_stock_disposal: dict = field(default_factory=lambda: {"name": "자기주식 처분 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/tsstkDpDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-22
    get_treasury_stock_trust_contract: dict = field(default_factory=lambda: {"name": "자기주식취득 신탁계약 체결 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/tsstkAqTrctrCnsDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-23
    get_treasury_stock_trust_termination: dict = field(default_factory=lambda: {"name": "자기주식취득 신탁계약 해지 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/tsstkAqTrctrCcDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-24
    get_business_transfer_acquisition: dict = field(default_factory=lambda: {"name": "영업양수 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/bsnInhDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-25
    get_business_transfer_disposal: dict = field(default_factory=lambda: {"name": "영업양도 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/bsnTrfDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-26
    get_tangible_asset_acquisition: dict = field(default_factory=lambda: {"name": "유형자산 양수 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/tgastInhDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-27
    get_tangible_asset_disposal: dict = field(default_factory=lambda: {"name": "유형자산 양도 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/tgastTrfDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-28
    get_equity_securities_acquisition: dict = field(default_factory=lambda: {"name": "타법인 주식 및 출자증권 양수결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/otcprStkInvscrInhDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-29
    get_equity_securities_disposal: dict = field(default_factory=lambda: {"name": "타법인 주식 및 출자증권 양도결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/otcprStkInvscrTrfDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-30
    get_stock_related_bond_acquisition: dict = field(default_factory=lambda: {"name": "주권 관련 사채권 양수 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/stkrtbdInhDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-31
    get_stock_related_bond_disposal: dict = field(default_factory=lambda: {"name": "주권 관련 사채권 양도 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "stkrtbdTrfDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-32
    get_merger_decision: dict = field(default_factory=lambda: {"name": "회사합병 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/cmpMgDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-33
    get_split_decision: dict = field(default_factory=lambda: {"name": "회사분할 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/cmpDvDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-34
    get_split_merger_decision: dict = field(default_factory=lambda: {"name": "회사분할합병 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/cmpDvmgDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-35
    get_stock_exchange_transfer_decision: dict = field(default_factory=lambda: {"name": "주식교환·이전 결정", "base_url": os.getenv("BASE_URL",""), "endpoint": "/stkExtrDecsn.json", "api_key": os.getenv("DART_API_KEY","")}) # 5-36

    # 증권신고서 주요정보 (Securities registration statement key information)
    get_equity_securities_registration: dict = field(default_factory=lambda: {"name": "지분증권", "base_url": os.getenv("BASE_URL",""), "endpoint": "/estkRs.json", "api_key": os.getenv("DART_API_KEY","")}) # 6-1
    get_debt_securities_registration: dict = field(default_factory=lambda: {"name": "채무증권", "base_url": os.getenv("BASE_URL",""), "endpoint": "/bdRs.json", "api_key": os.getenv("DART_API_KEY","")}) # 6-2
    get_depositary_receipts_registration: dict = field(default_factory=lambda: {"name": "증권예탁증권", "base_url": os.getenv("BASE_URL",""), "endpoint": "/stkdpRs.json", "api_key": os.getenv("DART_API_KEY","")}) # 6-3
    get_merger_registration: dict = field(default_factory=lambda: {"name": "합병", "base_url": os.getenv("BASE_URL",""), "endpoint": "/mgRs.json", "api_key": os.getenv("DART_API_KEY","")}) # 6-4
    get_comprehensive_stock_exchange_transfer_registration: dict = field(default_factory=lambda: {"name": "주식의포괄적교환,이전", "base_url": os.getenv("BASE_URL",""), "endpoint": "/extrRs.json", "api_key": os.getenv("DART_API_KEY","")}) # 6-5
    get_split_registration: dict = field(default_factory=lambda: {"name": "분할", "base_url": os.getenv("BASE_URL",""), "endpoint": "/dvRs.json", "api_key": os.getenv("DART_API_KEY","")}) # 6-6
