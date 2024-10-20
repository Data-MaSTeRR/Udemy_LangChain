import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import OpenAI, ChatOpenAI  # openai 관련 모듈
from langchain.prompts.prompt import PromptTemplate # 프롬포트 구성하는 모듈
from langchain_core.tools import Tool # langchain이 외부환경과 연동되는 각종 도구 ex. 온라인 검색
from langchain.agents import (
    create_react_agent, # react는 agent를 만든데 가장 많이 사용되는 방법 -> agent 구동용 LLM 받음
    AgentExecutor # agent의 런타임
)
from langchain import hub # langchain에서 미리 만든 프롬포트 사용가능

from tools.findURLTavily import get_profile_url_tavily

def lookup(name: str) -> str:

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
        openai_api_key=os.environ["OPENAI_API_KEY"]
    )


    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                          Your answer should contain only a URL"""
    prompt_template =  PromptTemplate(
        template=template, input_variable=["name_of_person"]
    )


    tool_for_agent = [
        Tool(
            name = "Tavily 4 linkedin profile page",
            func = get_profile_url_tavily, # tools에 name -> linkedin url 가져오는 함수 만듦
            description = "useful for when you need get the LinkedIn profile page URL", # 많은 도구들 중 선택하는 기준
        )
    ]

    # hwchase(해리슨 체이스)는 langchain 만든 사람이고, 이 사람의 프롬포트를 agent가 추론 시 사용하게 됨 / 추론 -> 행동 모델
    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tool_for_agent, prompt=react_prompt) # agent 속성 할당
    agent_executor = AgentExecutor(agent=agent, tools=tool_for_agent, verbose=True) # agent가 도구들을 활용하며 react하는 루프

    # agent한테 input -> result 시킴
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]

    return linked_profile_url

