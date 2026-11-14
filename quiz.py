class Quiz:
    """문제와 네 개의 선택지, 1부터 시작하는 정답 번호를 보관한다."""

    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지가 네 개여야 합니다.")
        if any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1~4 사이의 정수여야 합니다.")

        self.question = question
        self.choices = choices.copy()
        self.answer = answer

    def show(self):
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def is_correct(self, choice):
        return choice == self.answer

    def to_record(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_record(cls, record):
        if not isinstance(record, dict):
            raise ValueError("퀴즈 항목은 객체여야 합니다.")
        return cls(record["question"], record["choices"], record["answer"])
