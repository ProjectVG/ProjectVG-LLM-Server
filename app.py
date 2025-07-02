from fastapi import FastAPI
from src.api.routes import router
from src.utils.logger import setup_logging, get_logger

# 로깅 설정
setup_logging()

# FastAPI 앱 생성
app = FastAPI(
    title="LLM Server API",
    description="OpenAI API를 사용한 채팅 서버",
    version="1.0.0"
)

# 라우터 등록
app.include_router(router)

logger = get_logger(__name__)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    logger.info("루트 엔드포인트 접근")
    return {"message": "LLM Server API", "status": "running"}


if __name__ == "__main__":
    import uvicorn
    logger.info("서버 시작 중...")
    uvicorn.run(app, host="0.0.0.0", port=5601) 