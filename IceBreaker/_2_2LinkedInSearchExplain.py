from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 링크드인에서 사람정보를 json형태로 불러오는 api
from third_parties.LinkedInJson import scrape_linkedin_profile
# 실시간으로 인터넷에서 링크드인 url 찾는 api
from agents.LinkedInLookupAgent import lookup as linkedin_lookup_agent

# 문자열 입력 -> 문자열 반환
def ice_break_with(name: str) -> str:

    # 이름 기반으로 url을 찾고
    linkedin_username = linkedin_lookup_agent(name=name)
    # 찾은 url을 이용하여 사람의 정보를 json형태의 data로
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": linkedin_data})

    print(res)

if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with(name="Eden Marco")
