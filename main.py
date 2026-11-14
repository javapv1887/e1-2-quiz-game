from default_quizzes import make_default_quizzes
from quiz import Quiz


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


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("내용을 입력하세요.")


def show_menu():
    print("\n=== 파이썬 기초 퀴즈 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


def play_quizzes(quizzes):
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return None

    correct = 0
    total = len(quizzes)
    print(f"\n퀴즈를 시작합니다. 총 {total}문제입니다.")
    for number, quiz in enumerate(quizzes, start=1):
        print(f"\n[문제 {number}/{total}]")
        quiz.show()
        answer = read_number("정답 번호 (1~4): ", 1, 4)
        if quiz.is_correct(answer):
            correct += 1
            print("정답입니다!")
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

    print(f"\n결과: {total}문제 중 {correct}문제 정답")
    return correct, total


def add_quiz(quizzes):
    print("\n새 퀴즈를 등록합니다.")
    question = read_text("문제: ")
    choices = [read_text(f"선택지 {number}: ") for number in range(1, 5)]
    answer = read_number("정답 번호 (1~4): ", 1, 4)
    quizzes.append(Quiz(question, choices, answer))
    print("퀴즈가 추가되었습니다.")


def run_menu():
    quizzes = make_default_quizzes()
    while True:
        show_menu()
        choice = read_number("선택: ", 1, 5)
        if choice == 5:
            print("게임을 종료합니다.")
            return
        if choice == 1:
            play_quizzes(quizzes)
        elif choice == 2:
            add_quiz(quizzes)
        else:
            print("이 메뉴는 준비 중입니다.")


if __name__ == "__main__":
    try:
        run_menu()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 게임을 종료합니다.")
