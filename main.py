from dotenv import load_dotenv
import os
from openai import OpenAI
from openai.types.responses import Response
from datetime import datetime

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



def chat_with_openai(
        client: OpenAI,
        user_input: str,
        previous_messages_id: str | None = None
    ) -> tuple[str, Response]:
    """
    OpenAI API 요청
    """
    system_prompt = get_system_prompt()
    messages = [system_prompt]

    user_prompt = {
        "role": "user",
        "content": user_input
    }

    messages.append(user_prompt)

    model = "gpt-4o-mini"
    temperature = 1.0


    response = request_to_openai(client, messages, model, temperature, previous_messages_id)

    return response.output_text, response



def request_to_openai(
        client: OpenAI,
        messages: list[dict],
        model: str = "gpt-4o-mini",
        temperature: float = 1.0,
        instructions: str = "",
        previous_messages_id: str | None = None
    ) -> Response:
    """
    OpenAI API 요청

    Args:
        client (OpenAI): OpenAI 클라이언트
        messages (list[dict]): 메시지 리스트
        model (str): 모델 이름
        temperature (float): 온도
        instructions (str): 모델에 대한 지시사항
        previous_messages_id (str | None): 이전 메시지 ID

    ## Refrence: https://platform.openai.com/docs/api-reference/responses/create

    Returns:
        Response: OpenAI API 응답
    """
    response = client.responses.create(
        model=model,
        input=messages,
        instructions=instructions,
        temperature=temperature,
        previous_response_id=previous_messages_id,
        max_output_tokens=1000
    )

    print_response(response)

    return response


def print_response(response: Response):
    print(f"""
        ==== Open AI Response Information ====
        ID:         {response.id}
        Model:      {response.model}
        Token Usage:
            Input Tokens: {response.usage.input_tokens}     Output Tokens: {response.usage.output_tokens}
            Total Tokens: {response.usage.total_tokens}
        Output:
            Format:     {response.text.format.type}
        Created At: {datetime.fromtimestamp(response.created_at).strftime("%Y-%m-%d %H:%M:%S")}
    """)



def get_user_input_from_console() -> str:
    """
    콘솔에서 사용자 Input
    """
    user_input = str(input("You: "))
    return user_input


def get_system_prompt() -> str:
    """
    시스템 프롬프트를 반환
    """
    system_prompt = {
        "role": "developer",
        "content": "너는 친구 AI야. 반말로 짧게 말해줘."
    }
    return system_prompt


def app():
    client = load_api_client()

    previous_messages_id = None

    while True:
        user_input = get_user_input_from_console()

        reply, response = chat_with_openai(client, user_input, previous_messages_id)
        print("AI:", reply)

        previous_messages_id = response.id


if __name__ == "__main__":
    app()
