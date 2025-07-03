from fastapi import APIRouter, HTTPException
from src.dto.request_dto import ChatRequest
from src.dto.response_dto import ChatResponse
from src.core.openai_client import OpenAIChatClient
from src.core.system_prompt import SystemPrompt
from src.utils.logger import get_logger
from input import DEFAULT_MEMORY

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
        logger.info(f"채팅 요청 받음: {request.message[:50]}...")
        
        # 메모리 설정 (요청에 메모리가 없으면 기본값 사용)
        memory = request.memory if request.memory else DEFAULT_MEMORY
        
        # SystemPrompt 객체 생성
        system_prompt = SystemPrompt(
            memory=memory,
            current_situation=request.instructions,
            custom_instructions=request.instructions
        )
        
        response_text, custom_response = chat_client.chat(
            user_input=request.message,
            system_prompt=system_prompt,
            instructions=request.instructions
        )
        
        logger.info(f"채팅 응답 완료: {custom_response.response_time:.2f}s")
        return custom_response
        
    except Exception as e:
        logger.error(f"채팅 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail=f"채팅 처리 중 오류: {str(e)}")


@router.get("/hello")
async def hello():
    """Hello World 체크용 엔드포인트"""
    logger.info("Hello 엔드포인트 접근")    
    return {"message": "Hello, World!", "status": "success"} 


@router.get("/")
async def root():
    """루트 엔드포인트"""
    logger.info("루트 엔드포인트 접근")
    return {"message": "LLM Server API", "status": "running"}