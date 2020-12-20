from functools import partial
from typing import List

import rx
from rx.operators import map, flat_map, to_iterable, zip
from bs4 import BeautifulSoup

from utils import load_json, format_json, save_json, do, component


def process_answer_item(answer_item) -> str:
    ans_content: str = answer_item.p.contents[-1]
    return ans_content[ans_content.rindex(' ') + 1:]


def process_answer_html(answer_html_path: str) -> List[str]:
    with open(answer_html_path, 'r', encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    answer_items = soup('div', 'answer')

    return [process_answer_item(answer_item) for answer_item in answer_items]


def join_answer_into_problem(problem: dict, answer: List[int]):
    if problem['type'] == 0 and len(answer) == 1:
        problem['answer'] = answer[0]
    elif problem['type'] == 1:
        problem['answer'] = answer
    else:
        problem['answer'] = answer

        print('无法匹配的题目答案数据:')
        print(format_json(problem))
        print('答案:')
        print(answer)


if __name__ == '__main__':
    # 测试处理前 5 章的题目数据

    file_cnt = 6  # 文件数量，目前包括绪论和后五章总共 6 个
    problems_path = './outputs/problems_image_link.json'
    answered_path = './outputs/problems_answered.json'

    answers = rx.from_(
        range(file_cnt)
    ).pipe(
        map(lambda i: f'./resources/a{i}.html'),
        flat_map(lambda path: rx.from_(process_answer_html(path))),
        map(lambda s: [ord(ch) - ord('A') for ch in s])
    )

    problems = rx.from_(load_json(problems_path))

    problems.pipe(
        zip(answers),
        do(lambda pair: join_answer_into_problem(*pair)),
        component(0),
        to_iterable()
    ).subscribe(
        partial(save_json, path=answered_path)
    )
