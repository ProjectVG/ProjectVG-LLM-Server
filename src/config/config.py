import os

# 서버 설정 (Memory Server 방식에 맞춰 전역 변수로 정의)
SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8080"))
SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")

# OpenAI API 설정
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
DEFAULT_MAX_TOKENS: int = int(os.getenv("DEFAULT_MAX_TOKENS", "1000"))

# 로깅 설정
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

# 기존 config 객체와의 호환성을 위한 래퍼 클래스 (임시)
class Config:
    """하위 호환성을 위한 설정 클래스"""

    @property
    def SERVER_PORT(self) -> str:
        return str(SERVER_PORT)

    @property
    def OPENAI_API_KEY(self) -> str:
        return OPENAI_API_KEY

    @property
    def LOG_LEVEL(self) -> str:
        return LOG_LEVEL

    @property
    def LOG_FILE(self) -> str:
        return LOG_FILE

    @property
    def DEFAULT_MODEL(self) -> str:
        return DEFAULT_MODEL

    @property
    def DEFAULT_TEMPERATURE(self) -> str:
        return str(DEFAULT_TEMPERATURE)

    @property
    def DEFAULT_MAX_TOKENS(self) -> str:
        return str(DEFAULT_MAX_TOKENS)

    def get(self, key: str, default: str = None) -> str:
        """설정 값에서 값을 가져옴"""
        return getattr(self, key, default)

    def get_int(self, key: str, default: int = 0) -> int:
        """설정 값에서 정수 값을 가져옴"""
        value = self.get(key)
        try:
            return int(value) if value else default
        except (ValueError, TypeError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """설정 값에서 불린 값을 가져옴"""
        value = str(self.get(key, "")).lower()
        if value in ("true", "1", "yes", "on"):
            return True
        elif value in ("false", "0", "no", "off"):
            return False
        return default

# 하위 호환성을 위한 인스턴스 생성
config = Config() 