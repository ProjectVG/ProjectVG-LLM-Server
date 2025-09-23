from fastapi import APIRouter
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)

system_router = APIRouter(prefix="/api/v1", tags=["system"])

@system_router.get("/health")
async def health_check():
    """간단한 헬스체크 엔드포인트"""
    logger.info("헬스체크 요청 받음")
    return {
        "status": "healthy",
        "service": "LLM Server",
        "timestamp": datetime.now().isoformat()
    } 