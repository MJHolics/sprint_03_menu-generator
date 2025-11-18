"""
메뉴 추천 시스템 메인 실행 파일
"""

import sys
from src.intent_parser import IntentParser
from src.recommendation import MenuRecommender
from src.data_loader import DataLoader
from src.utils import format_recommendation_result


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🍽️  AI 메뉴 추천 시스템")
    print("=" * 60)

    # 1. 데이터 소스 선택
    print("\n데이터 소스를 선택하세요:")
    print("1. JSON 파일 (테스트용)")
    print("2. MySQL 데이터베이스")

    choice = input("\n선택 (1 또는 2): ").strip()

    if choice == '1':
        source = 'json'
        print("\n✅ JSON 파일에서 데이터를 로드합니다.")
    elif choice == '2':
        source = 'mysql'
        print("\n✅ MySQL 데이터베이스에서 데이터를 로드합니다.")
    else:
        print("\n❌ 잘못된 선택입니다. 프로그램을 종료합니다.")
        sys.exit(1)

    # 2. 데이터 로드
    try:
        loader = DataLoader(source=source)
        data = loader.load()
        print(f"✅ 데이터 로드 완료: 메뉴 {len(data['menu_items'])}개")
    except Exception as e:
        print(f"\n❌ 데이터 로드 실패: {e}")
        sys.exit(1)

    # 3. 메뉴 추천 루프
    parser = IntentParser()
    recommender = MenuRecommender()

    print("\n" + "=" * 60)
    print("무엇을 찾고 계신가요? (종료하려면 'exit' 입력)")
    print("=" * 60)

    while True:
        print("\n💬 고객 요청 예시:")
        print("   - 칼로리 낮은 음료 추천해줘")
        print("   - 고단백 메인 메뉴 찾아줘")
        print("   - 카페인 없는 디저트 뭐있어?")
        print("   - 다이어트 중인데 뭐 먹을까")

        customer_text = input("\n👤 당신: ").strip()

        if customer_text.lower() in ['exit', '종료', 'quit', 'q']:
            print("\n👋 이용해주셔서 감사합니다!")
            break

        if not customer_text:
            print("\n⚠️  요청을 입력해주세요.")
            continue

        try:
            # 4. 의도 파싱
            print("\n🤖 AI가 요청을 분석 중...")
            parsed_intent = parser.parse_customer_request(customer_text)
            print(f"✅ 분석 완료: {parsed_intent.get('explanation', '')}")

            # 5. 메뉴 추천
            print("\n🔍 메뉴 검색 중...")
            result = recommender.recommend(
                data['menu_items'],
                data['nutrition_estimates'],
                parsed_intent
            )

            # 6. 결과 출력
            if result['total_found'] == 0:
                print("\n❌ 조건에 맞는 메뉴를 찾을 수 없습니다.")
            else:
                print(f"\n✅ {result['total_found']}개의 메뉴를 찾았습니다.")
                print(format_recommendation_result(result['recommendations']))

        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            print("다시 시도해주세요.")

    # 7. 종료
    loader.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 프로그램이 종료되었습니다.")
        sys.exit(0)
