from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()


def load_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"Successfully loaded OPENAI_API_KEY: {api_key[:4]}****")
    else:
        print("OPENAI_API_KEY를 불러오지 못함. .env 파일 또는 환경변수를 확인하세요.")
        raise ValueError("OPENAI_API_KEY를 불러오지 못함. .env 파일 또는 환경변수를 확인하세요.")


def load_api_client() -> OpenAI:
    api_key = load_api_key()
    client = OpenAI(api_key=api_key)
    return client



def chat_with_openai(client, messages, model="gpt-4o-mini", temperature=0.7):
    response = client.responses.create(
        model=model,
        input=messages,
        temperature=temperature
    )
    return response.output_text


if __name__ == "__main__":
    client = load_api_client()

    messages = [
        {"role": "system", "content": "너는 친구 AI야. 반말로 짧게 말해줘."},
        {"role": "user", "content": "오늘 무슨일 있니?"}
    ]

    reply = chat_with_openai(client, messages)
    print("AI:", reply)
