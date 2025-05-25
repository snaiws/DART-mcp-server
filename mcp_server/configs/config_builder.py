from .env import EnvDefineUnit
from .apidefine import ApiDefineUnit
from .usecase import UsecaseDefineUnit

from . import terminology_alert



class ConfigDefineTool:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigDefineTool, cls).__new__(cls)
            # Initialize instance attributes    
            cls._instance.env = None
            cls._instance.api = None
            cls._instance.usecase = None
        return cls._instance
    
    def get_env(self):
        if self.env is None:
            self.env = EnvDefineUnit()
        return self.env
    
    def get_mapping(self):
        module = terminology_alert
        return module
    
    def get_api(self):
        if self.api is None:
            self.api = ApiDefineUnit()
        return self.api
    
    def get_usecase(self):
        if self.usecase is None:
            self.usecase = UsecaseDefineUnit()
        return self.usecase



if __name__ == "__main__":
    tool = ConfigDefineTool()
    environment = tool.get_env()  # 첫 호출: 인스턴스 생성
    
    tool2 = ConfigDefineTool()  # 새로운 변수로 인스턴스 접근
    environment2 = tool2.get_env()  # 동일한 인스턴스 반환
    
    print(environment is environment2)  # True 출력: 동일한 객체임을 확인
    print(tool is tool2)  # True 출력: 동일한 싱글톤 인스턴스임을 확인