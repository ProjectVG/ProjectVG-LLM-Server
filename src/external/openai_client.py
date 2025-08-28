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

    def create_response(
        self,
        input_data: Union[str, List[Dict]],
        api_key: str,
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        max_output_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        stream: bool = False,
        tools: Optional[List[Dict]] = None,
        background: bool = False,
        conversation: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        include: Optional[List[str]] = None,
        **kwargs
    ) -> Union[Response, Iterator[Response], str]:
        """
        새로운 Responses API를 사용한 응답 생성
        
        Args:
            input_data: 텍스트 문자열 또는 메시지 배열
            api_key: 사용할 API Key (필수)
            model: 사용할 모델
            instructions: 시스템 지시사항
            max_output_tokens: 최대 출력 토큰 수
            temperature: 온도 설정
            stream: 스트리밍 응답 여부
            tools: 사용 가능한 도구 배열
            background: 백그라운드 처리 여부
            conversation: 대화 ID (자동 대화 관리)
            metadata: 메타데이터 (최대 16개)
            include: 추가 데이터 포함 옵션
            **kwargs: 기타 고급 파라미터
            
        Returns:
            Response | Iterator[Response] | str: 응답 객체, 스트림, 또는 백그라운드 작업 ID
            
        Raises:
            OpenAIClientException: OpenAI API 호출 중 오류 발생 시
        """
        try:
            # API Key로 클라이언트 생성
            client = OpenAI(api_key=api_key)
            
            # 요청 파라미터 구성
            request_params = {
                "model": model,
                "input": input_data,
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
                "stream": stream
            }
            
            # 선택적 파라미터 추가
            if instructions:
                request_params["instructions"] = instructions
            if tools:
                request_params["tools"] = tools
            if background:
                request_params["background"] = background
            if conversation:
                request_params["conversation"] = conversation
            if metadata:
                request_params["metadata"] = metadata
            if include:
                request_params["include"] = include
                
            # 추가 파라미터 병합
            request_params.update(kwargs)
            
            logger.debug(f"Responses API 요청 시작 (model: {model}, stream: {stream}, background: {background})")
            
            response = client.responses.create(**request_params)
            
            if background:
                # 백그라운드 처리의 경우 작업 ID 반환
                logger.info(f"백그라운드 작업 시작: {response.id}")
                return response.id
            elif stream:
                # 스트리밍 응답의 경우 이터레이터 반환
                logger.debug("스트리밍 응답 시작")
                return response
            else:
                # 일반 응답의 경우 응답 객체 반환
                logger.debug(f"Responses API 응답 완료 (ID: {response.id})")
                return response
            
        except Exception as e:
            error_msg = f"Responses API 호출 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            raise OpenAIClientException(
                message=error_msg,
                error_code="RESPONSES_API_ERROR",
                details={"model": model, "stream": stream, "background": background}
            )

    def get_response_status(self, response_id: str, api_key: str) -> Response:
        """
        백그라운드 응답 상태 조회
        
        Args:
            response_id: 조회할 응답 ID
            api_key: 사용할 API Key (필수)
            
        Returns:
            Response: 응답 상태 객체
        """
        try:
            client = OpenAI(api_key=api_key)
            logger.debug(f"응답 상태 조회: {response_id}")
            return client.responses.retrieve(response_id)
        except Exception as e:
            error_msg = f"응답 상태 조회 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            raise OpenAIClientException(
                message=error_msg,
                error_code="RESPONSE_STATUS_ERROR",
                details={"response_id": response_id}
            )

    def cancel_response(self, response_id: str, api_key: str) -> bool:
        """
        백그라운드 응답 취소
        
        Args:
            response_id: 취소할 응답 ID
            api_key: 사용할 API Key (필수)
            
        Returns:
            bool: 취소 성공 여부
        """
        try:
            client = OpenAI(api_key=api_key)
            logger.info(f"응답 취소 요청: {response_id}")
            client.responses.cancel(response_id)
            return True
        except Exception as e:
            error_msg = f"응답 취소 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            raise OpenAIClientException(
                message=error_msg,
                error_code="RESPONSE_CANCEL_ERROR",
                details={"response_id": response_id}
            )

    def create_streaming_response(
        self,
        input_data: Union[str, List[Dict]],
        api_key: str,
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        max_output_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        **kwargs
    ) -> Iterator[str]:
        """
        스트리밍 응답 생성 (편의 메서드)
        
        Args:
            input_data: 텍스트 문자열 또는 메시지 배열
            api_key: 사용할 API Key (필수)
            model: 사용할 모델
            instructions: 시스템 지시사항
            max_output_tokens: 최대 출력 토큰 수
            temperature: 온도 설정
            **kwargs: 기타 파라미터
            
        Yields:
            str: 스트리밍 텍스트 청크
        """
        stream = self.create_response(
            input_data=input_data,
            api_key=api_key,
            model=model,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            stream=True,
            **kwargs
        )
        
        for chunk in stream:
            if hasattr(chunk, 'output') and chunk.output:
                for output in chunk.output:
                    if hasattr(output, 'content') and output.content:
                        yield output.content

    def create_web_search_response(
        self,
        query: str,
        api_key: str,
        model: str = DEFAULT_MODEL,
        instructions: str = "",
        include_sources: bool = True,
        **kwargs
    ) -> Response:
        """
        웹 검색을 활용한 응답 생성
        
        Args:
            query: 검색할 질의
            api_key: 사용할 API Key (필수)
            model: 사용할 모델
            instructions: 시스템 지시사항
            include_sources: 검색 소스 포함 여부
            **kwargs: 기타 파라미터
            
        Returns:
            Response: 웹 검색 결과를 포함한 응답
        """
        tools = [{"type": "web_search"}]
        include = ["web_search_call.action.sources"] if include_sources else None
        
        return self.create_response(
            input_data=query,
            api_key=api_key,
            model=model,
            instructions=instructions,
            tools=tools,
            include=include,
            **kwargs
        ) 