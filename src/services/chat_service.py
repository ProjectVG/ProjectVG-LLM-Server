from src.external.openai_client import OpenAIClient
from src.core.system_prompt import SystemPrompt
from src.dto.request_dto import ChatRequest
from src.dto.response_dto import ChatResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ChatService:
    """채팅 비즈니스 로직을 처리하는 서비스 클래스"""
    
    def __init__(self):
        self.openai_client = OpenAIClient()
    
    def _create_system_message(self, system_prompt: str, memory: list[str], role: str = "") -> dict:
        system_prompt_obj = SystemPrompt(system_prompt=system_prompt, memory=memory, role=role)
        return {
            "role": "system",
            "content": system_prompt_obj.get_system_prompt_form()
        }
    
    def _create_user_message(self, user_prompt: str) -> dict:
        return {
            "role": "user",
            "content": user_prompt
        }

    def _format_conversation_history(self, history: list[str]) -> list[dict]:
        formatted_history = []
        if history:
            for item in history:
                if ":" in item:
                    role, content = item.split(":", 1)
                    role = role.strip().lower()
                    if role in ["user", "assistant"]:
                        formatted_history.append({"role": role, "content": content.strip()})
        
        return formatted_history
    
    def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        """
        채팅 요청을 처리하여 응답을 반환
        
        Args:
            request: 채팅 요청 데이터
            
        Returns:
            ChatResponse: 채팅 응답 데이터
        """
        try:
            logger.info(f"채팅 요청 처리 시작: {request.user_message[:50]}...")
            
            # 메시지 구성
            system_message = self._create_system_message(
                request.system_message, 
                request.memory_context, 
                request.role
            )
            conversation_history = self._format_conversation_history(request.conversation_history or [])
            user_message = self._create_user_message(request.user_message)

            # 메시지 리스트 구성
            messages = [system_message] + conversation_history + [user_message]
            
            # OpenAI API 호출
            openai_response, response_time = self.openai_client.create_completion(
                messages=messages,
                model=request.model,
                instructions=request.instructions,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            # 응답 생성
            response = ChatResponse.from_openai_response(
                openai_response=openai_response,
                session_id=request.session_id,
                response_time=response_time
            )
            
            logger.info(f"채팅 응답 처리 완료: {response.response_time:.2f}s")
            return response
            
        except Exception as e:
            logger.error(f"채팅 요청 처리 중 오류: {e}")
            return ChatResponse.create_error_response(
                session_id=request.session_id or "",
                error_message=f"채팅 처리 중 오류: {str(e)}"
            ) 