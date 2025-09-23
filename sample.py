import logging
from src.services.chat_service import ChatService
from src.models.request_dto import ChatRequest
from src.utils.error_handler import ErrorHandler
from src.exceptions.chat_exceptions import (
    ChatServiceException,
    OpenAIClientException,
    ValidationException,
    ConfigurationException
)


DEFAULT_MEMORY = [
    "유저는 파이썬이랑 C#을 사용",
    "나랑 어제 데이트함"
]

DEFAULT_ROLE = "당신은 친근하고 유머러스한 AI 어시스턴트입니다. 항상 긍정적이고 도움이 되는 답변을 제공합니다."

def get_user_input_from_console() -> str:
    """콘솔에서 사용자 Input"""
    user_input = str(input("You: "))
    return user_input

def get_memory() -> list[str]:
    """메모리 로드"""
    return DEFAULT_MEMORY

def get_role() -> str:
    """역할 설정 로드"""
    return DEFAULT_ROLE

def app():
    """메인 애플리케이션"""

    print_info = True
    history = []  # 대화 히스토리 (역할:내용 문자열 리스트)

    try:
        chat_service = ChatService()
        error_handler = ErrorHandler()
        print("채팅 서비스가 초기화 완료")
        print("대화를 시작합니다.")
        
        while True:
            user_input = get_user_input_from_console()
            memory = get_memory()
            role = get_role()
            
            # ChatRequest 객체 생성
            request = ChatRequest(
                user_message=user_input,
                memory_context=memory,
                role=role,
                conversation_history=history,
                free_mode=True,
            )
            
            try:
                response = chat_service.process_chat_request(request)
                print("AI:", response.response_text)

                if print_info:
                    response.print_response_info()
                # history에 user/assistant 대화 추가
                history.append(f"user:{user_input}")
                history.append(f"assistant:{response.response_text}")
                
            except ValidationException as e:
                print(f"입력 오류: {e.message}")
                
            except OpenAIClientException as e:
                print(f"AI 서비스 오류: {e.message}")
                
            except ChatServiceException as e:
                print(f"채팅 서비스 오류: {e.message}")
                
            except ConfigurationException as e:
                print(f"설정 오류: {e.message}")
                break
                
            except Exception as e:
                print(f"예상치 못한 오류: {str(e)}")
                
    except Exception as e:
        logging.error(f"애플리케이션 초기화 실패: {e}")


if __name__ == "__main__":
    app()
