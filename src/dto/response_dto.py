from datetime import datetime
from dataclasses import dataclass
from typing import Optional
import time


@dataclass
class ChatResponse:
    """사용자 정의 채팅 응답 데이터 클래스"""
    
    # 기본 응답 정보
    response_text: str
    response_id: str
    model: str
    
    # 토큰 사용량
    input_tokens: int
    output_tokens: int
    total_tokens: int
    
    # 출력 형식
    output_format: str
    
    # 생성 시간
    created_at: datetime
    
    # 추가 메타데이터
    temperature: Optional[float] = None
    instructions: Optional[str] = None
    
    # 응답 시간 (초)
    response_time: Optional[float] = None
    
    def print_response_info(self):
        """응답 정보 출력"""
        print(f"""
==== Chat Response Information ====
ID:         {self.response_id}
Model:      {self.model}
Output:
    Response:   {self.response_text}
    Format:     {self.output_format}
Token Usage:
    Input Tokens: {self.input_tokens}     Output Tokens: {self.output_tokens}
    Total Tokens: {self.total_tokens}
Response Time: {self.response_time:.2f}s
Created At: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}
        """)
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "response_text": self.response_text,
            "response_id": self.response_id,
            "model": self.model,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "output_format": self.output_format,
            "created_at": self.created_at.isoformat(),
            "temperature": self.temperature,
            "instructions": self.instructions,
            "response_time": self.response_time
        }
    
    @classmethod
    def from_openai_response(cls, openai_response, response_time: float = None):
        """OpenAI Response에서 ChatResponse 생성"""
        return cls(
            response_text=openai_response.output_text,
            response_id=openai_response.id,
            model=openai_response.model,
            input_tokens=openai_response.usage.input_tokens,
            output_tokens=openai_response.usage.output_tokens,
            total_tokens=openai_response.usage.total_tokens,
            output_format=openai_response.text.format.type,
            created_at=datetime.fromtimestamp(openai_response.created_at),
            temperature=openai_response.temperature,
            response_time=response_time
        ) 