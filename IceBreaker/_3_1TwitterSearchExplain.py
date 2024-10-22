from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 링크드인에서 사람정보를 json형태로 불러오는 api
from third_parties.LinkedInJson import scrape_linkedin_profile
# 실시간으로 인터넷에서 링크드인 url 찾는 api
from agents.LinkedInLookupAgent import lookup as linkedin_lookup_agent

# 트윗 정보를 리스트형태로 불러오는 api
from third_parties.Twitter import scrape_user_tweets
# 실시간으로 인터넷에서 링크드인 url 찾는 api
from agents.TwitterLookupAgent import lookup as twitter_lookup_agent

# 문자열 입력 -> 문자열 반환
def ice_break_with(name: str) -> str:

    # 이름 기반으로 url을 찾고
    linkedin_username = linkedin_lookup_agent(name=name)
    # 찾은 url을 이용하여 사람의 정보를 json형태의 data로
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    # 이름을 통해 트위터 계정을 찾고
    twitter_username = twitter_lookup_agent(name=name)
    # 찾은 이름을 이용해 트윗을 리스트형의 data로
    tweets = scrape_user_tweets(username=twitter_username)

    summary_template = """
       given the information about a person from linkedin {information},
       and their latest twitter posts {twitter_posts} I want you to create:
       1. A short summary
       2. two interesting facts about them 

       Use both information from twitter and Linkedin
       """
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    print(res)

if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with(name="Eden Marco")
