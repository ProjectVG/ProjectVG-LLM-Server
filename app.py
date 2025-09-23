from fastapi import FastAPI
from src.api.routes import router
from src.api.system_routes import system_router
from src.api.exception_handlers import (
    validation_exception_handler,
    openai_client_exception_handler,
    chat_service_exception_handler,
    configuration_exception_handler,
    generic_exception_handler
)
from src.exceptions.chat_exceptions import (
    ChatServiceException,
    OpenAIClientException,
    ValidationException,
    ConfigurationException
)
from src.utils.logger import setup_logging, get_logger, get_uvicorn_custom_log
from src.config.config import SERVER_PORT, SERVER_HOST
import uvicorn

# 로깅 설정
setup_logging()

# FastAPI 앱 생성
app = FastAPI(
    title="LLM Server API",
    description="OpenAI API를 사용한 채팅 서버",
    version="1.0.0"
)

# 예외 핸들러 등록
app.add_exception_handler(ValidationException, validation_exception_handler)
app.add_exception_handler(OpenAIClientException, openai_client_exception_handler)
app.add_exception_handler(ChatServiceException, chat_service_exception_handler)
app.add_exception_handler(ConfigurationException, configuration_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# 라우터 등록
app.include_router(router)
app.include_router(system_router)

logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info(f"서버 시작 중... (Host: {SERVER_HOST}, Port: {SERVER_PORT})")

    uvicorn.run(
        app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_config=get_uvicorn_custom_log(),
        access_log=True
    ) 