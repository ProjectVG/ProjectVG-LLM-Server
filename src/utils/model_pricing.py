"""
OpenAI 모델 가격 정보 데이터베이스
성능 최적화를 위해 미리 계산된 토큰 단위 비용 포함
"""

# 원본 모델 가격 정보 (달러 단위, per 1M tokens)
MODEL_PRICES_USD = {
    # GPT-5 시리즈
    "gpt-5": {"input": 1.25, "cached_input": 0.125, "output": 10.00},
    "gpt-5-mini": {"input": 0.25, "cached_input": 0.025, "output": 2.00},
    "gpt-5-nano": {"input": 0.05, "cached_input": 0.005, "output": 0.40},
    "gpt-5-chat-latest": {"input": 1.25, "cached_input": 0.125, "output": 10.00},
    
    # GPT-4.1 시리즈
    "gpt-4.1": {"input": 2.00, "cached_input": 0.50, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "cached_input": 0.10, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "cached_input": 0.025, "output": 0.40},
    
    # GPT-4o 시리즈
    "gpt-4o": {"input": 2.50, "cached_input": 1.25, "output": 10.00},
    "gpt-4o-2024-05-13": {"input": 5.00, "output": 15.00},
    "gpt-4o-audio-preview": {"input": 2.50, "output": 10.00},
    "gpt-4o-realtime-preview": {"input": 5.00, "cached_input": 2.50, "output": 20.00},
    "gpt-4o-mini": {"input": 0.15, "cached_input": 0.075, "output": 0.60},
    "gpt-4o-mini-audio-preview": {"input": 0.15, "output": 0.60},
    "gpt-4o-mini-realtime-preview": {"input": 0.60, "cached_input": 0.30, "output": 2.40},
    
    # O 시리즈
    "o1": {"input": 15.00, "cached_input": 7.50, "output": 60.00},
    "o1-pro": {"input": 150.00, "output": 600.00},
    "o3-pro": {"input": 20.00, "output": 80.00},
    "o3": {"input": 2.00, "cached_input": 0.50, "output": 8.00},
    
    # 기존 모델들
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-4": {"input": 30.00, "output": 60.00},
}

# 기본 모델
DEFAULT_MODEL = "gpt-4o-mini"

# 성능 최적화를 위한 미리 계산된 토큰당 비용 (밀리센트 단위, 정수)
# 계산 공식: 달러 * 100,000 (밀리센트 변환) / 1,000,000 (토큰 단위)
def _calculate_millicent_per_token(usd_per_million_tokens: float) -> int:
    """달러/1M토큰을 밀리센트/토큰으로 변환"""
    return int(round(usd_per_million_tokens * 100_000 / 1_000_000))

# 모델별 토큰당 비용 (밀리센트 단위, 정수) - 런타임 최적화
MODEL_COSTS_PER_TOKEN = {}

for model, prices in MODEL_PRICES_USD.items():
    cached_input_price = prices.get("cached_input", prices["input"] * 0.1)
    
    MODEL_COSTS_PER_TOKEN[model] = {
        "input": _calculate_millicent_per_token(prices["input"]),
        "cached_input": _calculate_millicent_per_token(cached_input_price),
        "output": _calculate_millicent_per_token(prices["output"])
    }

# 빠른 조회를 위한 지원 모델 집합
SUPPORTED_MODELS = frozenset(MODEL_PRICES_USD.keys())

def get_model_costs(model: str) -> dict:
    """
    모델의 토큰당 비용을 반환 (밀리센트 단위, 정수)
    
    Args:
        model: 모델명
        
    Returns:
        dict: {"input": int, "cached_input": int, "output": int}
    """
    return MODEL_COSTS_PER_TOKEN.get(model, MODEL_COSTS_PER_TOKEN[DEFAULT_MODEL])

def is_supported_model(model: str) -> bool:
    """모델 지원 여부 확인 - O(1) 시간복잡도"""
    return model in SUPPORTED_MODELS

def get_supported_models() -> list[str]:
    """지원되는 모델 목록 반환"""
    return list(SUPPORTED_MODELS)