from fastapi import FastAPI
from src.api.routes import router

# FastAPI 앱 생성
app = FastAPI(
    title="LLM Server API",
    description="OpenAI API를 사용한 채팅 서버",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"message": "LLM Server API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5601) 