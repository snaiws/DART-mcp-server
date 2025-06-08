import os
from dataclasses import dataclass, field
from pathlib import Path

path_data = os.getenv("PATH_DATA", ".")

@dataclass
class PathDefine:
    '''
    파이썬 환경변수
    '''
    PATH_CORPLIST: Path = field(default_factory=lambda: Path(path_data) / 'CORPCODE.xml')
    PATH_FINSTATS: Path = field(default_factory=lambda: Path(path_data) / 'finstats')
    PATH_DISCLOSURES: Path = field(default_factory=lambda: Path(path_data) / 'disclosures')
        
    