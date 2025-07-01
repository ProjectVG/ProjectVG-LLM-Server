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


if __name__ == "__main__":
    check_api_key()