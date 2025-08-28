"""
OpenAI 모델 비용 계산 유틸리티 (고성능 최적화 버전)
"""

from .model_pricing import get_model_costs, is_supported_model, get_supported_models, DEFAULT_MODEL


class LLMCostCalculator:
    """
    LLM 모델 비용 계산기 - 고성능 최적화 버전
    
    특징:
    - O(1) 시간복잡도
    - 정수 연산만 사용 (float 연산 제거)
    - 함수 호출 오버헤드 최소화
    - 미리 계산된 토큰당 비용 사용
    """
    
    @classmethod
    def calculate_cost(
        cls, 
        model: str, 
        input_tokens: int, 
        output_tokens: int,
        cached_tokens: int = 0,
        reasoning_tokens: int = 0
    ) -> int:
        """
        초고속 모델 사용 비용 계산
        
        Args:
            model: 모델명
            input_tokens: 입력 토큰 수
            output_tokens: 출력 토큰 수  
            cached_tokens: 캐시된 토큰 수
            reasoning_tokens: 추론 토큰 수 (현재 미사용, 향후 확장용)
            
        Returns:
            int: 총 비용 (밀리센트 단위, 정수)
        """
        # 모델 비용 정보를 한 번만 조회 (O(1))
        costs = get_model_costs(model)
        
        # 일반 입력 토큰 계산 (조건문으로 max() 함수 호출 제거)
        normal_input_tokens = input_tokens - cached_tokens if input_tokens > cached_tokens else 0
        
        # 총 비용 계산 (정수 곱셈/덧셈만 사용)
        total_cost = (
            normal_input_tokens * costs["input"] +
            cached_tokens * costs["cached_input"] +
            output_tokens * costs["output"]
        )
        
        return total_cost
    
    @classmethod
    def calculate_cost_with_ceiling(
        cls, 
        model: str, 
        input_tokens: int, 
        output_tokens: int,
        cached_tokens: int = 0,
        reasoning_tokens: int = 0
    ) -> int:
        """
        C# 코드와 동일한 Math.Ceiling 로직을 사용한 비용 계산
        (기존 코드와의 호환성을 위해 제공)
        
        Args:
            model: 모델명
            input_tokens: 입력 토큰 수
            output_tokens: 출력 토큰 수  
            cached_tokens: 캐시된 토큰 수
            reasoning_tokens: 추론 토큰 수 (현재 미사용)
            
        Returns:
            int: 총 비용 (밀리센트 단위, 정수)
        """
        import math
        
        costs = get_model_costs(model)
        normal_input_tokens = input_tokens - cached_tokens if input_tokens > cached_tokens else 0
        
        # 각 토큰 타입별로 개별 ceiling 적용 (C# 호환)
        normal_input_cost = math.ceil(normal_input_tokens * costs["input"])
        cached_input_cost = math.ceil(cached_tokens * costs["cached_input"])
        output_cost = math.ceil(output_tokens * costs["output"])
        
        return normal_input_cost + cached_input_cost + output_cost
    
    @classmethod
    def is_supported_model(cls, model: str) -> bool:
        """모델 지원 여부 확인 - O(1) 시간복잡도"""
        return is_supported_model(model)
    
    @classmethod
    def get_supported_models(cls) -> list[str]:
        """지원되는 모델 목록 반환"""
        return get_supported_models()
    
    @classmethod
    def get_model_info(cls, model: str) -> dict:
        """
        모델의 토큰당 비용 정보 반환 (디버깅용)
        
        Args:
            model: 모델명
            
        Returns:
            dict: {"input": int, "cached_input": int, "output": int} (밀리센트 단위)
        """
        return get_model_costs(model)


# 최고 성능을 위한 함수형 인터페이스 (클래스 호출 오버헤드 제거)
def calculate_cost_fast(
    model: str, 
    input_tokens: int, 
    output_tokens: int, 
    cached_tokens: int = 0
) -> int:
    """
    최고 성능 비용 계산 함수
    
    클래스 메서드 호출 오버헤드를 제거한 직접 계산
    가장 자주 사용되는 케이스를 위한 최적화된 인터페이스
    
    Args:
        model: 모델명
        input_tokens: 입력 토큰 수
        output_tokens: 출력 토큰 수
        cached_tokens: 캐시된 토큰 수
        
    Returns:
        int: 총 비용 (밀리센트 단위)
    """
    costs = get_model_costs(model)
    normal_input_tokens = input_tokens - cached_tokens if input_tokens > cached_tokens else 0
    
    return (
        normal_input_tokens * costs["input"] +
        cached_tokens * costs["cached_input"] +
        output_tokens * costs["output"]
    )