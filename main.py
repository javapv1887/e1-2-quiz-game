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

    points = correct * 100 // total
    print(f"\n결과: {total}문제 중 {correct}문제 정답 ({points}점)")
    return correct, total


def add_quiz(quizzes):
    print("\n새 퀴즈를 등록합니다.")
    question = read_text("문제: ")
    choices = [read_text(f"선택지 {number}: ") for number in range(1, 5)]
    answer = read_number("정답 번호 (1~4): ", 1, 4)
    quizzes.append(Quiz(question, choices, answer))
    print("퀴즈가 추가되었습니다.")


def show_quizzes(quizzes):
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    print(f"\n등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    for number, quiz in enumerate(quizzes, start=1):
        print(f"{number}. {quiz.question}")


def update_best_score(best_score, result):
    if result is None:
        return best_score

    correct, total = result
    # 두 정답률을 교차 곱으로 비교해 정수 표시 때의 반올림 오차를 피한다.
    if best_score is None or correct * best_score["total"] > best_score["correct"] * total:
        print("새 최고 점수입니다!")
        return {"correct": correct, "total": total}
    return best_score


def show_best_score(best_score):
    if best_score is None:
        print("아직 퀴즈를 마친 기록이 없습니다.")
        return

    correct = best_score["correct"]
    total = best_score["total"]
    points = correct * 100 // total
    print(f"최고 점수: {points}점 ({total}문제 중 {correct}문제 정답)")


def run_menu():
    quizzes = make_default_quizzes()
    best_score = None
    while True:
        show_menu()
        choice = read_number("선택: ", 1, 5)
        if choice == 5:
            print("게임을 종료합니다.")
            return
        if choice == 1:
            result = play_quizzes(quizzes)
            best_score = update_best_score(best_score, result)
        elif choice == 2:
            add_quiz(quizzes)
        elif choice == 3:
            show_quizzes(quizzes)
        elif choice == 4:
            show_best_score(best_score)


if __name__ == "__main__":
    try:
        run_menu()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 게임을 종료합니다.")
