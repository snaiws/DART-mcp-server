# utils/config_builder.py
import os
import json
from dataclasses import dataclass, asdict, field, is_dataclass
from typing import  Dict, Any



@dataclass
class Configs:
    """여러 종류의 config들을 받아서 자기 자신이 config 데이터클래스가 되는 빌더"""

    def add(self, other):
        if is_dataclass(other):
            return self.from_dataclass(other)
        elif type(other) == dict:
            return self.from_dict(other)
        else:
            raise "type error"
    
    def from_dataclass(self, source_dataclass: object):
        """데이터클래스 소스 추가"""
        source = asdict(source_dataclass)
        for key, value in source.items():
            setattr(self, key, value)
        return self
    
    def from_dict(self, source_dict: Dict[str, Any]):
        """딕셔너리 소스 추가"""
        for key, value in source_dict.items():
            setattr(self, key, value)
        return self

    def from_json(self, file_path: str):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return self.from_dict(data)
    
    def register_env(self):
        """환경변수 등록"""
        d = self.to_dict()
        for key, value in d.items():
            os.environ[key] = str(value)
    
    def to_dict(self):
        return self.__dict__
    
