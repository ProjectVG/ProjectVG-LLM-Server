"""
시나리오 테스트
- 대화 지속 테스트
- 메모리 테스트  
- 시스템 메시지 테스트
- Instructions 테스트
- 다중 대화 시나리오 테스트
- 지시사항 준수 시나리오 테스트
- 성능 시나리오 테스트
"""

import unittest
import time
from src.core.openai_client import OpenAIChatClient
from src.config import config
from tests.test_input import get_test_max_tokens, get_performance_test_max_tokens


class TestScenarios(unittest.TestCase):
    """시나리오 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        api_key = config.get("OPENAI_API_KEY")
        if not api_key:
            self.skipTest("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        self.client = OpenAIChatClient()
        self.conversation_history = []
    
    def test_conversation_continuity(self):
        """대화 지속 테스트 - 첫 번째 대화에서 지시사항을 주고 두 번째 대화에서 확인"""
        print("\n1. 대화 지속 테스트")
        print("-" * 40)
        
        history = []
        
        first_prompt = "다음 숫자를 기억하고 있어라. 68"
        print(f"첫 번째 프롬프트: {first_prompt}")
        
        response, response_time = self.client.chat(
            user_prompt=first_prompt,
            memory=[],
            system_prompt="",
            instructions="",
            history=history,
            max_tokens=get_test_max_tokens()
        )
        
        response_text = response.output_text
        print(f"첫 번째 응답: {response_text}")
        print(f"응답 시간: {response_time:.2f}초")
        
        # history에 첫 번째 대화 추가 (sample.py처럼)
        history.append(f"user:{first_prompt}")
        history.append(f"assistant:{response_text}")
        
        # 두 번째 대화: 지시사항 확인
        second_prompt = "지금 방금 기억한 숫자는?"
        print(f"\n두 번째 프롬프트: {second_prompt}")
        
        response2, response_time2 = self.client.chat(
            user_prompt=second_prompt,
            memory=[],
            system_prompt="",
            instructions="",
            history=history,
            max_tokens=get_test_max_tokens()  # 테스트용 토큰 제한
        )
        
        response2_text = response2.output_text
        print(f"두 번째 응답: {response2_text}")
        print(f"응답 시간: {response_time2:.2f}초")
        
        # 결과 검증
        self.assertIn("68", response2_text, "AI가 이전 지시사항을 기억하지 못함")
        print("[SUCCESS] 대화 지속 테스트 성공: AI가 이전 지시사항을 기억하고 68으로 응답")
    
    def test_memory_functionality(self):
        """메모리 기능 테스트 - 메모리에 정보를 넣고 질문으로 확인"""
        print("\n2. 메모리 테스트")
        print("-" * 40)
        
        # 메모리에 정보 추가
        memory = ["유저가 좋아하는 꽃은 백합이다."]
        prompt = "내가 좋아하는 꽃은?"
        
        print(f"메모리: {memory}")
        print(f"프롬프트: {prompt}")
        
        response, response_time = self.client.chat(
            user_prompt=prompt,
            memory=memory,
            system_prompt="",
            instructions="",
            max_tokens=get_test_max_tokens() 
        )
        
        response_text = response.output_text
        print(f"응답: {response_text}")
        print(f"응답 시간: {response_time:.2f}초")
        
        # 결과 검증
        self.assertIn("백합", response_text, "AI가 메모리 정보를 활용하지 못함")
        print("[SUCCESS] 메모리 테스트 성공: AI가 메모리에서 백합 정보를 찾아 응답")
    
    def test_system_message(self):
        """시스템 메시지 테스트 - 시스템 메시지로 응답 형식 강제"""
        print("\n3. 시스템 메시지 테스트")
        print("-" * 40)
        
        system_message = "말끝 뒤에 항상 냥을 붙여라"
        prompt = "안녕하세요"
        
        print(f"시스템 메시지: {system_message}")
        print(f"프롬프트: {prompt}")
        
        response, response_time = self.client.chat(
            user_prompt=prompt,
            memory=[],
            system_prompt="",
            instructions=system_message,
            max_tokens=get_test_max_tokens() 
        )
        
        response_text = response.output_text
        print(f"응답: {response_text}")
        print(f"응답 시간: {response_time:.2f}초")
        
        # 결과 검증
        self.assertIn("냥", response_text, "AI가 시스템 메시지를 따르지 않음")
        print("[SUCCESS] 시스템 메시지 테스트 성공: AI가 '냥'을 포함하여 응답")
    
    def test_instructions_format(self):
        """Instructions 테스트 - 응답 형식 강제"""
        print("\n4. Instructions 테스트")
        print("-" * 40)
        
        instructions = "응답 메시지는 항상 'assistance: (메시지)' 형태로 주어져야한다."
        prompt = "파이썬이 뭐야?"
        
        print(f"Instructions: {instructions}")
        print(f"프롬프트: {prompt}")
        
        response, response_time = self.client.chat(
            user_prompt=prompt,
            memory=[],
            system_prompt="",
            instructions=instructions,
            max_tokens=get_test_max_tokens()  # 테스트용 토큰 제한
        )
        
        response_text = response.output_text
        print(f"응답: {response_text}")
        print(f"응답 시간: {response_time:.2f}초")
        
        # 결과 검증
        self.assertTrue(
            response_text.strip().lower().startswith("assistance:"),
            "AI가 지정된 형식을 따르지 않음"
        )
        print("[SUCCESS] Instructions 테스트 성공: AI가 지정된 형식으로 응답")
    
    def test_multiple_conversation_scenario(self):
        """다중 대화 시나리오 테스트 - 여러 대화를 연속으로 진행"""
        print("\n5. 다중 대화 시나리오 테스트")
        print("-" * 40)
        
        from tests.test_input import get_test_inputs, get_test_memory, get_test_max_tokens, get_performance_test_max_tokens
        
        test_inputs = get_test_inputs()
        memory = get_test_memory()
        
        print(f"테스트 입력 개수: {len(test_inputs[:3])}")
        print(f"메모리: {memory}")
        
        for i, user_input in enumerate(test_inputs[:3]):
            print(f"\n--- 대화 {i+1} ---")
            print(f"사용자: {user_input}")
            
            response, response_time = self.client.chat(
                user_prompt=user_input,
                memory=memory,
                system_prompt="",
                instructions="",
                max_tokens=get_test_max_tokens()
            )
            
            response_text = response.output_text
            print(f"AI: {response_text}")
            print(f"응답 시간: {response_time:.2f}초")
            
            # 기본 검증
            self.assertGreater(len(response_text), 0, f"대화 {i+1}에서 빈 응답")
            print(f"[SUCCESS] 대화 {i+1} 성공")
    
    def test_instruction_following_scenario(self):
        """지시사항 준수 시나리오 테스트 - 다양한 지시사항에 따른 응답"""
        print("\n6. 지시사항 준수 시나리오 테스트")
        print("-" * 40)
        
        from tests.test_input import get_instructions, get_test_memory, get_test_max_tokens
        
        instructions_list = get_instructions()
        memory = get_test_memory()
        prompt = "파이썬에 대해 설명해줘"
        
        print(f"테스트할 지시사항 개수: {len(instructions_list)}")
        print(f"프롬프트: {prompt}")
        
        for i, instruction in enumerate(instructions_list):
            print(f"\n--- 지시사항 {i+1} ---")
            print(f"지시사항: {instruction}")
            
            response, response_time = self.client.chat(
                user_prompt=prompt,
                memory=memory,
                system_prompt="",
                instructions=instruction,
                max_tokens=get_test_max_tokens()  # 테스트용 토큰 제한
            )
            
            response_text = response.output_text
            print(f"응답: {response_text[:100]}...")
            print(f"응답 시간: {response_time:.2f}초")
            
            # 기본 검증
            self.assertGreater(len(response_text), 0, f"지시사항 {i+1}에서 빈 응답")
            print(f"[SUCCESS] 지시사항 {i+1} 성공")
    
    def test_performance_scenario(self):
        """성능 시나리오 테스트 - 긴 입력에 대한 응답 성능"""
        print("\n7. 성능 시나리오 테스트")
        print("-" * 40)
        
        from tests.test_input import get_performance_inputs, get_test_memory, get_performance_test_max_tokens
        
        performance_inputs = get_performance_inputs()
        memory = get_test_memory()
        
        print(f"성능 테스트 입력 개수: {len(performance_inputs)}")
        
        total_time = 0
        success_count = 0
        
        for i, user_input in enumerate(performance_inputs):
            print(f"\n--- 성능 테스트 {i+1} ---")
            print(f"입력: {user_input[:50]}...")
            
            response, response_time = self.client.chat(
                user_prompt=user_input,
                memory=memory,
                system_prompt="",
                instructions="",
                max_tokens=get_performance_test_max_tokens()  # 성능 테스트는 조금 더 많은 토큰 허용
            )
            
            response_text = response.output_text
            total_time += response_time
            
            print(f"응답 길이: {len(response_text)} 문자")
            print(f"응답 시간: {response_time:.2f}초")
            
            # 성능 기준 검증 (30초 이내)
            self.assertLess(response_time, 30, f"성능 테스트 {i+1}에서 응답 시간 초과")
            self.assertGreater(len(response_text), 0, f"성능 테스트 {i+1}에서 빈 응답")
            
            print(f"[SUCCESS] 성능 테스트 {i+1} 성공")
            success_count += 1
        
        avg_time = total_time / len(performance_inputs)
        print(f"\n--- 성능 요약 ---")
        print(f"평균 응답 시간: {avg_time:.2f}초")
        print(f"성공률: {success_count}/{len(performance_inputs)} ({success_count/len(performance_inputs)*100:.1f}%)")
        
        self.assertEqual(success_count, len(performance_inputs), "일부 성능 테스트 실패")
        print("[SUCCESS] 전체 성능 시나리오 테스트 성공")

    def test_role_functionality(self):
        """역할 설정 기능 테스트 - 다양한 역할에 따른 응답 스타일 확인"""
        print("\n8. 역할 설정 테스트")
        print("-" * 40)
        
        from tests.test_input import get_role_variants, get_test_max_tokens
        
        role_variants = get_role_variants()
        prompt = "파이썬에 대해 설명해줘"
        
        print(f"테스트할 역할 개수: {len(role_variants)}")
        print(f"프롬프트: {prompt}")
        
        for i, role in enumerate(role_variants):
            print(f"\n--- 역할 {i+1} ---")
            print(f"역할: {role[:50]}...")
            
            response, response_time = self.client.chat(
                user_prompt=prompt,
                memory=[],
                system_prompt="",
                role=role,
                instructions="",
                max_tokens=get_test_max_tokens()
            )
            
            response_text = response.output_text
            print(f"응답: {response_text[:100]}...")
            print(f"응답 시간: {response_time:.2f}초")
            
            # 기본 검증
            self.assertGreater(len(response_text), 0, f"역할 {i+1}에서 빈 응답")
            print(f"[SUCCESS] 역할 {i+1} 성공")
    
    def test_role_with_memory(self):
        """역할과 메모리 조합 테스트 - 역할과 메모리가 함께 작동하는지 확인"""
        print("\n9. 역할과 메모리 조합 테스트")
        print("-" * 40)
        
        role = "당신은 친근한 AI 어시스턴트입니다. 반말을 사용합니다. 사용자의 취향을 기억하고 그에 맞는 답변을 제공합니다."
        memory = ["사용자는 파이썬을 좋아합니다", "사용자는 간단한 설명을 선호합니다"]
        prompt = "프로그래밍 언어에 대해 설명해줘"
        
        print(f"역할: {role[:50]}...")
        print(f"메모리: {memory}")
        print(f"프롬프트: {prompt}")
        
        response, response_time = self.client.chat(
            user_prompt=prompt,
            memory=memory,
            system_prompt="",
            role=role,
            instructions="",
            max_tokens=get_test_max_tokens()
        )
        
        response_text = response.output_text
        print(f"응답: {response_text[:150]}...")
        print(f"응답 시간: {response_time:.2f}초")
        
        # 결과 검증 - 파이썬이 언급되었는지 확인
        self.assertIn("파이썬", response_text.lower(), "AI가 메모리 정보를 활용하지 못함")
        print("[SUCCESS] 역할과 메모리 조합 테스트 성공: AI가 역할과 메모리를 모두 활용하여 응답")


def run_scenario_tests():
    """시나리오 테스트 실행"""
    print("=" * 60)
    print("시나리오 테스트 시작")
    print("=" * 60)
    
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestScenarios)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("=" * 60)
    print("시나리오 테스트 결과:")
    print(f"실행된 테스트: {result.testsRun}")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"실패: {len(result.failures)}")
    print(f"오류: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()


def main():
    """메인 테스트 실행 함수"""
    print("시나리오 테스트 시작...")
    
    # 환경 설정 확인
    if not config.get("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY가 설정되지 않았습니다.")
        print("env.example 파일을 참고하여 .env 파일을 생성하세요.")
        return
    
    # 테스트 실행
    run_scenario_tests()


if __name__ == "__main__":
    main() 