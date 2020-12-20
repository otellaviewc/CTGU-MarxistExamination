from functools import partial
from typing import List

import rx
from rx.operators import map, flat_map, to_iterable
from bs4 import BeautifulSoup

from utils import save_json, do

'''
题目信息样例：
{
    "id": 17320783,
    "type": 0, // 0 代表单选，1 代表多选
    "problem": "https://qn-st0.yuketang.cn/Fvpd-q4sULimGV6A6EzDW6Cqa-fK",
    "answer": 0,
    "chapter": 0,
    "index": 1,
    "options": [
        "https://qn-st0.yuketang.cn/Fhui9pAJGBRYzPNye4GrJuSHuY4_",
        "https://qn-st0.yuketang.cn/FvYJabIl-G_C4F_c2n1u-QYtiuKS",
        "https://qn-st0.yuketang.cn/FsEWoZwjKobDMBYMnN8V7_T93Snf",
        "https://qn-st0.yuketang.cn/Fje5dOyTawtJrtyo7BYcNHYmJyYg"
    ]
}
'''


def process_problem_item(problem_item) -> dict or None:
    pid = problem_item['data-problemid']
    if pid == '':  # 部分 item 是分割试卷的空白页面
        return

    problem_type = 0 if problem_item['class'][-1] == "MultipleChoice" else 1
    problem_index = 1 + int(problem_item['data-index'])
    problem_images = [v['data-background'] for v in problem_item(lambda tag: tag.has_attr('data-background'))]

    return {
        'id': int(pid),
        'type': problem_type,
        'answer': 0 if problem_type == 0 else [0],
        'problem': problem_images[0],
        'index': problem_index,
        'options': problem_images[1:]
    }


def process_problem_html(problem_html_path: str, chapter: int) -> List[dict]:
    with open(problem_html_path, 'r', encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    problem_items = soup('div', 'problem_item')

    problem_ls: List[dict] = []

    for problem_item in problem_items:
        problem = process_problem_item(problem_item)
        if problem is None:
            continue

        problem['chapter'] = chapter
        problem_ls.append(problem)

    return problem_ls


if __name__ == '__main__':
    # 测试处理前 5 章的题目数据

    file_cnt = 6  # 文件数量，目前包括绪论和后五章总共 6 个
    save_path = 'outputs/2020/problems_image_link.json'

    rx.from_(
        range(file_cnt)
    ).pipe(
        map(lambda i: (f'resources/{i}.html', i)),
        flat_map(lambda pair: rx.from_(process_problem_html(*pair))),
        to_iterable(),
        do(lambda ls: print('total: ', len(ls)))
    ).subscribe(
        partial(save_json, path=save_path)
    )
