import logging
import sys
from typing import Optional


class LoggerConfig:
    """중앙화된 로거 설정 클래스"""
    
    def __init__(
        self,
        level: int = logging.INFO,
        format_string: str = "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        log_file: Optional[str] = None
    ):
        self.level = level
        self.format_string = format_string
        self.log_file = log_file
        self._configured = False
    
    def configure(self):
        """로거 설정 적용"""
        if self._configured:
            return
        
        # 기존 핸들러 제거
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # 포맷터 생성
        formatter = logging.Formatter(self.format_string)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # 파일 핸들러 (선택사항)
        if self.log_file:
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        # 루트 로거 레벨 설정
        root_logger.setLevel(self.level)
        
        self._configured = True


def setup_logging(
    level: int = logging.INFO,
    format_string: str = "%(asctime)s %(levelname)s [%(name)s] %(message)s",
    log_file: Optional[str] = None
):
    """로깅 설정"""
    config = LoggerConfig(level, format_string, log_file)
    config.configure()


def get_logger(name: str = None) -> logging.Logger:
    """로거 인스턴스 반환"""
    if name is None:
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'unknown')
    
    return logging.getLogger(name)


# 편의 함수들
def setup_dev_logging():
    """개발 환경용 로깅 설정"""
    setup_logging(
        level=logging.INFO,
        format_string="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )


def setup_prod_logging(log_file: str = "logs/app.log"):
    """프로덕션 환경용 로깅 설정"""
    setup_logging(
        level=logging.INFO,
        format_string="%(asctime)s %(levelname)s [%(name)s] %(funcName)s:%(lineno)d - %(message)s",
        log_file=log_file
    ) 