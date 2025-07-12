import os
from typing import Optional
from pathlib import Path

class Config:
    """설정 관리 클래스"""
    
    SERVER_PORT = "5601"
    OPENAI_API_KEY = ""
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/app.log"
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_TEMPERATURE = "0.7"
    DEFAULT_MAX_TOKENS = "1000"
    DEFAULT_SYSTEM_MESSAGE = "당신은 도움이 되는 AI 어시스턴트입니다."
    
    def __init__(self):
        self._load_env_file()
        self._load_from_env()
    
    def _load_env_file(self):
        """환경 변수 파일 로드"""
        env_file = Path(".env")
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        if key not in os.environ:
                            os.environ[key] = value
    
    def _load_from_env(self):
        """환경 변수에서 설정 값들을 로드"""
        # 환경 변수가 있으면 고정 값 대신 사용
        if os.environ.get("SERVER_PORT"):
            self.SERVER_PORT = os.environ.get("SERVER_PORT")
        if os.environ.get("OPENAI_API_KEY"):
            self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        if os.environ.get("LOG_LEVEL"):
            self.LOG_LEVEL = os.environ.get("LOG_LEVEL")
        if os.environ.get("LOG_FILE"):
            self.LOG_FILE = os.environ.get("LOG_FILE")
        if os.environ.get("DEFAULT_MODEL"):
            self.DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL")
        if os.environ.get("DEFAULT_TEMPERATURE"):
            self.DEFAULT_TEMPERATURE = os.environ.get("DEFAULT_TEMPERATURE")
        if os.environ.get("DEFAULT_MAX_TOKENS"):
            self.DEFAULT_MAX_TOKENS = os.environ.get("DEFAULT_MAX_TOKENS")
        if os.environ.get("DEFAULT_SYSTEM_MESSAGE"):
            self.DEFAULT_SYSTEM_MESSAGE = os.environ.get("DEFAULT_SYSTEM_MESSAGE")
    
    def get(self, key: str, default: Optional[str] = None) -> str:
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

config = Config() 