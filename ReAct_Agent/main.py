from typing import Union, List
from dotenv import load_dotenv
from langchain.agents import tool

from langchain.agents.format_scratchpad import format_log_to_str

from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool
from langchain.tools.render import render_text_description

from callbacks import AgentCallbackHandler

load_dotenv()


# @ 데코레이터를 사용하여 자동으로 agent의 도구를 만들 수 있다.
@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )  # 입력 문자열의 길이를 반환하는 함수입니다. 이 함수는 에이전트가 사용할 수 있는 도구로 등록됩니다.
    # 입력 문자열에서 공백과 따옴표를 제거한 후 문자의 길이를 반환합니다.

    return len(text)


# 도구 목록에서 주어진 이름의 도구를 찾는 함수입니다. 도구가 없으면 오류를 발생시킵니다.
def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")


if __name__ == "__main__":
    print("Hello ReAct LangChain!")

    # 사용할 도구를 리스트로 정리함 -> 예시에서는 길이출력만
    tools = [get_text_length]

    # 에이전트가 따를 질문-답변 형식입니다. 주어진 질문에 대해 어떤 도구를 사용할 수 있는지, 그 도구를 어떻게 사용하는지를 설명하는 양식입니다.
    template = """
        Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: {agent_scratchpad}
        """

    # 앞서 정의한 템플릿을 PromptTemplate 클래스를 사용해 초기화하고, 도구 목록을 템플릿에 삽입하여 최종적으로 사용 가능한 프롬프트를 만듭니다.
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    # temperature=0은 모델의 응답이 더 결정적이게 설정되었음을 의미하며, 모델이 특정 구문에서 응답을 멈추도록 설정
    llm = ChatOpenAI(
        temperature=0,
        stop=["Final Answer"], # Final Answer에서 멈추도록 추가 설정
        callbacks=[
            AgentCallbackHandler()
        ],  # callback을 통해 log를 출력이 가능함. 주의) 출력이 길어짐..
    )

    # 에이전트가 작업 중 기록한 "생각-행동-관찰" 과정을 저장할 리스트를 초기화 -> "agent_scratchpad"로 사용됨
    intermediate_steps = []

    # 입력, 프롬프트, LLM, 그리고 출력 파서로 이루어진 ReAct 에이전트입니다(|을 사용하여 파이프라인 형태 구성).
    # 주어진 입력과 기록된 중간 단계 -> "agent_scratchpad" 변수를 받아 최종 응답을 생성하는 데 사용
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(
                x["agent_scratchpad"]
            ),  # langchain 객체 -> llm이 이해할 수 있는데 text화
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    # DOG라는 단어의 길이를 구하는 질문을 입력으로 주고, 에이전트를 호출합니다.
    # agent_scratchpad는 중간 단계 기록입니다. invoke 함수는 결과로 AgentAction 또는 AgentFinish 객체를 반환합니다.
    agent_step = ""
    while not isinstance(agent_step, AgentFinish): # AgentFinish 일때까지 loop
        try:
            agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
                {
                    "input": "What is the length of the word: DOG",
                    "agent_scratchpad": intermediate_steps,
                }
            )
            print(agent_step)

            if isinstance(agent_step, AgentAction):
                tool_name = agent_step.tool
                tool_to_use = find_tool_by_name(tools, tool_name)
                tool_input = agent_step.tool_input.strip().split("\n")[0]  # 첫 번째 줄만 가져오기
                observation = tool_to_use.func(str(tool_input))
                print(f"{observation=}")
                intermediate_steps.append((agent_step, str(observation)))

                # 전이랑 과정이 동일하면 루프 탈출
                if len(intermediate_steps) > 1 and intermediate_steps[-1] == intermediate_steps[-2]:
                    print("Loop detected, stopping agent.")
                    break

        except Exception as e:
            print(f"Error during agent execution: {e}")
            break

    # AgentFinish에 달하면 종료!
    if isinstance(agent_step, AgentFinish):
        print("### AgentFinish ###")
        print(agent_step.return_values)
