from openai import OpenAI
from openai.types.responses import Response
import time
from src.utils.logger import get_logger
from src.config import config

logger = get_logger(__name__)


class OpenAIClient:
    """OpenAI API와의 통신을 담당하는 클래스"""

    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 1000
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or self._load_api_key()
        self.client = OpenAI(api_key=self.api_key)
        
    def _load_api_key(self) -> str:
        api_key = config.get("OPENAI_API_KEY")
        if api_key:
            logger.info(f"성공적으로 OPENAI_API_KEY를 불러왔습니다: {api_key[:4]}****")
            return api_key
        else:
            logger.error("OPENAI_API_KEY를 불러오지 못했습니다.")
            raise ValueError("OPENAI_API_KEY를 불러오지 못했습니다.")
    
    def create_completion(
        self,
        messages: list[dict],
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> tuple[Response, float]:
        """
        OpenAI API에 메시지 전송하여 응답 생성
        
        Args:
            messages: OpenAI 형식의 메시지 리스트
            model: 사용할 모델
            instructions: 추가 지시사항
            max_tokens: 최대 토큰 수
            temperature: 온도
            
        Returns:
            tuple[Response, float]: OpenAI 응답과 응답 시간
        """
        start_time = time.time()
        
        logger.debug(f"OpenAI API 요청 시작 (model: {model}, temperature: {temperature})")
        
        response = self.client.responses.create(
            model=model,
            input=messages,
            instructions=instructions,
            temperature=temperature,
            max_output_tokens=max_tokens
        )

        response_time = time.time() - start_time
        logger.debug(f"OpenAI API 응답 완료 (ID: {response.id}, 시간: {response_time:.2f}s)")
        
        return response, response_time 