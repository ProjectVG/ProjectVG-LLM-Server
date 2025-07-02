from dotenv import load_dotenv
import os
from openai import OpenAI
from openai.types.responses import Response
from datetime import datetime
import time
from src.dto.response_dto import ChatResponse
from src.utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class OpenAIChatClient:
    """OpenAI API와의 채팅을 담당하는 클래스"""

    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_TEMPERATURE = 1.0
    DEFAULT_MAX_TOKENS = 1000
    DEFAULT_SYSTEM_PROMPT = "너는 친구 AI야. 반말로 짧게 말해줘."
    
    def __init__(self, api_key: str = None, model: str = DEFAULT_MODEL):
        """
        OpenAI 채팅 클라이언트 초기화
        
        Args:
            api_key (str, optional): OpenAI API 키. None이면 환경변수에서 로드
            model (str, optional): 사용할 모델
        """
        self.api_key = api_key or self._load_api_key()
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.previous_messages_id = None
        
    def _load_api_key(self) -> str:
        """환경변수에서 API 키 로드"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            logger.info(f"성공적으로 OPENAI_API_KEY를 불러왔습니다: {api_key[:4]}****")
            return api_key
        else:
            logger.error("OPENAI_API_KEY를 불러오지 못했습니다.")
            raise ValueError("OPENAI_API_KEY를 불러오지 못했습니다.")
    
    def _get_system_prompt(self, memory: list[str] = []) -> dict:
        """시스템 프롬프트 반환"""
        if memory:
            memory_prompt = "\nmemory: " + "\n".join(memory)
        else:
            memory_prompt = ""

        system_prompt = {
            "role": "developer",
            "content": self.DEFAULT_SYSTEM_PROMPT + memory_prompt
        }

        return system_prompt
    
    def _request_to_openai(
        self,
        messages: list[dict],
        temperature: float = DEFAULT_TEMPERATURE,
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
        logger.debug(f"OpenAI API 요청 시작 (temperature: {temperature})")
        
        response = self.client.responses.create(
            model=self.model,
            input=messages,
            instructions=instructions,
            temperature=temperature,
            previous_response_id=previous_messages_id,
            max_output_tokens=self.DEFAULT_MAX_TOKENS
        )

        logger.debug(f"OpenAI API 응답 완료 (ID: {response.id})")
        return response
    
    def chat(
        self,
        user_input: str,
        instructions: str = "",
        memory: list[str] = [],
    ) -> tuple[str, ChatResponse]:
        """
        사용자 입력에 대한 채팅 응답 생성
        
        Args:
            user_input (str): 사용자 입력
            instructions (str): 추가 지시사항
            memory (list[str]): 이전 대화 기억
            
        Returns:
            tuple[str, ChatResponse]: 응답 텍스트와 사용자 정의 응답 객체
        """
        logger.info(f"채팅 요청 처리 시작: {user_input[:50]}...")
        
        # 요청 시작 시간 기록
        start_time = time.time()
        
        system_prompt = self._get_system_prompt(memory)
        user_prompt = {"role": "user", "content": user_input}

        messages = [system_prompt, user_prompt]
        
        # OpenAI API 요청
        openai_response = self._request_to_openai(
            messages=messages,
            instructions=instructions,
            previous_messages_id=self.previous_messages_id
        )

        # 응답 시간 계산
        response_time = time.time() - start_time

        # 이전 메시지 ID 업데이트
        self.previous_messages_id = openai_response.id
        
        # 응답 결과
        response_text = openai_response.output_text
        response = ChatResponse.from_openai_response(
            openai_response=openai_response,
            response_time=response_time
        )
        
        return response_text, response 