import importlib

from .env import EnvDefineUnit
from .endpoint import EndpointDefineUnit

from . import terminology_alert

class ConfigDefineTool:
    def get_env(self):
        self.env = EnvDefineUnit()
        return self.env
    
    def get_endpoint(self):
        self.endpoint = EndpointDefineUnit()
        return self.endpoint


    def get_mapping(self):
        module = terminology_alert
        return module

if __name__ == "__main__":
    tool = ConfigDefineTool()
    environment = tool.get_env()  # 한번만 호출하고 반환값 사용
    # experiment = tool.get_exp()  # 한번만 호출하고 반환값 사용
    print(environment)