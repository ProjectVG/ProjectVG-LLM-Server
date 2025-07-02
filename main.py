from dotenv import load_dotenv
import os
from openai import OpenAI
from openai.types.responses import Response
from datetime import datetime

import logging


load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class OpenAIChatClient:
    """OpenAI API와의 채팅을 담당하는 클래스"""
    
    def __init__(self, api_key: str = None):
        """
        OpenAI 채팅 클라이언트 초기화
        
        Args:
            api_key (str, optional): OpenAI API 키. None이면 환경변수에서 로드
            model (str, optional): 사용할 모델
        """
        self.api_key = api_key or self._load_api_key()
        self.client = OpenAI(api_key=self.api_key)
        self.previous_messages_id = None
        
    def _load_api_key(self) -> str:
        """환경변수에서 API 키 로드"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            logging.info(f"성공적으로 OPENAI_API_KEY를 불러왔습니다: {api_key[:4]}****")
            return api_key
        else:
            raise ValueError("OPENAI_API_KEY를 불러오지 못했습니다.")
    
    def _get_system_prompt(self, memory: list[str] = []) -> dict:
        """시스템 프롬프트 반환"""
        if memory:
            memory_prompt = "\nmemory: " + "\n".join(memory)
        else:
            memory_prompt = ""

        system_prompt = {
            "role": "developer",
            "content": "너는 친구 AI야. 반말로 짧게 말해줘." + memory_prompt
        }
        print(system_prompt)

        return system_prompt
    
    
    def _print_response_info(self, response: Response):
        """API 응답 정보 출력"""
        print(f"""
        ==== Open AI Response Information ====
        ID:         {response.id}
        Model:      {response.model}
        Token Usage:
            Input Tokens: {response.usage.input_tokens}     Output Tokens: {response.usage.output_tokens}
            Total Tokens: {response.usage.total_tokens}
        Output:
            Format:     {response.text.format.type}
        Created At: {datetime.fromtimestamp(response.created_at).strftime("%Y-%m-%d %H:%M:%S")}
    """)
    
    def _request_to_openai(
        self,
        messages: list[dict],
        model: str = "gpt-4o-mini",
        temperature: float = 1.0,
        instructions: str = "",
        previous_messages_id: str | None = None
    ) -> Response:
        """
        OpenAI API 요청

        Args:
            messages (list[dict]): 메시지 리스트
            temperature (float): 온도
            instructions (str): 모델에 대한 지시사항
            previous_messages_id (str | None): 이전 메시지 ID

        Returns:
            Response: OpenAI API 응답
        """
        response = self.client.responses.create(
            model=model,
            input=messages,
            instructions=instructions,
            temperature=temperature,
            previous_response_id=previous_messages_id,
            max_output_tokens=1000
        )

        self._print_response_info(response)
        return response
    
    def chat(
        self,
        user_input: str,
        model: str = "gpt-4o-mini",
        instructions: str = "",
        memory: list[str] = [],
    ) -> tuple[str, Response]:
        """
        사용자 입력에 대한 채팅 응답 생성
        
        Args:
            user_input (str): 사용자 입력
            model (str): 사용할 모델
            instructions (str): 추가 지시사항
            use_memory (bool): 이전 대화 기억 사용 여부
            memory (list[str]): 이전 대화 기억
            
        Returns:
            tuple[str, Response]: 응답 텍스트와 응답 객체
        """
        system_prompt = self._get_system_prompt(memory)
        messages = [system_prompt]
        
        user_prompt = {
            "role": "user",
            "content": user_input
        }
        messages.append(user_prompt)
        
        response = self._request_to_openai(
            messages=messages,
            model=model,
            instructions=instructions,
            previous_messages_id=self.previous_messages_id
        )
        
        self.previous_messages_id = response.id
        
        return response.output_text, response


def get_user_input_from_console() -> str:
    """콘솔에서 사용자 Input"""
    user_input = str(input("You: "))
    return user_input


def app():
    """메인 애플리케이션"""
    try:
        chat_client = OpenAIChatClient()
        print("OpenAI 채팅 클라이언트가 초기화 완료")
        print("대화를 시작합니다.")
        
        while True:
            user_input = get_user_input_from_console()

            memory = [
                "유저는 파이썬이랑 C#을 사용",
                "나랑 어제 데이트함"
            ]
            
            try:
                reply, response = chat_client.chat(user_input, memory=memory)
                print("AI:", reply)
            except Exception as e:
                logging.error(f"채팅 중 오류 발생: {e}")
                print(f"오류가 발생했습니다: {e}")
                
    except Exception as e:
        logging.error(f"애플리케이션 초기화 실패: {e}")



if __name__ == "__main__":
    app()
