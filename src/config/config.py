import os
from typing import Optional
from pathlib import Path

class Config:
    """설정 관리 클래스"""
    
    def __init__(self):
        self._load_env_file()
    
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
    
    def get(self, key: str, default: Optional[str] = None) -> str:
        """환경 변수에서 값을 가져옴"""
        return os.environ.get(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """환경 변수에서 정수 값을 가져옴"""
        value = self.get(key)
        try:
            return int(value) if value else default
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """환경 변수에서 불린 값을 가져옴"""
        value = self.get(key, "").lower()
        if value in ("true", "1", "yes", "on"):
            return True
        elif value in ("false", "0", "no", "off"):
            return False
        return default

# 전역 설정 인스턴스
config = Config() 