Feature: 공시정보 조회

  Scenario: 실제 DART API에서 공시 목록을 조회한다
    Given 환경 변수에 유효한 DART API 키가 설정되어 있다
    When 삼성전자의 공시 목록을 조회하면
    Then 응답 결과는 적어도 하나 이상의 공시를 포함해야 한다
