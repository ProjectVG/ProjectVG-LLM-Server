from src.external.openai_client import OpenAIClient
from src.dto.request_dto import ChatRequest
from src.dto.response_dto import ChatResponse
from src.utils.logger import get_logger
from src.exceptions.chat_exceptions import (
    ChatServiceException,
    OpenAIClientException,
    ValidationException
)

logger = get_logger(__name__)


class ChatService:
    """채팅 비즈니스 로직을 처리하는 서비스 클래스"""
    
    def __init__(self):
        self.openai_client = OpenAIClient()
    
    def _create_system_message(self, request: ChatRequest) -> dict:
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

    def _format_conversation_history(self, history: list[str]) -> list[dict]:
        formatted_history = []
        if history:
            for item in history:
                if ":" in item:
                    role, content = item.split(":", 1)
                    role = role.strip().lower()
                    if role in ["user", "assistant"]:
                        formatted_history.append({"role": role, "content": content.strip()})
        
        return formatted_history
    
    def _validate_request(self, request: ChatRequest) -> None:
        """요청 데이터 검증"""
        if not request.user_message or request.user_message.strip() == "":
            raise ValidationException(
                message="user_message는 필수 필드입니다.",
                field="user_message",
                value=request.user_message
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
            logger.info(f"채팅 요청 처리 시작: {request.user_message[:50]}...")
            
            # 요청 데이터 검증
            self._validate_request(request)
            
            # 메시지 구성
            system_message = self._create_system_message(request)
            conversation_history = self._format_conversation_history(request.conversation_history or [])
            user_message = self._create_user_message(request.user_message)

            # 메시지 리스트 구성
            messages = [system_message] + conversation_history + [user_message]
            
            # OpenAI API 호출
            openai_response, response_time, api_key_source = self.openai_client.generate_response(
                messages=messages,
                api_key=request.openai_api_key,
                free_mode=request.free_mode,
                model=request.model,
                instructions=request.instructions,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            # 응답 생성
            response = ChatResponse.from_openai_response(
                openai_response=openai_response,
                session_id=request.session_id,
                response_time=response_time,
                api_key_source=api_key_source
            )
            
            logger.info(f"채팅 응답 처리 완료: {response.response_time:.2f}s (API Key: {api_key_source})")
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
                details={"session_id": request.session_id}
            ) 