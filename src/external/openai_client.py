from openai import OpenAI
from openai.types.responses import Response
from typing import Iterator, Optional, Union, Dict, Any, List
from src.utils.logger import get_logger
from src.exceptions.chat_exceptions import OpenAIClientException

logger = get_logger(__name__)


class OpenAIClient:
    """OpenAI API와의 통신을 담당하는 클래스"""

    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 1000

    def generate_response(
        self,
        messages: list[dict],
        api_key: str,
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> Response:
        """
        OpenAI API에 메시지 전송하여 응답 생성

        Args:
            messages: OpenAI 형식의 메시지 리스트
            api_key: 사용할 API Key (필수)
            model: 사용할 모델
            instructions: 추가 지시사항
            max_tokens: 최대 토큰 수
            temperature: 온도

        Returns:
            Response: OpenAI 응답

        Raises:
            OpenAIClientException: OpenAI API 호출 중 오류 발생 시
        """
        try:
            # API Key로 클라이언트 생성
            client = OpenAI(api_key=api_key)

            logger.debug(f"OpenAI API 요청 시작 (model: {model}, temperature: {temperature})")

            response = client.responses.create(
                model=model,
                input=messages,
                instructions=instructions,
                temperature=temperature,
                max_output_tokens=max_tokens
            )

            logger.debug(f"OpenAI API 응답 완료 (ID: {response.id})")
            return response
            
        except Exception as e:
            error_msg = f"OpenAI API 호출 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            raise OpenAIClientException(
                message=error_msg,
                error_code="OPENAI_API_ERROR",
                details={"model": model, "temperature": temperature}
            )

    def create_chat_completion(
        self,
        messages: List[Dict],
        api_key: str,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        stream: bool = False
    ) -> Union[Response, Iterator[Response]]:
        """
        Chat Completions API를 사용한 채팅 완성 생성

        Args:
            messages: 채팅 메시지 배열
            api_key: 사용할 API Key (필수)
            model: 사용할 모델
            temperature: 온도 설정
            max_tokens: 최대 토큰 수
            stream: 스트리밍 응답 여부

        Returns:
            Response | Iterator[Response]: 응답 객체 또는 스트림

        Raises:
            OpenAIClientException: OpenAI API 호출 중 오류 발생 시
        """
        try:
            client = OpenAI(api_key=api_key)

            logger.debug(f"Chat Completions API 요청 시작 (model: {model}, stream: {stream})")

            response = client.responses.create(
                model=model,
                input=messages,
                temperature=temperature,
                max_output_tokens=max_tokens,
                stream=stream
            )

            if stream:
                logger.debug("스트리밍 응답 시작")
                return response
            else:
                logger.debug(f"Chat Completions API 응답 완료 (ID: {response.id})")
                return response

        except Exception as e:
            error_msg = f"Chat Completions API 호출 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            raise OpenAIClientException(
                message=error_msg,
                error_code="CHAT_COMPLETIONS_ERROR",
                details={"model": model, "stream": stream}
            ) 