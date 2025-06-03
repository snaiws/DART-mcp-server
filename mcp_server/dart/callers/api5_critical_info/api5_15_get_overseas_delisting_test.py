import pytest
from configs.config_builder import ConfigDefineTool
from .api5_15_get_overseas_delisting import get_overseas_delisting



@pytest.mark.asyncio
async def test_get_overseas_delisting():
    # Given
    config = ConfigDefineTool()
    env = config.get_env()
    base_url = "https://opendart.fss.or.kr/api"
    endpoint = "/ovDlst.json"
    API_KEY = env.API_KEY
    corp_code = "00344287"
    bgn_de="20190101"
    end_de="20191231"

    # When
    results = await get_overseas_delisting(
        base_url=base_url,
        endpoint=endpoint,
        api_key=API_KEY,
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    )

    # Then
    assert isinstance(results, list)