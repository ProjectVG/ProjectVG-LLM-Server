from fastapi import HTTPException
from src.models.response_dto import ChatResponse
from src.exceptions.chat_exceptions import (
    ChatServiceException,
    OpenAIClientException,
    ValidationException,
    ConfigurationException
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ErrorHandler:
    """에러 처리 핸들러"""
    
    @staticmethod
    def handle_chat_service_error(exception: ChatServiceException, request_id: str = "") -> ChatResponse:
        """채팅 서비스 에러 처리"""
        logger.error(f"채팅 서비스 에러: {exception.message} (코드: {exception.error_code})")
        
        return ChatResponse.create_error_response(
            request_id=request_id,
            error_message=f"채팅 서비스 오류: {exception.message}"
        )
    
    @staticmethod
    def handle_openai_client_error(exception: OpenAIClientException, request_id: str = "") -> ChatResponse:
        """OpenAI 클라이언트 에러 처리"""
        logger.error(f"OpenAI 클라이언트 에러: {exception.message} (코드: {exception.error_code})")
        
        return ChatResponse.create_error_response(
            request_id=request_id,
            error_message=f"AI 서비스 연결 오류: {exception.message}"
        )
    
    @staticmethod
    def handle_validation_error(exception: ValidationException, request_id: str = "") -> ChatResponse:
        """검증 에러 처리"""
        logger.error(f"검증 에러: {exception.message} (필드: {exception.field}, 값: {exception.value})")
        
        return ChatResponse.create_error_response(
            request_id=request_id,
            error_message=f"입력 데이터 오류: {exception.message}"
        )
    
    @staticmethod
    def handle_configuration_error(exception: ConfigurationException, request_id: str = "") -> ChatResponse:
        """설정 에러 처리"""
        logger.error(f"설정 에러: {exception.message} (키: {exception.config_key})")
        
        return ChatResponse.create_error_response(
            request_id=request_id,
            error_message=f"시스템 설정 오류: {exception.message}"
        )
    
    @staticmethod
    def handle_generic_error(exception: Exception, request_id: str = "") -> ChatResponse:
        """일반 에러 처리"""
        logger.error(f"예상치 못한 에러: {str(exception)}")
        
        return ChatResponse.create_error_response(
            request_id=request_id,
            error_message=f"시스템 오류가 발생했습니다: {str(exception)}"
        )
    
    @staticmethod
    def handle_api_error(exception: Exception, request_id: str = "") -> HTTPException:
        """API 에러 처리 (HTTPException 반환)"""
        logger.error(f"API 에러: {str(exception)}")
        
        if isinstance(exception, ValidationException):
            return HTTPException(status_code=400, detail=exception.message)
        elif isinstance(exception, ConfigurationException):
            return HTTPException(status_code=500, detail=exception.message)
        elif isinstance(exception, (ChatServiceException, OpenAIClientException)):
            return HTTPException(status_code=503, detail=exception.message)
        else:
            return HTTPException(status_code=500, detail="내부 서버 오류") 