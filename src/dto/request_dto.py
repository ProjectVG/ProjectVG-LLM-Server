from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    """채팅 요청 데이터 전송 객체"""
    session_id: Optional[str] = ""
    system_message: Optional[str] = ""
    user_message: Optional[str] = ""
    conversation_history: Optional[List[str]] = []
    memory_context: Optional[List[str]] = []
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    model: Optional[str] = "gpt-4o-mini" 