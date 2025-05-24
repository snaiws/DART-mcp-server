import pytest

from mcp_server.configs.config_builder import ConfigDefineTool
from .api1_1_search_report import get_disclosurelist

@pytest.mark.asyncio # 테스트가 비동기로 실행되어야 함을 의미한다.
async def test_get_disclosurelist():
    '''
        BDD(Behavior Driven Development) 방식의 GWT(Given-When-Then) 패턴으로 구현된 테스트 함수
    '''
    # Given
    config = ConfigDefineTool()
    env = config.get_env()
    base_url = "https://opendart.fss.or.kr/api"
    endpoint = "/list.json"
    API_KEY = env.API_KEY
    corp_code = "00126380"
    bgn_de="20240101"
    end_de="20241231"

    # When
    results = await get_disclosurelist(
        base_url=base_url,
        endpoint=endpoint,
        api_key=API_KEY,
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    )

    # Then
    assert isinstance(results, list)