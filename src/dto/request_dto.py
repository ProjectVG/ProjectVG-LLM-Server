from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    """채팅 요청 데이터 전송 객체"""
    message: str
    memory: Optional[List[str]] = []
    instructions: Optional[str] = ""
    # history는 '역할:내용' 형태의 문자열 리스트
    history: Optional[List[str]] = [] 