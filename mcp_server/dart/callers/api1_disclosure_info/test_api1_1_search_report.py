import pytest
from pytest_bdd import scenario, given, when, then
from configs import EnvDefineUnit
from .api1_1_search_report import get_disclosurelist

@scenario('disclosure_info.feature', '실제 DART API에서 공시 목록을 조회한다')
def test_real_disclosurelist():
    pass


@pytest.fixture
def context():
    return {}


@given("환경 변수에 유효한 DART API 키가 설정되어 있다", target_fixture="env_config")
def env_config():
    env = EnvDefineUnit()
    assert env.API_KEY and env.API_KEY.strip() != ""
    return env


@when("삼성전자의 공시 목록을 조회하면")
@pytest.mark.asyncio
async def call_real_api(env_config, context):
    env = env_config
    results = await get_disclosurelist(
        base_url=env.BASE_URL,
        endpoint="/list.json",
        api_key=env.API_KEY,
        corp_code="00126380",
        bgn_de="20240101",
        end_de="20241231"
    )
    context["results"] = results


@then("응답 결과는 적어도 하나 이상의 공시를 포함해야 한다")
def check_response(context):
    results = context.get("results")
    assert isinstance(results, list)
    assert len(results) > 0
    print(f"\n✅ 총 {len(results)}건 수신됨")
