class ChatServiceException(Exception):
    """채팅 서비스 관련 예외"""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "CHAT_SERVICE_ERROR"
        self.details = details or {}


class OpenAIClientException(Exception):
    """OpenAI 클라이언트 관련 예외"""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "OPENAI_CLIENT_ERROR"
        self.details = details or {}


class ValidationException(Exception):
    """데이터 검증 관련 예외"""
    
    def __init__(self, message: str, field: str = None, value: str = None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.value = value


class ConfigurationException(Exception):
    """설정 관련 예외"""
    
    def __init__(self, message: str, config_key: str = None):
        super().__init__(message)
        self.message = message
        self.config_key = config_key 