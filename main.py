from dotenv import load_dotenv
import os
from openai import OpenAI
import logging


load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        logging.info(f"성공적으로 OPENAI_API_KEY를 불러왔습니다: {api_key[:4]}****")
    else:
        raise ValueError("OPENAI_API_KEY를 불러오지 못했습니다.")


def load_api_client() -> OpenAI:
    try:
        api_key = load_api_key()
        client = OpenAI(api_key=api_key)
        return client
    except Exception as e:
        logging.error(f"API 클라이언트 로드 실패: {e}")
        raise e



def chat_with_openai(client, messages, model="gpt-4o-mini", temperature=0.7):
    response = client.responses.create(
        model=model,
        input=messages,
        temperature=temperature
    )
    return response.output_text


def app():
    client = load_api_client()

    system_prompt = {
        "role": "system",
        "content": "너는 친구 AI야. 반말로 짧게 말해줘."
    }

    while True:
        user_input = str(input("You: "))

        user_prompt = {
            "role": "user",
            "content": user_input
        }

        messages = [system_prompt, user_prompt]
        reply = chat_with_openai(client, messages)
        print("AI:", reply)


if __name__ == "__main__":
    app()
