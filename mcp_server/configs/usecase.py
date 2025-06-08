from typing import List
from dataclasses import dataclass, asdict, field

@dataclass
class UsecaseDefineUnit:
    '''
    환경변수
    나중에 바뀌는 서버환경마다 적응시킬 수 있을까
    '''
    light:List[str] = field(default_factory=lambda: [
        "get_disclosurelist",
        "get_corpinfo",
        "update_corplist",
        "get_corpcode",
        "get_corp_candidates"
    ])

    main:List[str] = field(default_factory=lambda: [
        "get_disclosurelist",
        "get_corpinfo",
        "update_corplist",
        "get_corpcode",
        "get_corp_candidates",
        "get_capitalstatus",
        "get_dividend_info",
        "get_treasury_stock",
        "get_major_shareholders",
        "get_major_shareholders_changes",
        "get_minority_shareholders",
        "get_executives",
        "get_employees",
        "get_individual_compensation_over_500m",
        "get_board_total_compensation",
        "get_top5_compensation_over_500m",
        "get_investment_in_other_corp",
        "get_total_shares",
        "get_debt_securities_issuance",
        "get_commercial_paper_balance",
        "get_short_term_bond_balance",
        "get_corporate_bond_balance",
        "get_hybrid_securities_balance",
        "get_contingent_convertible_balance",
        "get_auditor_opinion",
        "get_audit_service_contract",
        "get_non_audit_service_contract",
        "get_outside_directors",
        "get_unregistered_executives_compensation",
        "get_board_approved_compensation",
        "get_board_compensation_by_type",
        "get_public_fund_usage",
        "get_private_fund_usage"
    ])

    finance:List[str] = field(default_factory=lambda: [
        "get_disclosurelist",
        "get_corpinfo",
        "update_corplist",
        "get_corpcode",
        "get_corp_candidates",
        "get_single_company_accounts",
        "get_multi_company_accounts",
        "get_xbrl_financial_statements",
        "get_complete_financial_statements",
        "get_xbrl_taxonomy_format",
        "get_single_company_key_indicators"
    ])

    shareholding:List[str] = field(default_factory=lambda: [
        "get_disclosurelist",
        "get_corpinfo",
        "update_corplist",
        "get_corpcode",
        "get_corp_candidates",
        "get_major_holding_reports",
        "get_executive_major_shareholders_reports"
    ])

    critical:List[str] = field(default_factory=lambda: [
        "get_disclosurelist",
        "get_corpinfo",
        "update_corplist",
        "get_corpcode",
        "get_corp_candidates",
        "get_asset_acquisition_disposal",
        "get_rehabilitation_filing",
        "get_dissolution_event",
        "get_paid_capital_increase",
        "get_free_capital_increase",
        "get_mixed_capital_increase",
        "get_capital_reduction",
        "get_convertible_bond_issuance",
        "get_bond_with_warrants_issuance",
        "get_exchangeable_bond_issuance",
        "get_contingent_capital_securities_issuance",
        "get_treasury_stock_acquisition",
        "get_treasury_stock_disposal",
        "get_treasury_stock_trust_contract",
        "get_treasury_stock_trust_termination",
        "get_business_transfer_acquisition",
        "get_business_transfer_disposal",
        "get_tangible_asset_acquisition",
        "get_tangible_asset_disposal",
        "get_equity_securities_acquisition",
        "get_equity_securities_disposal",
        "get_stock_related_bond_acquisition",
        "get_stock_related_bond_disposal",
        "get_merger_decision",
        "get_split_decision",
        "get_split_merger_decision",
        "get_stock_exchange_transfer_decision"
    ])
    
    securities:List[str] = field(default_factory=lambda: [
        "get_disclosurelist",
        "get_corpinfo",
        "update_corplist",
        "get_corpcode",
        "get_corp_candidates",
        "get_equity_securities_registration",
        "get_debt_securities_registration",
        "get_depositary_receipts_registration",
        "get_merger_registration",
        "get_comprehensive_stock_exchange_transfer_registration",
        "get_split_registration"
    ])

    
    
    def to_dict(self):
        return asdict(self)
    

if __name__ == "__main__":
    import json
    endpoint = UsecaseDefineUnit()
    
    d = endpoint.to_dict()
    print(d)
    with open("usecase.json", "w") as f:
        json.dump(d, f)
