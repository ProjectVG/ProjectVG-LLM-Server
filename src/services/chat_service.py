import time
from src.external.openai_client import OpenAIClient
from src.dto.request_dto import ChatRequest, ChatRoleRequest, History
from src.dto.response_dto import ChatResponse
from src.utils.logger import get_logger
from src.utils.cost_calculator import LLMCostCalculator
from src.config import config
from src.exceptions.chat_exceptions import (
    ChatServiceException,
    OpenAIClientException,
    ValidationException,
    ConfigurationException
)

logger = get_logger(__name__)


class ChatService:
    """채팅 비즈니스 로직을 처리하는 서비스 클래스"""
    
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.default_api_key = self._load_default_api_key()
    
    def _load_default_api_key(self) -> str:
        """기본 API Key 로드"""
        api_key = config.get("OPENAI_API_KEY")
        if api_key:
            logger.info(f"성공적으로 OPENAI_API_KEY를 불러왔습니다: {api_key[:4]}****")
            return api_key
        else:
            logger.warning("OPENAI_API_KEY가 설정되지 않았습니다. 사용자 API Key만 사용 가능합니다.")
            return None
    
    def _select_api_key(self, request_api_key: str = None, use_user_api_key: bool = False) -> str:
        """
        API Key 선택 - use_user_api_key가 True면 사용자 키 사용, 아니면 기본 키 사용
        """
        if use_user_api_key and request_api_key:
            logger.debug("사용자 API Key 사용")
            return request_api_key
        elif self.default_api_key:
            logger.debug("기본 API Key 사용")
            return self.default_api_key
        else:
            raise ConfigurationException("사용 가능한 API Key가 없습니다.", config_key="OPENAI_API_KEY")
    
    def _calculate_cost(self, openai_response, use_user_api_key: bool = False) -> int:
        """
        OpenAI 응답을 기반으로 비용 계산 (고성능 최적화 버전)
        
        Args:
            openai_response: OpenAI 응답 객체
            use_user_api_key: 사용자 API Key 사용 여부
            
        Returns:
            int: 계산된 비용 (밀리센트 단위, 정수), 사용자 키 사용 시 0
        """
        if use_user_api_key:
            return 0
        
        try:
            # 토큰 정보 추출
            input_tokens = openai_response.usage.input_tokens
            output_tokens = openai_response.usage.output_tokens
            cached_tokens = getattr(openai_response.usage, 'input_tokens_details', {}).get('cached_tokens', 0)
            reasoning_tokens = getattr(openai_response.usage, 'output_tokens_details', {}).get('reasoning_tokens', 0)
            
            # 고성능 비용 계산 (O(1), 정수 연산만 사용)
            cost = LLMCostCalculator.calculate_cost(
                model=openai_response.model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cached_tokens=cached_tokens,
                reasoning_tokens=reasoning_tokens
            )
            
            logger.debug(f"비용 계산 완료: {cost} 밀리센트 (model: {openai_response.model}, input: {input_tokens}, output: {output_tokens}, cached: {cached_tokens}, reasoning: {reasoning_tokens})")
            return cost
            
        except Exception as e:
            logger.warning(f"비용 계산 중 오류 발생: {str(e)}, 기본값 0 사용")
            return 0
    
    def _create_system_message(self, request) -> dict:
        """시스템 메시지 생성"""
        return {
            "role": "system",
            "content": request.get_system_message()
        }
    
    def _create_user_message(self, user_prompt: str) -> dict:
        return {
            "role": "user",
            "content": user_prompt
        }

    
    def _validate_request(self, request) -> None:
        """요청 데이터 검증"""
        user_prompt = getattr(request, 'user_prompt', None)
        if not user_prompt or user_prompt.strip() == "":
            raise ValidationException(
                message="user_prompt는 필수 필드입니다.",
                field="user_prompt", 
                value=user_prompt
            )
        
        if request.max_tokens and request.max_tokens <= 0:
            raise ValidationException(
                message="max_tokens는 0보다 커야 합니다.",
                field="max_tokens",
                value=str(request.max_tokens)
            )
        
        if request.temperature and (request.temperature < 0 or request.temperature > 2):
            raise ValidationException(
                message="temperature는 0과 2 사이의 값이어야 합니다.",
                field="temperature",
                value=str(request.temperature)
            )
    
    def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        """
        채팅 요청을 처리하여 응답을 반환
        
        Args:
            request: 채팅 요청 데이터
            
        Returns:
            ChatResponse: 채팅 응답 데이터
            
        Raises:
            ChatServiceException: 채팅 서비스 처리 중 오류 발생 시
            ValidationException: 요청 데이터 검증 실패 시
        """
        try:
            logger.debug(f"채팅 요청 처리 시작")
            
            # 요청 데이터 검증
            self._validate_request(request)
            
            # 메시지 구성
            system_message = self._create_system_message(request)
            conversation_history = [item.model_dump() for item in (request.conversation_history or [])]
            user_message = self._create_user_message(request.user_prompt)

            # 메시지 리스트 구성
            messages = [system_message] + conversation_history + [user_message]
            
            # API Key 선택
            selected_api_key = self._select_api_key(request.openai_api_key, request.use_user_api_key)
            use_user_api_key = bool(request.use_user_api_key and request.openai_api_key)
            
            # 응답 시간 측정 시작
            start_time = time.perf_counter()
            
            # OpenAI API 호출
            openai_response = self.openai_client.create_response(
                input_data=messages,
                api_key=selected_api_key,
                model=request.model,
                instructions=request.instructions,
                max_output_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            # 응답 시간 계산
            response_time = time.perf_counter() - start_time
            if response_time < 0:
                logger.warning(f"음수 응답 시간 감지: {response_time:.2f}s, 0으로 조정")
                response_time = 0.0
            
            # 비용 계산
            cost = self._calculate_cost(openai_response, use_user_api_key)
            
            # 응답 생성
            response = ChatResponse.from_openai_response(
                openai_response=openai_response,
                request_id=request.request_id,
                response_time=response_time,
                use_user_api_key=use_user_api_key,
                cost=cost
            )
            
            logger.info(f"채팅 응답 처리 완료: {response.response_time:.2f}s (User API Key: {use_user_api_key})")
            return response
            
        except (ValidationException, OpenAIClientException):
            # 검증 에러와 OpenAI 에러는 그대로 재발생
            raise
        except Exception as e:
            error_msg = f"채팅 요청 처리 중 예상치 못한 오류: {str(e)}"
            logger.error(error_msg)
            raise ChatServiceException(
                message=error_msg,
                error_code="CHAT_PROCESSING_ERROR",
                details={"request_id": request.request_id}
            )
    
    def process_chat_role_request(self, request: ChatRoleRequest) -> ChatResponse:
        """
        역할 기반 채팅 요청을 처리하여 응답을 반환
        
        Args:
            request: 역할 기반 채팅 요청 데이터
            
        Returns:
            ChatResponse: 채팅 응답 데이터
            
        Raises:
            ChatServiceException: 채팅 서비스 처리 중 오류 발생 시
            ValidationException: 요청 데이터 검증 실패 시
        """
        try:
            logger.debug(f"역할 채팅 요청 처리 시작")
            
            # 요청 데이터 검증
            self._validate_request(request)
            
            # 메시지 구성
            system_message = self._create_system_message(request)
            conversation_history = [item.model_dump() for item in (request.conversation_history or [])]
            user_message = self._create_user_message(request.user_prompt)

            # 메시지 리스트 구성
            messages = [system_message] + conversation_history + [user_message]
            
            # API Key 선택
            selected_api_key = self._select_api_key(request.openai_api_key, request.use_user_api_key)
            use_user_api_key = bool(request.use_user_api_key and request.openai_api_key)
            
            # 응답 시간 측정 시작
            start_time = time.perf_counter()
            
            # OpenAI API 호출
            openai_response = self.openai_client.create_response(
                input_data=messages,
                api_key=selected_api_key,
                model=request.model,
                instructions=request.instructions,
                max_output_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            # 응답 시간 계산
            response_time = time.perf_counter() - start_time
            if response_time < 0:
                logger.warning(f"음수 응답 시간 감지: {response_time:.2f}s, 0으로 조정")
                response_time = 0.0
            
            # 비용 계산
            cost = self._calculate_cost(openai_response, use_user_api_key)
            
            # 응답 생성
            response = ChatResponse.from_openai_response(
                openai_response=openai_response,
                request_id=request.request_id,
                response_time=response_time,
                use_user_api_key=use_user_api_key,
                cost=cost
            )
            
            logger.info(f"역할 채팅 응답 처리 완료: {response.response_time:.2f}s (User API Key: {use_user_api_key})")
            return response
            
        except (ValidationException, OpenAIClientException):
            # 검증 에러와 OpenAI 에러는 그대로 재발생
            raise
        except Exception as e:
            error_msg = f"역할 채팅 요청 처리 중 예상치 못한 오류: {str(e)}"
            logger.error(error_msg)
            raise ChatServiceException(
                message=error_msg,
                error_code="CHAT_ROLE_PROCESSING_ERROR",
                details={"request_id": request.request_id}
            ) 