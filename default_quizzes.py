from quiz import Quiz


def make_default_quizzes():
    return [
        Quiz(
            "len([10, 20, 30])의 결과는?",
            ["2", "3", "10", "30"],
            2,
        ),
        Quiz(
            "키와 값의 쌍으로 데이터를 저장하는 자료형은?",
            ["list", "bool", "dict", "str"],
            3,
        ),
        Quiz(
            "list(range(3))의 결과는?",
            ["[0, 1, 2]", "[1, 2, 3]", "[0, 1, 2, 3]", "[3]"],
            1,
        ),
        Quiz(
            "int('abc')를 실행하면 발생하는 예외는?",
            ["TypeError", "IndexError", "KeyError", "ValueError"],
            4,
        ),
        Quiz(
            "인스턴스 메서드의 첫 매개변수 self가 가리키는 것은?",
            ["모듈", "메서드를 호출한 인스턴스", "메서드의 반환값", "부모 클래스"],
            2,
        ),
    ]
