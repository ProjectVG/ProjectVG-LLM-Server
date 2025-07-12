from fastapi import APIRouter, HTTPException
from src.dto.request_dto import ChatRequest
from src.dto.response_dto import ChatResponse
from src.services.chat_service import ChatService
from src.utils.logger import get_logger
from src.utils.error_handler import ErrorHandler
from src.exceptions.chat_exceptions import (
    ChatServiceException,
    OpenAIClientException,
    ValidationException,
    ConfigurationException
)

# 로거 설정
logger = get_logger(__name__)

# 라우터 생성
router = APIRouter(prefix="/api/v1", tags=["chat"])

# 서비스 및 에러 핸들러 인스턴스
chat_service = ChatService()
error_handler = ErrorHandler()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    AI와 채팅하는 엔드포인트
    
    Args:
        request: 채팅 요청 데이터
    
    Returns:
        ChatResponse: AI 응답 데이터
    """
    try:
        logger.info(f"채팅 요청 받음: {request.user_message[:50]}...")
        
        # 서비스를 통한 채팅 처리
        response = chat_service.process_chat_request(request)
        
        logger.info(f"채팅 응답 완료: {response.response_time:.2f}s")
        return response
        
    except ValidationException as e:
        logger.warning(f"검증 에러: {e.message}")
        return error_handler.handle_validation_error(e, request.session_id)
        
    except OpenAIClientException as e:
        logger.error(f"OpenAI 클라이언트 에러: {e.message}")
        return error_handler.handle_openai_client_error(e, request.session_id)
        
    except ChatServiceException as e:
        logger.error(f"채팅 서비스 에러: {e.message}")
        return error_handler.handle_chat_service_error(e, request.session_id)
        
    except ConfigurationException as e:
        logger.error(f"설정 에러: {e.message}")
        return error_handler.handle_configuration_error(e, request.session_id)
        
    except Exception as e:
        logger.error(f"예상치 못한 에러: {str(e)}")
        return error_handler.handle_generic_error(e, request.session_id)


@router.get("/")
async def root():
    """루트 엔드포인트"""
    logger.info("루트 엔드포인트 접근")
    return {"message": "LLM Server API", "status": "running"}