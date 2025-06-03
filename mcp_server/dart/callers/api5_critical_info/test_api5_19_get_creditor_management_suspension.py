import pytest

from configs.config_builder import ConfigDefineTool
from dart.callers.api5_critical_info.api5_19_get_creditor_management_suspension import get_creditor_management_suspension

@pytest.mark.asyncio
async def test_get_creditor_management_suspension():
    # Given
    config = ConfigDefineTool()
    env = config.get_env()
    base_url = "https://opendart.fss.or.kr/api"
    endpoint = "/bnkMngtPcsp.json"
    API_KEY = env.API_KEY
    corp_code = "00141608"
    bgn_de="20160101"
    end_de="20161231"

    # When
    results = await get_creditor_management_suspension(
        base_url=base_url,
        endpoint=endpoint,
        api_key=API_KEY,
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    )

    # Then
    assert isinstance(results, list)