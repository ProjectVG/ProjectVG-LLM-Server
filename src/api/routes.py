from fastapi import APIRouter, HTTPException
from src.dto.request_dto import ChatRequest
from src.dto.response_dto import ChatResponse
from src.core.openai_client import OpenAIChatClient
from src.core.system_prompt import SystemPrompt
from src.utils.logger import get_logger
from tests.test_input import DEFAULT_MEMORY
from src.api.system_routes import system_router

# 로거 설정
logger = get_logger(__name__)

# 라우터 생성
router = APIRouter(prefix="/api/v1", tags=["chat"])

# OpenAI 클라이언트 인스턴스
chat_client = OpenAIChatClient()


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
        # 필수 필드 검증
        if not request.user_message or request.user_message.strip() == "":
            error_response = ChatResponse.create_error_response(
                session_id=request.session_id or "",
                error_message="user_message는 필수 필드입니다."
            )
            return error_response
        
        logger.info(f"채팅 요청 받음: {request.user_message[:50]}...")
        
        openai_response, response_time = chat_client.chat(
            session_id=request.session_id,
            model=request.model,
            system_prompt=request.system_message,
            user_prompt=request.user_message,
            history=request.conversation_history,
            memory=request.memory_context,
            role=request.role,
            instructions=request.instructions,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        # 응답 결과
        response = ChatResponse.from_openai_response(
            openai_response=openai_response,
            session_id=request.session_id,
            response_time=response_time
        )
        
        logger.info(f"채팅 응답 완료: {response.response_time:.2f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"채팅 중 오류 발생: {e}")
        error_response = ChatResponse.create_error_response(
            session_id=request.session_id or "",
            error_message=f"채팅 처리 중 오류: {str(e)}"
        )
        return error_response


@router.get("/")
async def root():
    """루트 엔드포인트"""
    logger.info("루트 엔드포인트 접근")
    return {"message": "LLM Server API", "status": "running"}