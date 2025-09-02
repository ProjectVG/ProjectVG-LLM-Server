from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
import time


class ChatResponse(BaseModel):
    """채팅 응답 데이터 클래스 (OpenAI Response 구조 기반)"""
    
    # OpenAI Response 기본 정보
    id: str                 = Field(description="OpenAI Response ID")
    request_id: str         = Field(description="세션 ID")
    object: str             = Field(default="response", description="응답 객체 타입")
    created_at: int         = Field(default_factory=lambda: int(time.time()), description="생성 시간 (Unix timestamp)")
    status: str             = Field(default="completed", description="응답 상태 (completed, failed)")
    model: str              = Field(default="gpt-4o-mini", description="사용된 OpenAI 모델")
    
    # 응답 텍스트
    output_text: str        = Field(default="", description="AI 응답 텍스트")
    
    # 토큰 사용량 정보
    input_tokens: int       = Field(default=0, ge=0, description="입력 토큰 수")
    output_tokens: int      = Field(default=0, ge=0, description="출력 토큰 수")
    total_tokens: int       = Field(default=0, ge=0, description="총 토큰 수")
    cached_tokens: int      = Field(default=0, ge=0, description="캐시된 토큰 수")
    reasoning_tokens: int   = Field(default=0, ge=0, description="추론 토큰 수 (o-series)")
    
    # 응답 형식
    text_format_type: str   = Field(default="text", description="텍스트 형식 타입")
    
    # 비용 정보 (밀리센트 단위)
    cost: Optional[int]     = Field(default=None, ge=0, description="계산된 비용 (밀리센트)")
    
    # 성능 측정
    response_time: Optional[float] = Field(default=None, ge=0.0, description="응답 시간 (초)")
    
    # 상태 정보
    success: bool           = Field(default=True, description="성공 여부")
    error: Optional[str]    = Field(default=None, description="에러 메시지")
    use_user_api_key: bool  = Field(default=False, description="사용자 API Key 사용 여부")
    
    class Config:
        """Pydantic 설정"""
        # JSON 스키마 생성 시 예시 값 제공
        schema_extra = {
            "example": {
                "id": "resp_12345",
                "request_id": "sess_67890",
                "object": "response",
                "created_at": 1641234567,
                "status": "completed",
                "model": "gpt-4o-mini",
                "output_text": "안녕하세요! 도움이 필요하시면 언제든 말씀해 주세요.",
                "input_tokens": 15,
                "output_tokens": 20,
                "total_tokens": 35,
                "cached_tokens": 0,
                "reasoning_tokens": 0,
                "text_format_type": "text",
                "cost": 42,
                "response_time": 1.23,
                "success": True,
                "error": None,
                "use_user_api_key": False
            }
        }
    
    def print_response_info(self):
        """응답 정보 출력"""
        created_datetime = datetime.fromtimestamp(self.created_at)
        print(f"""
==== Chat Response Information ====
ID:         {self.id}
Request ID: {self.request_id}
Status:     {self.status}
Model:      {self.model}
Output:
    Response:   {self.output_text}
    Format:     {self.text_format_type}
Token Usage:
    Input Tokens: {self.input_tokens}     Output Tokens: {self.output_tokens}
    Cached Tokens: {self.cached_tokens}   Reasoning Tokens: {self.reasoning_tokens}
    Total Tokens: {self.total_tokens}
Cost: {self.cost} 밀리센트 if self.cost else 'N/A'
Response Time: {self.response_time:.2f}s if self.response_time else 'N/A'
Created At: {created_datetime.strftime("%Y-%m-%d %H:%M:%S")}
Success: {self.success}
User API Key: {self.use_user_api_key}
        """)
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "request_id": self.request_id,
            "object": self.object,
            "created_at": self.created_at,
            "status": self.status,
            "model": self.model,
            "output_text": self.output_text,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cached_tokens": self.cached_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "text_format_type": self.text_format_type,
            "cost": self.cost,
            "response_time": self.response_time,
            "success": self.success,
            "error": self.error,
            "use_user_api_key": self.use_user_api_key
        }
    
    @classmethod
    def from_openai_response(cls, openai_response, request_id: str = "", response_time: float = None, use_user_api_key: bool = False, cost: int = None):
        """OpenAI Response에서 ChatResponse 생성"""
        # 사용자 API Key 사용 시 비용 측정을 위해 토큰을 0으로 설정
        if use_user_api_key:
            input_tokens = 0
            output_tokens = 0
            total_tokens = 0
            cached_tokens = 0
            reasoning_tokens = 0
        else:
            input_tokens = openai_response.usage.input_tokens
            output_tokens = openai_response.usage.output_tokens
            total_tokens = openai_response.usage.total_tokens
            # 새로운 토큰 세부 정보 추출 - 안전한 방식으로 처리
            cached_tokens = 0
            if hasattr(openai_response.usage, 'input_tokens_details'):
                input_tokens_details = openai_response.usage.input_tokens_details
                if input_tokens_details and hasattr(input_tokens_details, 'cached_tokens'):
                    cached_tokens = getattr(input_tokens_details, 'cached_tokens', 0)
            
            reasoning_tokens = 0
            if hasattr(openai_response.usage, 'output_tokens_details'):
                output_tokens_details = openai_response.usage.output_tokens_details
                if output_tokens_details and hasattr(output_tokens_details, 'reasoning_tokens'):
                    reasoning_tokens = getattr(output_tokens_details, 'reasoning_tokens', 0)
            
        return cls(
            id=openai_response.id,
            request_id=request_id,
            object=openai_response.object,
            created_at=openai_response.created_at,
            status=openai_response.status,
            model=openai_response.model,
            output_text=openai_response.output_text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cached_tokens=cached_tokens,
            reasoning_tokens=reasoning_tokens,
            text_format_type=openai_response.text.format.type,
            cost=cost,
            response_time=response_time,
            success=True,
            use_user_api_key=use_user_api_key
        )
    
    @classmethod
    def create_error_response(cls, request_id: str, error_message: str):
        """에러 응답 생성"""
        current_timestamp = int(time.time())
        return cls(
            id="",
            request_id=request_id,
            object="response",
            created_at=current_timestamp,
            status="failed",
            model="",
            output_text="",
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
            cached_tokens=0,
            reasoning_tokens=0,
            text_format_type="text",
            cost=0,
            response_time=0.0,
            success=False,
            error=error_message,
            use_user_api_key=False
        ) 