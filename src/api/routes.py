from fastapi import APIRouter, HTTPException
import logging
from src.dto import ChatRequest, ChatResponse
from src.core.openai_client import OpenAIChatClient
from input import DEFAULT_MEMORY

# 로거 설정
logger = logging.getLogger(__name__)

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
        logger.info(f"채팅 요청 받음: {request.message[:50]}...")
        
        # 메모리 설정
        memory = request.memory if request.memory else DEFAULT_MEMORY
        
        # 채팅 요청
        response_text, custom_response = chat_client.chat(
            user_input=request.message,
            instructions=request.instructions,
            memory=memory
        )
        
        logger.info(f"채팅 응답 완료: {custom_response.response_time:.2f}s")
        logger.info(f"채팅 응답: {response_text}")
        return custom_response
        
    except Exception as e:
        logger.error(f"채팅 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail=f"채팅 처리 중 오류: {str(e)}")


@router.get("/hello")
async def hello():
    """Hello World 체크용 엔드포인트"""
    return {"message": "Hello, World!", "status": "success"} 