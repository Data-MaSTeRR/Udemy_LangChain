import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    scrapes the linkedin profile page, manually scraping the information
    """

    # api 사용없이 일단 테스트 하기 위함
    mock = True

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )

    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f"Bearer {os.getenv('PROXYCURL_API_KEY')}"}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10
        )

    data = response.json()

    # 필요없는 키와 밸류의 빈값 제거해주는 알고리즘 -> dict comprehesion
    data = {
        key: value for key, value in data.items()
        if value not in ([], "", None) and key not in ["people_also_viewed", "certifications"]
    }

    return data

if __name__ == '__main__':
    print(
        # 심현우 링크드인 프로필 주소
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/%ED%98%84%EC%9A%B0-%EC%8B%AC-a1162520a/",
        )
    )
