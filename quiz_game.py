import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from default_quizzes import make_default_quizzes
from quiz import Quiz


STATE_PATH = Path(__file__).resolve().parent / "state.json"


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


class QuizGame:
    """콘솔 메뉴와 게임 상태를 관리한다."""

    def __init__(self, state_path=STATE_PATH):
        self.state_path = state_path
        self.quizzes = make_default_quizzes()
        self.best_score = None
        self.needs_save = False

    def run(self):
        try:
            self.load_state()
            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 5)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_best_score()
                else:
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다.")
        finally:
            if self.needs_save:
                self.save_state()
        print("게임을 종료합니다.")

    def show_menu(self):
        print("\n=== 파이썬 기초 퀴즈 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct = 0
        total = len(self.quizzes)
        print(f"\n퀴즈를 시작합니다. 총 {total}문제입니다.")
        for number, quiz in enumerate(self.quizzes, start=1):
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
        self.update_best_score(correct, total)

    def add_quiz(self):
        print("\n새 퀴즈를 등록합니다.")
        question = read_text("문제: ")
        choices = [read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = read_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.needs_save = True
        if self.save_state():
            print("퀴즈가 추가되었습니다.")
        else:
            print("이번 실행에서 새 퀴즈를 사용할 수 있습니다.")

    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def update_best_score(self, correct, total):
        best = self.best_score
        # 문제 수가 달라도 정답률을 정확히 비교한다.
        if best is None or correct * best["total"] > best["correct"] * total:
            self.best_score = {"correct": correct, "total": total}
            self.needs_save = True
            print("새 최고 점수입니다!")
            self.save_state()

    def show_best_score(self):
        best_score = self.best_score
        if best_score is None:
            print("아직 퀴즈를 마친 기록이 없습니다.")
            return

        correct = best_score["correct"]
        total = best_score["total"]
        points = correct * 100 // total
        print(f"최고 점수: {points}점 ({total}문제 중 {correct}문제 정답)")

    def load_state(self):
        try:
            with self.state_path.open(encoding="utf-8") as file:
                state = json.load(file)
            if not isinstance(state, dict) or not isinstance(state.get("quizzes"), list):
                raise ValueError("퀴즈 목록을 읽을 수 없습니다.")

            quizzes = [Quiz.from_record(item) for item in state["quizzes"]]
            best_score = state["best_score"]
            if best_score is not None:
                if not isinstance(best_score, dict):
                    raise ValueError("최고 점수 형식이 올바르지 않습니다.")
                correct, total = best_score["correct"], best_score["total"]
                if (
                    type(correct) is not int
                    or type(total) is not int
                    or not 0 <= correct <= total
                    or total == 0
                ):
                    raise ValueError("최고 점수의 문제 수가 올바르지 않습니다.")
        except FileNotFoundError:
            self.needs_save = True
            return
        except (ValueError, KeyError, RecursionError):
            print("state.json이 손상되어 기본 퀴즈로 복구합니다.")
            self.needs_save = True
            return
        except OSError as error:
            print(f"state.json을 읽을 수 없어 기본 퀴즈를 사용합니다. ({error.strerror})")
            return

        self.quizzes = quizzes
        self.best_score = best_score

    def save_state(self):
        state = {
            "quizzes": [quiz.to_record() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        temporary_path = None
        try:
            try:
                with NamedTemporaryFile(
                    mode="w", encoding="utf-8", dir=self.state_path.parent, delete=False
                ) as file:
                    temporary_path = Path(file.name)
                    json.dump(state, file, ensure_ascii=False, indent=2)
                    file.write("\n")
                # 쓰기를 마친 파일로 교체해 저장 도중 기존 JSON이 잘리는 일을 막는다.
                temporary_path.replace(self.state_path)
            finally:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)
        except (OSError, UnicodeError) as error:
            print(f"state.json을 저장할 수 없습니다. ({error})")
            return False
        except KeyboardInterrupt:
            print("\n저장이 중단되었습니다.")
            return False

        self.needs_save = False
        return True
