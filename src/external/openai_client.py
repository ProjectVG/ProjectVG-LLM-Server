from openai import OpenAI
from openai.types.responses import Response
import time
from src.utils.logger import get_logger
from src.config import config
from src.exceptions.chat_exceptions import OpenAIClientException, ConfigurationException

logger = get_logger(__name__)


class OpenAIClient:
    """OpenAI API와의 통신을 담당하는 클래스"""

    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 1000
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or self._load_api_key()
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
        
    def _load_api_key(self) -> str:
        """기본 API Key 로드"""
        api_key = config.get("OPENAI_API_KEY")
        if api_key:
            logger.info(f"성공적으로 OPENAI_API_KEY를 불러왔습니다: {api_key[:4]}****")
            return api_key
        else:
            logger.warning("OPENAI_API_KEY가 설정되지 않았습니다. Free 모드에서만 사용 가능합니다.")
            return None
    
    def _validate_api_key(self, api_key: str) -> bool:
        """API Key 유효성 검증"""
        try:
            test_client = OpenAI(api_key=api_key)
            # 간단한 테스트 요청으로 유효성 확인
            response = test_client.models.list()
            return True
        except Exception as e:
            logger.warning(f"API Key 유효성 검증 실패: {str(e)}")
            return False
    
    def _select_api_key(self, api_key: str = None, free_mode: bool = False) -> tuple[str, str]:
        """
        API Key 선택 및 검증
        """
        default_key = self._load_api_key()
        
        if free_mode:
            if api_key and self._validate_api_key(api_key):
                logger.info("Free 모드: 사용자 제공 API Key 사용")
                return api_key, "user_provided"
            elif default_key:
                logger.info("Free 모드: 기본 API Key 사용")
                return default_key, "default"
            else:
                raise ConfigurationException("Free 모드에서도 유효한 API Key를 찾을 수 없습니다.", config_key="OPENAI_API_KEY")
        
        if api_key and self._validate_api_key(api_key):
            logger.info("일반 모드: 사용자 제공 API Key 사용")
            return api_key, "user_provided"
        else:
            raise ConfigurationException("유효한 OpenAI API Key가 제공되지 않았습니다.", config_key="OPENAI_API_KEY")
    
    def generate_response(
        self,
        messages: list[dict],
        api_key: str = None,
        free_mode: bool = False,
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> tuple[Response, float, str]:
        """
        OpenAI API에 메시지 전송하여 응답 생성
        
        Args:
            messages: OpenAI 형식의 메시지 리스트
            api_key: 사용할 API Key (선택사항)
            free_mode: Free 모드 여부 (기본값: False)
            model: 사용할 모델
            instructions: 추가 지시사항
            max_tokens: 최대 토큰 수
            temperature: 온도
            
        Returns:
            tuple[Response, float, str]: OpenAI 응답, 응답 시간, API Key 소스
            
        Raises:
            OpenAIClientException: OpenAI API 호출 중 오류 발생 시
            ConfigurationException: API Key 설정 오류 시
        """
        start_time = time.time()
        
        # API Key 선택 및 검증
        selected_api_key, api_key_source = self._select_api_key(api_key, free_mode)
        
        try:
            # 선택된 API Key로 클라이언트 생성
            client = OpenAI(api_key=selected_api_key)
            
            logger.debug(f"OpenAI API 요청 시작 (model: {model}, temperature: {temperature}, key_source: {api_key_source})")
            
            response = client.responses.create(
                model=model,
                input=messages,
                instructions=instructions,
                temperature=temperature,
                max_output_tokens=max_tokens
            )

            response_time = time.time() - start_time
            logger.debug(f"OpenAI API 응답 완료 (ID: {response.id}, 시간: {response_time:.2f}s)")
            
            return response, response_time, api_key_source
            
        except Exception as e:
            error_msg = f"OpenAI API 호출 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            raise OpenAIClientException(
                message=error_msg,
                error_code="OPENAI_API_ERROR",
                details={"model": model, "temperature": temperature, "key_source": api_key_source}
            ) 