from functools import partial

from pypinyin import pinyin, Style
import rx
from rx.operators import map, to_iterable

from utils import load_json, save_json, after


def pinyin_text(problem_text: str) -> str:
    return ''.join([''.join([c for c in py[0] if '0' <= c <= '9' or 'a' <= c <= 'z'])
                    for py in pinyin(problem_text, style=Style.TONE3, neutral_tone_with_five=True)])


def pinyin_problem(problem: dict):
    problem['problem_pinyin'] = pinyin_text(problem['problem'])


def sort_problems(problems: list):
    problems.sort(key=lambda problem: problem['problem_pinyin'])


if __name__ == '__main__':
    problems_path = 'temp/corrected_text_problems.json'
    sorted_path = 'temp/sorted_corrected_text_problems.json'

    rx.from_(
        load_json(problems_path)
    ).pipe(
        map(after(pinyin_problem)),
        to_iterable(),
        map(after(sort_problems))
    ).subscribe(
        partial(save_json, path=sorted_path)
    )
