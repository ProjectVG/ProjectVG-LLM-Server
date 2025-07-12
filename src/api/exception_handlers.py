from fastapi import Request
from fastapi.responses import JSONResponse
from src.dto.response_dto import ChatResponse
from src.exceptions.chat_exceptions import (
    ChatServiceException,
    OpenAIClientException,
    ValidationException,
    ConfigurationException
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


def _extract_session_id(request: Request) -> str:
    """요청에서 session_id를 추출"""
    try:
        body = request.json()
        return body.get("session_id", "")
    except:
        return ""


async def validation_exception_handler(request: Request, exc: ValidationException):
    """검증 예외 핸들러"""
    session_id = _extract_session_id(request)
    logger.warning(f"검증 에러: {exc.message} (필드: {exc.field}, 값: {exc.value})")
    
    error_response = ChatResponse.create_error_response(
        session_id=session_id,
        error_message=f"입력 데이터 오류: {exc.message}"
    )
    
    return JSONResponse(
        status_code=400,
        content=error_response.to_dict()
    )


async def openai_client_exception_handler(request: Request, exc: OpenAIClientException):
    """OpenAI 클라이언트 예외 핸들러"""
    session_id = _extract_session_id(request)
    logger.error(f"OpenAI 클라이언트 에러: {exc.message} (코드: {exc.error_code})")
    
    error_response = ChatResponse.create_error_response(
        session_id=session_id,
        error_message=f"AI 서비스 연결 오류: {exc.message}"
    )
    
    return JSONResponse(
        status_code=503,
        content=error_response.to_dict()
    )


async def chat_service_exception_handler(request: Request, exc: ChatServiceException):
    """채팅 서비스 예외 핸들러"""
    session_id = _extract_session_id(request)
    logger.error(f"채팅 서비스 에러: {exc.message} (코드: {exc.error_code})")
    
    error_response = ChatResponse.create_error_response(
        session_id=session_id,
        error_message=f"채팅 서비스 오류: {exc.message}"
    )
    
    return JSONResponse(
        status_code=503,
        content=error_response.to_dict()
    )


async def configuration_exception_handler(request: Request, exc: ConfigurationException):
    """설정 예외 핸들러"""
    session_id = _extract_session_id(request)
    logger.error(f"설정 에러: {exc.message} (키: {exc.config_key})")
    
    error_response = ChatResponse.create_error_response(
        session_id=session_id,
        error_message=f"시스템 설정 오류: {exc.message}"
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.to_dict()
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """일반 예외 핸들러"""
    session_id = _extract_session_id(request)
    logger.error(f"예상치 못한 에러: {str(exc)}")
    
    error_response = ChatResponse.create_error_response(
        session_id=session_id,
        error_message=f"시스템 오류가 발생했습니다: {str(exc)}"
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.to_dict()
    ) 