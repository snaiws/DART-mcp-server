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
    
    
    def to_dict(self):
        return asdict(self)
    

if __name__ == "__main__":
    import json
    endpoint = UsecaseDefineUnit()
    
    d = endpoint.to_dict()
    print(d)
    with open("usecase.json", "w") as f:
        json.dump(d, f)
