from pydantic import BaseModel, Field
from typing import List, Optional


class History(BaseModel):
    """대화 기록 데이터 타입"""
    role: str       = Field(description="메시지 역할 (user, assistant, system)")
    content: str    = Field(description="메시지 내용")


class ChatRequest(BaseModel):
    """채팅 요청 DTO"""
    request_id: Optional[str]           = Field(default="", description="요청 ID")
    system_prompt: Optional[str]        = Field(default="", description="시스템 프롬프트")
    user_prompt: Optional[str]          = Field(default="", description="사용자 메시지")
    instructions: Optional[str]         = Field(default="", description="추가 지시사항")
    conversation_history: Optional[List[History]] = Field(default_factory=list, description="대화 기록")
    max_tokens: Optional[int]           = Field(default=1000, description="최대 토큰 수")
    temperature: Optional[float]        = Field(default=0.7, ge=0.0, le=2.0, description="응답 다양성 (0.0-2.0)")
    model: Optional[str]                = Field(default="gpt-4o-mini", description="사용할 OpenAI 모델")
    openai_api_key: Optional[str]       = Field(default="", description="사용자 제공 API Key")
    use_user_api_key: Optional[bool]    = Field(default=False, description="사용자 API Key 사용 여부")