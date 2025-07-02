import logging
from openai_client import OpenAIChatClient
from input import DEFAULT_MEMORY


def get_user_input_from_console() -> str:
    """콘솔에서 사용자 Input"""
    user_input = str(input("You: "))
    return user_input

def get_memory() -> list[str]:
    """메모리 로드"""
    return DEFAULT_MEMORY

def app():
    """메인 애플리케이션"""
    try:
        chat_client = OpenAIChatClient()
        print("OpenAI 채팅 클라이언트가 초기화 완료")
        print("대화를 시작합니다.")
        
        while True:
            user_input = get_user_input_from_console()
            memory = get_memory()
            
            try:
                reply, response = chat_client.chat(user_input, memory=memory)
                print("AI:", reply)

                response.print_response_info()
                
            except Exception as e:
                logging.error(f"채팅 중 오류 발생: {e}")
                
    except Exception as e:
        logging.error(f"애플리케이션 초기화 실패: {e}")


if __name__ == "__main__":
    app()
