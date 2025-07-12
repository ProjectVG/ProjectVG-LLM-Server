from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    """채팅 요청 데이터 전송 객체"""
    session_id: Optional[str] = ""
    system_message: Optional[str] = ""
    user_message: Optional[str] = ""
    role: Optional[str] = ""
    instructions: Optional[str] = ""
    conversation_history: Optional[List[str]] = []
    memory_context: Optional[List[str]] = []
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    model: Optional[str] = "gpt-4o-mini"
    openai_api_key: Optional[str] = ""
    free_mode: Optional[bool] = False
    
    def get_system_message(self) -> str:
        """시스템 메시지를 조합하여 반환"""
        system_prompt = f"""
{self.system_message}

{self._format_role()}

{self._format_memory()}

{self._format_instructions()}
        """
        return system_prompt.strip()
    
    def _format_role(self) -> str:
        """역할 설정을 포맷팅"""
        if self.role:
            return f"#역할\n{self.role}\n"
        return ""
    
    def _format_memory(self) -> str:
        """기억 리스트를 포맷팅"""
        if self.memory_context:
            memory_text = "#기억\n"
            for mem in self.memory_context:
                memory_text += f"- {mem}\n"
            return memory_text
        return ""
    
    def _format_instructions(self) -> str:
        """추가 지시사항을 포맷팅"""
        if self.instructions:
            return f"#추가 지시사항\n{self.instructions}\n"
        return "" 