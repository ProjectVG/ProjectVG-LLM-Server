from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def check_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"Successfully loaded OPENAI_API_KEY: {api_key[:4]}****")
    else:
        print("OPENAI_API_KEY를 불러오지 못함. .env 파일 또는 환경변수를 확인하세요.")



def chat_with_openai(messages, model="gpt-4o-mini", temperature=0.7):
    response = openai.responses.create(
        model=model,
        input=messages,
        temperature=temperature
    )
    return response.output_text


if __name__ == "__main__":
    check_api_key()

    messages = [
        {"role": "system", "content": "너는 친구 AI야. 반말로 짧게 말해줘."},
        {"role": "user", "content": "오늘 무슨일 있니?"}
    ]

    reply = chat_with_openai(messages)
    print("AI:", reply)
