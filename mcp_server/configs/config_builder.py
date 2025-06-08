from typing import Optional
import os
import json

from .env import EnvDefineUnit
from .apidefine import ApiDefineUnit
from .usecase import UsecaseDefineUnit
from . import terminology_alert


def register_env(d):
    for key, value in d.items():
        os.environ[key] = str(value)


@dataclass
class Configs:
    def __post__init__(self):
        self.env: EnvDefineUnit()
        register_env(self.env.to_dict())
        self.path: PathDefineUnit()
        usecase = UsecaseDefineUnit()
        self.api: ApiDefineUnit()
        
        # dynamic exp -> exp받아 만드는 callbacks모음? 이건 이미 코드의영역. json을 원격에서 받아오는애들로. 키 자체가 변함

    @classmethod
    def from_json(cls, json_source: Union[str, dict]):
        if os.path.exists(json_source):
            with open(json_source, 'r', encoding='utf-8') as f:
                data = json.load(f)
        return cls(**data)
    
    @classmethod
    def from_env(cls):
        return cls(
            DEBUG=os.getenv('DEBUG', 'False').lower() == 'true',
            DATABASE_URL=os.getenv('DATABASE_URL', 'sqlite:///app.db'),
            SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key'),
            API_KEY=os.getenv('API_KEY', ''),
            LOG_LEVEL=os.getenv('LOG_LEVEL', 'INFO'),
            PORT=int(os.getenv('PORT', '8000')),
            HOST=os.getenv('HOST', 'localhost')
        )
    
    @classmethod
    def from_dataclass(cls, source_dataclass: object):
        source_data = {}
        for field in fields(source_dataclass):
            value = getattr(source_dataclass, field.name)
            source_data[field.name.upper()] = value
        return cls(**source_data)

    @classmethod
    def load(cls, 
            config_file: Optional[str] = None,
            json_config: Optional[Union[str, dict]] = None
            )
        env_config = cls.from_env()
        config = cls._merge_configs(config, env_config)
            
        json_config_obj = cls.from_json(json_config)
        config = cls._merge_configs(config, json_config_obj)
        
        return config

    def to_dict(self):
        return asdict(self)

    def to_json(self, file_path: Optional[str] = None, indent: int = 2) -> str:
        """현재 설정을 JSON으로 내보내기"""
        config_dict = self.to_dict()
        
        json_string = json.dumps(config_dict, indent=indent, ensure_ascii=False)
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_string)
            print(f"Config saved to: {file_path}")
        
        return json_string
