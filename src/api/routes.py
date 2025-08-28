from fastapi import APIRouter
from src.dto.request_dto import ChatRequest, ChatRoleRequest
from src.dto.response_dto import ChatResponse
from src.services.chat_service import ChatService
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["chat"])

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    AI와 채팅하는 엔드포인트 (최소 기능)
    
    Args:
        request: 채팅 요청 데이터
    
    Returns:
        ChatResponse: AI 응답 데이터
    """
    logger.info(f"채팅 요청 받음: {request.user_prompt[:50]}...")
    
    response = chat_service.process_chat_request(request)
    
    logger.info(f"채팅 응답 완료: {response.response_time:.2f}s")
    return response


@router.post("/chat-role", response_model=ChatResponse)
async def chat_with_role(request: ChatRoleRequest):
    """
    역할 기반 AI와 채팅하는 엔드포인트 (전체 기능)
    
    Args:
        request: 역할 기반 채팅 요청 데이터
    
    Returns:
        ChatResponse: AI 응답 데이터
    """
    logger.info(f"역할 채팅 요청 받음: {request.user_prompt[:50]}...")
    
    response = chat_service.process_chat_role_request(request)
    
    logger.info(f"역할 채팅 응답 완료: {response.response_time:.2f}s")
    return response


@router.get("/")
async def root():
    """루트 엔드포인트"""
    logger.info("루트 엔드포인트 접근")
    return {"message": "LLM Server API", "status": "running"}