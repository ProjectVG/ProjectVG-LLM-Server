"""
테스트용 입력값 관리 모듈
"""

# 기본 테스트 메모리
DEFAULT_MEMORY = [
    "유저는 파이썬이랑 C#을 사용",
    "나랑 어제 데이트함"
]

# 기본 테스트 입력값들
DEFAULT_INPUTS = [
    "안녕하세요",
    "파이썬에 대해 알려줘",
    "오늘 날씨 어때?",
    "C#과 파이썬의 차이점은?",
    "고마워"
]

# 지시사항 테스트용
DEFAULT_INSTRUCTIONS = [
    "간단하고 명확하게 설명해주세요.",
    "한 문장으로 답해주세요.",
    "친근한 말투로 답해주세요.",
    "기술적인 용어를 사용해서 설명해주세요."
]

# 성능 테스트용 긴 입력
PERFORMANCE_INPUTS = [
    "파이썬의 장점과 단점을 자세히 설명해주세요.",
    "머신러닝과 딥러닝의 차이점을 설명해주세요.",
    "웹 개발에서 프론트엔드와 백엔드의 역할을 설명해주세요."
]


def get_test_memory():
    """테스트용 메모리 반환"""
    return DEFAULT_MEMORY.copy()


def get_test_inputs():
    """테스트용 입력값들 반환"""
    return DEFAULT_INPUTS.copy()


def get_instructions():
    """지시사항들 반환"""
    return DEFAULT_INSTRUCTIONS.copy()


def get_performance_inputs():
    """성능 테스트용 입력값들 반환"""
    return PERFORMANCE_INPUTS.copy()


def get_custom_inputs():
    """사용자 정의 입력값들 (환경변수에서 읽기)"""
    import os
    custom_inputs = os.getenv("TEST_INPUTS")
    if custom_inputs:
        return custom_inputs.split("|")
    return DEFAULT_INPUTS.copy()


def get_custom_memory():
    """사용자 정의 메모리 (환경변수에서 읽기)"""
    import os
    custom_memory = os.getenv("TEST_MEMORY")
    if custom_memory:
        return custom_memory.split("|")
    return DEFAULT_MEMORY.copy() 