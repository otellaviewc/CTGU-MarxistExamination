from typing import List

import rx
from rx.operators import map, flat_map, to_iterable

from process_answer_html import process_answer_html
from process_problem_html import process_problem_html

# TODO 清洗试卷题目 html 得到试卷题目图片链接列表


def list_chapters_html():
    return rx.pipe(
        map(lambda i: (f'./resources/{i}.html', i))
    )


def list_chapters_problems():
    return rx.pipe(
        list_chapters_html(),
        flat_map(lambda pair: rx.from_(process_problem_html(*pair)))
    )


# TODO OCR 试卷题目列表得到试卷题目文本列表

# TODO 清洗试卷答案 html 文件得到试卷答案列表


def list_chapters_answer_html():
    return rx.pipe(
        map(lambda i: f'./resources/a{i}.html')
    )


def format_answer(answer: str) -> List[int]:
    return [ord(ch) - ord('A') for ch in answer]


def list_chapters_answers():
    return rx.pipe(
        list_chapters_answer_html(),
        flat_map(lambda path: rx.from_(process_answer_html(path))),
        map(format_answer)
    )


# TODO 将答案插入试卷题目列表中

# TODO 将题目按照拼音序排序

# TODO 将排好序的题目数据转化为 doc 文档

# TODO 串联处理流


def migrate_chapter_6_7_then_reprint():
    """
    流程：获取后两章的答案和题目。将其拼接在一起后发送给
    """
    chapter_6_7_problems = rx.just(6, 7).pipe(
        list_chapters_problems()
    )

    chapter_6_7_answers = rx.just(6, 7).pipe(
        list_chapters_answers()
    )


if __name__ == '__main__':
    migrate_chapter_6_7_then_reprint()
