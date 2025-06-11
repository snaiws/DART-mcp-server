# 소개

DART-MCP-서버는 한국의 전자공시시스템(DART) API를 활용하여 Claude와 같은 AI 모델이 상장 기업의 공시 정보에 접근할 수 있게 하는 Model Context Protocol(MCP) 서버입니다. 이 서버를 활용하면 금융 데이터, 기업 공시 정보, 재무제표 등을 AI 모델이 쉽게 분석하고 활용할 수 있습니다.

### MCP란 무엇인가?

MCP(Model Context Protocol)는 대규모 언어 모델(LLM)이 외부 데이터 소스 및 도구와 상호작용할 수 있게 해주는 오픈 프로토콜입니다. 2024년 11월 Anthropic이 발표한 이 프로토콜은 AI 모델이 실시간 데이터에 접근하고 다양한 기능을 활용할 수 있도록 표준화된 방식을 제공합니다.

MCP를 활용하면 AI 시스템이 외부 데이터베이스, API, 파일 시스템 등과 연결되어 더 정확하고 최신 정보를 바탕으로 사용자의 요청에 응답할 수 있습니다.

## DART-MCP-서버 기능

DART-MCP-서버는 다음과 같은 전자공시시스템(DART) API 기능을 제공합니다:

- **공시검색**: 기업의 공시 정보를 검색합니다.
- **기업개황**: 기업의 기본 정보를 조회합니다.
- **고유번호 조회**: 기업의 고유번호를 검색합니다.
- **증자(감자) 현황**: 기업의 증자/감자 정보를 확인합니다.
- **그 외 다양한 재무 정보**: 배당, 자기주식, 최대주주, 임원 현황 등 다양한 정보에 접근할 수 있습니다.
- **클로드 데스크탑 APP 등 MCP 클라이언트와 연동하여 사용자 명령에 따라 공시 분석이 가능합니다.**

## 설치 요구 사항

DART-MCP-서버를 사용하기 위해 필요한 사항:

1. [Docker Desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/) 앱 설치
2. [Claude Desktop](https://claude.ai/download) 앱 설치
3. [DART API 키 (금융감독원 전자공시시스템에서 발급)](https://opendart.fss.or.kr/uss/umt/EgovMberInsertView.do)

## 서버 설치 및 설정 방법

### 1. DART API 키 발급받기

1. [DART API 키 신청 페이지](https://opendart.fss.or.kr/api/signup.do)에서 회원가입 후 API 키를 발급받습니다.
2. 발급받은 API 키를 안전하게 보관하세요.

### 2. Claude Desktop 설정

1. Claude Desktop 앱을 설치하고 실행합니다.
2. Claude 메뉴에서 “파일(File)” - "설정(Settings)"을 클릭합니다.
3. 좌측 메뉴에서 "개발자(Developer)"를 선택하고 "설정 편집(Edit Config)"을 클릭합니다.
4. 설정 파일이 열리면 다음과 같이 DART-MCP-서버 설정을 추가합니다:(api-key 부분 수정)
    
    ```json
    {
        "mcpServers": {
    		    "DART": {
    		        "command": "docker",
    		        "args": [
    		            "run",
    		            "--rm",
    		            "-i",
    		            "-v", ".:/app/data/mcp/DART",
    		            "-e", "DART_API_KEY=your-api-key",
    		            "-e", "USECASE=light",
    		            "snaiws/dart:latest"
    		        ]
    		    }
    	  }
    }
    ```
    
5. 설정 파일을 저장합니다.
6. 클로드 좌측 메뉴에서 “파일” - “종료”를 클릭해서 종료 후 재시작합니다.

## 서버 사용법

### Claude에서 도구 사용하기

Claude Desktop 앱을 재시작하면 하단 입력창에 도구 아이콘(해머 모양)이 표시됩니다. 이 아이콘을 클릭하면 DART-MCP-서버가 제공하는 도구 목록을 확인할 수 있습니다.

### 예시 질문

Claude에게 다음과 같은 질문을 할 수 있습니다:

- "삼성전자의 최근 공시 정보를 검색해줘"
- "네이버의 기업 개황을 알려줘"
- "카카오의 증자 현황을 분석해줘"
- "현대자동차와 기아자동차의 최근 재무제표를 비교해줘"
- "SK하이닉스의 최대주주 현황을 보여줘"
