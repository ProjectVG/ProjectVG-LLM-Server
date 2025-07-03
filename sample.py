import logging
from src.core.openai_client import OpenAIChatClient
from src.core.system_prompt import SystemPrompt


DEFAULT_MEMORY = [
    "유저는 파이썬이랑 C#을 사용",
    "나랑 어제 데이트함"
]

def get_user_input_from_console() -> str:
    """콘솔에서 사용자 Input"""
    user_input = str(input("You: "))
    return user_input

def get_memory() -> list[str]:
    """메모리 로드"""
    return DEFAULT_MEMORY

def app():
    """메인 애플리케이션"""

    print_info = True

    try:
        chat_client = OpenAIChatClient()
        print("OpenAI 채팅 클라이언트가 초기화 완료")
        print("대화를 시작합니다.")
        
        while True:
            user_input = get_user_input_from_console()
            memory = get_memory()
            
            # SystemPrompt 객체 생성
            system_prompt = SystemPrompt(
                memory=memory,
                current_situation="대화 중",
                custom_instructions=""
            )
            
            try:
                reply, response = chat_client.chat(user_input, system_prompt=system_prompt)
                print("AI:", reply)

                if print_info:
                    response.print_response_info()
                
            except Exception as e:
                logging.error(f"채팅 중 오류 발생: {e}")
                
    except Exception as e:
        logging.error(f"애플리케이션 초기화 실패: {e}")


if __name__ == "__main__":
    app()
