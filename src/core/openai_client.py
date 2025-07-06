from openai import OpenAI
from openai.types.responses import Response
from datetime import datetime
import time
from src.dto.response_dto import ChatResponse
from src.utils.logger import get_logger
from src.config import config
from src.core.system_prompt import SystemPrompt

logger = get_logger(__name__)


class OpenAIChatClient:
    """OpenAI API와의 채팅을 담당하는 클래스"""

    DEFAULT_MODEL = "gpt-4.1-mini"
    DEFAULT_TEMPERATURE = 1.0
    DEFAULT_MAX_TOKENS = 1000
    MAX_HISTORY_LENGTH = 10  # 최대 대화 히스토리 길이
    
    def __init__(self, api_key: str = None):
        """
        OpenAI 채팅 클라이언트 초기화
        
        Args:
            api_key (str, optional): OpenAI API 키. None이면 환경변수에서 로드
            model (str, optional): 사용할 모델. None이면 환경변수에서 로드
        """
        self.api_key = api_key or self._load_api_key()
        self.client = OpenAI(api_key=self.api_key)
        
    def _load_api_key(self) -> str:
        """환경변수에서 API 키 로드"""
        api_key = config.get("OPENAI_API_KEY")
        if api_key:
            logger.info(f"성공적으로 OPENAI_API_KEY를 불러왔습니다: {api_key[:4]}****")
            return api_key
        else:
            logger.error("OPENAI_API_KEY를 불러오지 못했습니다.")
            raise ValueError("OPENAI_API_KEY를 불러오지 못했습니다.")
    
    def _get_system_prompt(self, system_prompt: str, memory: list[str]) -> dict:
        """시스템 프롬프트 반환"""
        system_prompt = SystemPrompt(system_prompt=system_prompt, memory=memory)
        return {
            "role": "system",
            "content": system_prompt.get_system_prompt_form()
        }
    
    def _get_user_prompt(self, user_prompt: str) -> dict:
        """사용자 프롬프트 반환"""
        return {
            "role": "user",
            "content": user_prompt
        }

    def _get_history(self, history: list[str]) -> list[dict]:
        """history 포맷팅: '역할:내용' -> {role: ..., content: ...}"""
        formatted_history = []
        if history:
            for item in history:
                if ":" in item:
                    role, content = item.split(":", 1)
                    role = role.strip().lower()
                    if role in ["user", "assistant"]:
                        formatted_history.append({"role": role, "content": content.strip()})
        
        # 최대 대화 히스토리 길이 제한
        if len(formatted_history) > self.MAX_HISTORY_LENGTH * 2:
            formatted_history = formatted_history[-self.MAX_HISTORY_LENGTH * 2:]

        return formatted_history


    def _request_to_openai(
        self,
        messages: list[dict],
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> Response:
        """
        OpenAI API 요청

        Args:
            messages (list[dict]): 메시지 리스트
            temperature (float): 온도
            instructions (str): 모델에 대한 지시사항

        Returns:
            Response: OpenAI API 응답
        """
        logger.debug(f"OpenAI API 요청 시작 (temperature: {temperature})")
        
        response = self.client.responses.create(
            model=model,
            input=messages,
            instructions=instructions,
            temperature=temperature,
            max_output_tokens=max_tokens
        )

        logger.debug(f"OpenAI API 응답 완료 (ID: {response.id})")
        return response
    
    def chat(
        self,
        session_id: str = "",
        model: str = DEFAULT_MODEL,
        system_prompt: str = "",
        user_prompt: str = "",
        history: list[str] = None,
        memory: list[str] = [],
        instructions: str = "",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> tuple[Response, float]:
        """
        사용자 입력에 대한 채팅 응답 생성
        
        Args:
            user_input (str): 사용자 입력
            system_prompt (SystemPrompt, optional): 시스템 프롬프트 객체
            instructions (str): 추가 지시사항
            memory (list[str]): 이전 대화 기억
            history (list[str]): '역할:내용' 형태의 대화 기록
            session_id (str): 세션 ID
            
        Returns:
            tuple[str, ChatResponse]: 응답 텍스트와 사용자 정의 응답 객체
        """
        start_time = time.time()
        
        system_prompt = self._get_system_prompt(system_prompt, memory) #시스템 프롬포트
        conversation_history = self._get_history(history) #대화 히스토리
        user_prompt = self._get_user_prompt(user_prompt) #사용자 프롬포트

        # 메시지 포멧팅
        messages = [system_prompt] + conversation_history + [user_prompt]
        
        # OpenAI API 요청
        openai_response = self._request_to_openai(
            messages=messages,
            model=model,
            instructions=instructions,
            max_tokens=max_tokens,
            temperature=temperature
        )

        # 응답 시간 계산
        response_time = time.time() - start_time
        
        return openai_response, response_time