#!/usr/bin/env python3
"""
테스트 실행 스크립트
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tests.test_simple_request import run_simple_request_tests


def main():
    """메인 테스트 실행 함수"""
    print("LLM Server 테스트 스위트")
    print("=" * 50)
    
    print("\n단순 요청 테스트")
    print("-" * 30)
    success = run_simple_request_tests()
    
    print("\n" + "=" * 50)
    if success:
        print("모든 테스트가 성공했습니다!")
        return 0
    else:
        print("일부 테스트가 실패했습니다.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 