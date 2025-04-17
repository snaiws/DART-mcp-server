import httpx


async def get_corpinfo(key:str, url:str, corp_code:str)->str:
    params = {
        'crtfc_key': key,
        'corp_code': corp_code
    }

    # GET 요청 보내기
    with httpx.Client() as client:
        response = client.get(url, params = params)
        
        # 응답 확인
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            print(f"에러 발생: {response.status_code}")
            return None



if __name__ == "__main__":
    url = "https://opendart.fss.or.kr/api/company.json"
    key = ""
    corp_code = "00126380"
    res = get_corpinfo(url, key, corp_code)

    print(res)