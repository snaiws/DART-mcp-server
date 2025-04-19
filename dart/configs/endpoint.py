import os
from dataclasses import dataclass, asdict

@dataclass
class EndpointDefineUnit:
    '''
    api url endpoint 관리 클래스
    '''
    URL_CORPCODE:str = "/corpCode.xml?crtfc_key={api_key}"
    URL_CORPINFO:str = "/company.json"
    URL_DICSLIST:str = "/list.json"
    URL_CAPTSTAT:str = "/irdsSttus.json"

    def to_dict(self):
        return asdict(self)
    

if __name__ == "__main__":
    import json
    endpoint = EndpointDefineUnit()
    
    d = endpoint.to_dict()
    print(d)
    with open("endpoints.json", "w") as f:
        json.dump(d, f)
