import random
from pathlib import Path

from default_quizzes import make_default_quizzes
from quiz import Quiz
from storage import InvalidStateError, backup_path, read_state, write_state


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
        self.can_save = True

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
                print("저장되지 않은 변경사항을 저장합니다.")
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

        questions = self.quizzes.copy()
        random.shuffle(questions)
        correct = 0
        total = len(questions)
        print(f"\n퀴즈를 시작합니다. 총 {total}문제입니다.")
        for number, quiz in enumerate(questions, start=1):
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
            self.quizzes, self.best_score = read_state(self.state_path)
        except FileNotFoundError:
            self.load_backup()
        except InvalidStateError:
            print("state.json이 손상되었습니다.")
            self.load_backup()
        except OSError as error:
            self.disable_saving(self.state_path, error)

    def load_backup(self):
        path = backup_path(self.state_path)
        try:
            self.quizzes, self.best_score = read_state(path)
        except FileNotFoundError:
            print("기본 퀴즈로 시작합니다.")
        except InvalidStateError:
            print("백업도 손상되어 기본 퀴즈로 시작합니다.")
        except OSError as error:
            self.disable_saving(path, error)
            return
        else:
            print(f"{path.name}에서 퀴즈와 최고 점수를 복구했습니다.")
        self.needs_save = True

    def disable_saving(self, path, error):
        self.can_save = False
        print(f"{path.name}을 읽을 수 없어 이번 실행에서는 기본 퀴즈를 사용합니다. ({error})")

    def save_state(self):
        if not self.can_save:
            print("파일을 읽을 수 없어 저장을 건너뜁니다. 접근 권한을 확인하고 다시 실행하세요.")
            return False
        try:
            write_state(self.state_path, self.quizzes, self.best_score)
        except (OSError, UnicodeError) as error:
            print(f"state.json을 저장할 수 없습니다. ({error})")
            return False
        except KeyboardInterrupt:
            print("\n저장이 중단되었습니다.")
            return False

        self.needs_save = False
        return True
