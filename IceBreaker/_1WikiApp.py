from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

if __name__ == "__main__":

    load_dotenv() # .env에서 API_KEY를 가져오기 위함

    # 이제 OPENAI_API_KEY를 환경 변수로 가져옵니다.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please check your .env file or environment variables.")

    print("Hello LangChain")

    information = """
    블록체인에서 **계좌 간 이체**가 발생할 때, 이 과정은 **트랜잭션**으로 기록되고, 해당 트랜잭션은 네트워크 전체에 전파되어 **블록체인에 추가**됩니다. 이 과정은 일반적인 은행 시스템에서의 이체와는 다르게 **중앙화된 기관 없이**, 블록체인 네트워크에서 **탈중앙화**된 방식으로 처리됩니다. 아래에서 블록체인에서 계좌 간 이체가 어떻게 일어나는지 **트랜잭션 처리 과정**을 설명하겠습니다.

    ### 1. **트랜잭션 생성**
    트랜잭션은 **계좌 간 이체**를 의미하며, 특정한 발신자(송신자)가 수신자에게 암호화폐나 자산을 보내는 것을 나타냅니다. 이 트랜잭션은 다음과 같은 중요한 정보를 포함합니다:
    
    - **발신자의 공개키(주소)**: 이체를 요청하는 사람의 지갑 주소.
    - **수신자의 공개키(주소)**: 암호화폐를 받는 사람의 지갑 주소.
    - **이체 금액**: 발신자가 수신자에게 보내는 암호화폐의 양.
    - **트랜잭션 수수료**: 트랜잭션을 처리해줄 채굴자에게 지급하는 수수료.
    - **디지털 서명**: 발신자가 트랜잭션을 승인하기 위해 자신의 개인키를 사용하여 서명한 정보. 이 서명을 통해 트랜잭션이 정당한지 검증할 수 있습니다.
    
    트랜잭션이 생성되면, 발신자는 자신의 **개인키**를 사용해 트랜잭션에 **디지털 서명**을 합니다. 이를 통해 네트워크에서 트랜잭션이 **발신자 본인**에 의해 승인되었음을 보장합니다.
    
    ### 2. **트랜잭션의 네트워크 전파**
    트랜잭션이 생성되면, 이 트랜잭션은 **블록체인 네트워크**에 전파됩니다. 블록체인은 **탈중앙화된 네트워크**이기 때문에, 트랜잭션은 전 세계의 **노드(참여자)**들에게 브로드캐스트됩니다. 각 노드는 트랜잭션을 받아서 **유효성을 검증**한 후, **메모리 풀**(memory pool)이라는 임시 공간에 저장합니다.
    
    - **메모리 풀**은 아직 블록에 포함되지 않은 대기 중인 트랜잭션들을 모아놓은 공간입니다.
    - 채굴자는 이 메모리 풀에서 트랜잭션을 선택하여 블록에 포함시킵니다.
    
    ### 3. **트랜잭션 검증**
    트랜잭션이 네트워크에 전파된 후, 네트워크의 **노드**들은 이 트랜잭션의 **유효성**을 검증합니다. 이 검증 과정은 다음을 포함합니다:
    
    - **발신자의 자산이 충분한지 확인**: 발신자의 계좌(지갑)에 수신자에게 이체할 수 있는 충분한 자산(암호화폐)이 있는지 확인합니다. 만약 자산이 부족하면 트랜잭션은 유효하지 않다고 판단됩니다.
      
    - **디지털 서명 검증**: 발신자의 개인키로 서명된 트랜잭션을 공개키로 검증하여, 이 트랜잭션이 발신자 본인이 승인한 것인지 확인합니다. 이를 통해 트랜잭션이 위조되지 않았음을 보장합니다.
    
    이 검증 과정을 통과하면, 트랜잭션은 **유효한 트랜잭션**으로 간주됩니다.
    
    ### 4. **블록에 포함 및 채굴**
    트랜잭션이 검증된 후, 채굴자(또는 검증자)는 메모리 풀에서 **유효한 트랜잭션들**을 선택하여 새로운 **블록**을 생성합니다. 이 과정에서 트랜잭션이 블록에 포함됩니다.
    
    - **작업 증명(Proof of Work)** 또는 다른 합의 알고리즘을 통해 채굴자는 새로운 블록을 생성하기 위한 **해시값을 찾는 작업**을 수행합니다.
    - 블록이 성공적으로 채굴되면, 그 블록에 포함된 모든 트랜잭션(계좌 간 이체 정보 포함)이 **블록체인에 추가**됩니다.
    
    ### 5. **블록의 네트워크 전파 및 확인**
    채굴자가 새롭게 생성한 블록이 블록체인에 추가되면, 그 블록은 네트워크 전체에 전파됩니다. 블록이 전파되면, 네트워크에 있는 모든 노드들이 해당 블록의 **유효성을 검증**하고, **자신의 블록체인에 추가**하게 됩니다.
    
    - **트랜잭션 확인(confirmation)**: 트랜잭션이 블록에 포함되고 블록체인에 추가된 후, 이 트랜잭션은 **1회의 확인(confirmation)**을 받게 됩니다. 시간이 지나면서 추가적인 블록들이 이어서 쌓이면, 트랜잭션은 더 많은 확인을 받습니다. 일반적으로 6회 이상의 확인이 이루어지면 트랜잭션이 **완전히 안전하다고 간주**됩니다.
    
    ### 6. **이체 완료**
    블록이 블록체인에 추가되면, 발신자의 자산에서 이체 금액이 차감되고, 수신자의 계좌에 해당 금액이 추가됩니다. 이 트랜잭션 정보는 블록체인에 **영구적으로 기록**되며, 이후에는 변경할 수 없습니다.
    
    - **발신자 계좌**: 발신자의 지갑에서 트랜잭션 금액과 수수료가 차감됩니다.
    - **수신자 계좌**: 수신자는 지정된 암호화폐를 자신의 지갑에서 확인할 수 있습니다.
    
    ### 트랜잭션의 주요 단계 요약
    
    1. **트랜잭션 생성**: 발신자가 트랜잭션을 생성하고, 이를 디지털 서명한 후 네트워크에 전송.
    2. **네트워크 전파**: 트랜잭션이 네트워크에 브로드캐스트되어 노드들이 검증.
    3. **트랜잭션 검증**: 노드들이 트랜잭션의 유효성을 검증.
    4. **블록 생성**: 채굴자가 유효한 트랜잭션을 모아 블록을 생성.
    5. **블록 추가**: 블록이 블록체인에 추가되고 네트워크에 전파.
    6. **트랜잭션 완료**: 발신자와 수신자의 계좌가 업데이트되며, 트랜잭션이 완료됨.
    
    ### 결론
    
    블록체인에서 계좌 간 이체가 이루어질 때, 트랜잭션은 **발신자에서 수신자로의 암호화폐 이동**을 나타내며, 이를 통해 네트워크에서 **탈중앙화된 방식으로 거래**가 처리됩니다. 이 트랜잭션은 **디지털 서명**과 **검증** 과정을 통해 안전하게 처리되며, **블록에 기록되어** 영구적으로 보존됩니다.
        
    
    """


    summary_template = """
    주어진 정보를 활용하여 {information} 다음과 같이 만들어줘:
    1. 짧은 요약문
    2. Case Study
    """

    # prompt에 들어갈 입력에 대한 정의
    summary_prompt_template = PromptTemplate(input_variables=["information"], template = summary_template)

    # 모델이 얼마나 창의적일지를 temperature가 결정
    llm = ChatOpenAI(temperature=0, model_name ="gpt-3.5-turbo", openai_api_key=api_key)

    # 위 chain의 invoke 메소드 LLMChain에서 입력 데이터를 언어 모델에게 전달하고, prompt와 LLM을 결합하는 새로운 방식
    res = llm.invoke(summary_prompt_template.format(information= information))

    print(res)

