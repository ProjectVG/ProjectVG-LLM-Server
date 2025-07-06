#!/usr/bin/env python3
"""
통합 테스트 실행 스크립트
- 단위 테스트와 시나리오 테스트를 모두 실행
"""

import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.test_unit import run_unit_tests
from tests.test_scenarios import main as run_scenario_tests


def main():
    """모든 테스트 실행"""
    print("=" * 80)
    print("LLM Server 통합 테스트 시작")
    print("=" * 80)
    
    # 1. 단위 테스트 실행
    print("\n" + "=" * 60)
    print("1단계: 단위 테스트 실행")
    print("=" * 60)
    
    unit_success = run_unit_tests()
    
    # 2. 시나리오 테스트 실행
    print("\n" + "=" * 60)
    print("2단계: 시나리오 테스트 실행")
    print("=" * 60)
    
    try:
        run_scenario_tests()
        scenario_success = True
    except Exception as e:
        print(f"[ERROR] 시나리오 테스트 실행 중 오류: {e}")
        scenario_success = False
    
    # 3. 최종 결과 요약
    print("\n" + "=" * 80)
    print("통합 테스트 최종 결과")
    print("=" * 80)
    
    if unit_success and scenario_success:
        print("[SUCCESS] 모든 테스트 성공!")
        print("LLM Server가 정상적으로 작동합니다.")
    else:
        print("[FAILED] 일부 테스트 실패")
        if not unit_success:
            print("   - 단위 테스트 실패")
        if not scenario_success:
            print("   - 시나리오 테스트 실패")
        print("문제를 확인하고 수정해주세요.")
    
    print("=" * 80)


if __name__ == "__main__":
    main() 