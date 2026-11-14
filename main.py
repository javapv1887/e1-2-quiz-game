def read_number(prompt, minimum, maximum):
    while True:
        text = input(prompt).strip()
        if not text:
            print("번호를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print("정수를 입력하세요.")
            continue

        if minimum <= number <= maximum:
            return number
        print(f"{minimum}~{maximum} 사이의 번호를 입력하세요.")


def show_menu():
    print("\n=== 파이썬 기초 퀴즈 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


def run_menu():
    while True:
        show_menu()
        choice = read_number("선택: ", 1, 5)
        if choice == 5:
            print("게임을 종료합니다.")
            return
        print("이 메뉴는 준비 중입니다.")


if __name__ == "__main__":
    try:
        run_menu()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 게임을 종료합니다.")
