import json
from shutil import copyfileobj
from pathlib import Path
from tempfile import NamedTemporaryFile

from quiz import Quiz


class InvalidStateError(ValueError):
    """읽을 수는 있지만 게임 상태로 사용할 수 없는 데이터."""


def state_record(quizzes, best_score):
    return {"quizzes": [quiz.to_record() for quiz in quizzes], "best_score": best_score}


def backup_path(path):
    return path.with_name(f"{path.name}.bak")


def read_state(path):
    try:
        with path.open(encoding="utf-8") as file:
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
            best_score = {"correct": correct, "total": total}
    except (ValueError, KeyError, RecursionError) as error:
        raise InvalidStateError from error
    return quizzes, best_score


def write_state(path, quizzes, best_score):
    state = state_record(quizzes, best_score)
    try:
        previous = state_record(*read_state(path))
    except FileNotFoundError:
        pass
    except InvalidStateError:
        archive = archive_corrupt_state(path)
        print(f"손상된 파일을 {archive.name}에 보존했습니다.")
    else:
        if previous == state:
            return
        write_json(backup_path(path), previous)
    write_json(path, state)


def archive_corrupt_state(path):
    archive = None
    try:
        with path.open("rb") as source, NamedTemporaryFile(
            dir=path.parent, prefix=f"{path.name}.corrupt-", delete=False
        ) as file:
            archive = Path(file.name)
            copyfileobj(source, file)
    except (OSError, KeyboardInterrupt):
        if archive is not None:
            archive.unlink(missing_ok=True)
        raise
    return archive


def write_json(path, state):
    temporary_path = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as file:
            temporary_path = Path(file.name)
            json.dump(state, file, ensure_ascii=False, indent=2)
            file.write("\n")
        # 쓰기를 마친 파일로 교체해 저장 도중 기존 JSON이 잘리는 일을 막는다.
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
