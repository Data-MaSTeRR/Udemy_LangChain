from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 링크드인에서 사람정보 불러오는 API
from third_parties.LinkedInJson import scrape_linkedin_profile

if __name__ == "__main__":

    load_dotenv() # .env에서 API_KEY를 가져오기 위함

    # 이제 OPENAI_API_KEY를 환경 변수로 가져옵니다.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please check your .env file or environment variables.")

    print("Hello LangChain")

    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    # prompt에 들어갈 입력에 대한 정의
    summary_prompt_template = PromptTemplate(input_variables=["information"], template = summary_template)

    # 모델이 얼마나 창의적일지를 temperature가 결정
    llm = ChatOpenAI(temperature=0, model_name ="gpt-3.5-turbo", openai_api_key=api_key)

    # prompt에 사용을 원하는 링크드인 유저프로필 url
    likedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/%ED%98%84%EC%9A%B0-%EC%8B%AC-a1162520a/")

    # 위 chain의 invoke 메소드 LLMChain에서 입력 데이터를 언어 모델에게 전달하고, prompt와 LLM을 결합하는 새로운 방식
    res = llm.invoke(summary_prompt_template.format(information= likedin_data))

    print(res)

