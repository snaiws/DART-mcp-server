import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PathDefine:
    '''
    파이썬 환경변수
    '''
    PATH_CORPLIST: Path = field(default_factory=lambda: Path(os.getenv("PATH_DATA", "./data/mcp/DART/")) / 'CORPCODE.xml')
    PATH_FINSTATS: Path = field(default_factory=lambda: Path(os.getenv("PATH_DATA", "./data/mcp/DART/")) / 'finstats')
    PATH_DISCLOSURES: Path = field(default_factory=lambda: Path(os.getenv("PATH_DATA", "./data/mcp/DART/")) / 'disclosures')
    PATH_LOG: Path = field(default_factory=lambda: Path(os.getenv("PATH_DATA", "./data/mcp/DART/")) / 'dart.log')
    