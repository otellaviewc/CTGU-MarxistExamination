import rx
from rx import operators as ops

from utils import load_json


def print_problem(problem: dict):
    print(f"[{problem['chapter']}.{problem['index']}]\t {problem['problem']}")

    checked = [problem['answer']] if problem['type'] == 0 else problem['answer']
    options = problem['options']
    for i in checked:
        print(f'{chr(ord("A") + i)}. {options[i]}')


if __name__ == '__main__':
    problems_path = 'temp/sorted_corrected_text_problems.json'

    rx.from_iterable(
        load_json(problems_path)
    ).pipe(
        ops.take(100)
    ).subscribe(print_problem)
