from functools import partial

import rx
from rx.operators import map, to_iterable

from utils import *

"""
全部无法纠正的错误：

警告：第 0 章第 31 道题目无法自动纠错，请手动处理：
31.单选（2分）1984年1月3日意大利人卡内帕给恩格斯写信，请求他为即将在日内瓦出版的饿《新纪元》周刊的创刊号题词，而且要求尽量用简短的字句来表述未来的社会主义纪元的基本思想以区别于伟大诗人但丁的对纪元所作的一些人统治，另一些人受苦难”的界定。恩格斯回答说这就是：“代替那存在着阶级和阶级对立的资产阶级社会的，将是这样一个联合体在那里每个人的自由发展是一切人的自由发展的条件。”这段话表明，马克思主义追求的根本价值目标是（）
警告：第 1 章第 78 道题目无法自动纠错，请手动处理：
78.在互联网上，有人发起“超能力”的培讲课程教学员利用本我的意念”来移动物体的置甚至是直接改变物质结构。这是信奉（）
警告：第 1 章第 81 道题目无法自动纠错，请手动处理：
81.马克思说：“人在劳动过程结束时得到的结果，在这个过程开始时就已经在劳动者的表象中存在着，即已经观念地存在着。人的活动的整个过程就是围绕着“观念地存在着”的目标和蓝图而进行的。这说明了（）
警告：第 1 章第 98 道题目无法自动纠错，请手动处理：
97.俗话说“过犹不及”，我们在工作中要尽量防止“过”和不及”。把握这一点的关键在于（）
警告：第 1 章第 140 道题目选项 1 无法自动纠错，请手动处理：
两点论”与“重点论"相结合
警告：第 1 章第 190 道题目无法自动纠错，请手动处理：
24.2016年3月，谷歌“阿尔法狗与李世石上演人机五番棋大战最终，李世石以四负一胜的结局输给了“阿尔法狗”。人工智能在棋盘上战胜人类，这样的结果令人惊讶。这一事件给我们的启示是
警告：第 1 章第 204 道题目无法自动纠错，请手动处理：
38.‘守株待兔”是中国古代寓言中一个内涵深刻的故事,故事中的主人公采取“守株”的方法,最终没有能够成功地“待免”。其失败的原因在于
警告：第 2 章第 34 道题目无法自动纠错，请手动处理：
34.“公说公有理，婆说婆有理与“仁者见仁智者见智”这两种说法（）
警告：第 2 章第 82 道题目无法自动纠错，请手动处理：
82.列宁在谈到检验真理的实践标准时指出：“这个标准也这是样的不确定,以便不至于使人的知识变成绝对”同时它又是这样的确定，以便同唯心主义和不可知论的一切变种进行无情的斗争。"这句话说明（）
警告：第 2 章第 153 道题目无法自动纠错，请手动处理：
39.认为“真理是思想形式是人类经验的组织形式”，是具有普遍意义”的“社会的组织起来的经验”。这种观点（）
警告：第 3 章第 20 道题目无法自动纠错，请手动处理：
20.随着我国经济社会发展的转型，关注发展质量、增加民生福社被提到了前所未有的高度在城市形象宣传中，“幸福”“活力".生态"等成了常见的宣传语。这说明0
警告：第 3 章第 121 道题目无法自动纠错，请手动处理：
121.卢梭在《论人类不平等的起源和基础》中说道：“我认为.在人类的一切知识中最有用但也最不完善的知识就是关于人的知识马克思的唯物史观破解了人是什么这一"斯芬克斯之谜"马克思在《关于费尔巴哈的提纲》中指出人的本质在其现实性上是（）
"""


def chip_problem_index(problem_text: str) -> str:
    # 找到题目编号后一位的下标
    idx = 0
    while '0' <= problem_text[idx] <= '9':
        idx += 1

    if problem_text[idx] in '.．。，,':
        idx += 1

    if problem_text[idx] == ' ':
        idx += 1

    return problem_text[idx:]


chinese_letter_transformation = str.maketrans('():,．"', '（）：，.“')


def translate_chinese_letter(problem_text: str) -> str:
    return problem_text.translate(chinese_letter_transformation)


def correct_text_quotation(translated_text: str) -> str:
    # 匹配引号
    left_double_quotation_marks_count = translated_text.count('“')
    right_double_quotation_marks_count = translated_text.count('”')
    double_quotation_marks_count = left_double_quotation_marks_count + right_double_quotation_marks_count

    if double_quotation_marks_count == 0:
        return translated_text
    elif double_quotation_marks_count % 2 != 0:
        if double_quotation_marks_count == 1:  # 舍弃单括号
            if left_double_quotation_marks_count == 1:
                return translated_text.replace('“', '')
            if right_double_quotation_marks_count == 1:
                return translated_text.replace('”', '')
        else:
            raise RuntimeError('无法自动纠正引号不匹配错误')
    else:
        quotation_corrected_chars = list(translated_text)
        should_be_left = True

        for i, ch in enumerate(translated_text):
            if ch == '“':
                if not should_be_left:
                    quotation_corrected_chars[i] = '”'
                should_be_left = False
            elif ch == '”':
                if should_be_left:
                    quotation_corrected_chars[i] = '“'
                should_be_left = True

        return ''.join(quotation_corrected_chars)


def chip_problem_tail(problem_text: str) -> str:
    idx = len(problem_text) - 1
    while problem_text[idx] in '0（）':
        idx -= 1

    return problem_text[:idx + 1]


def correct_problem(problem: dict) -> dict:
    problem['problem'] = rx.just(
        problem['problem']
    ).pipe(
        map(chip_problem_index),
        map(translate_chinese_letter),
        map(chip_problem_tail)
    ).run()

    try:
        problem['problem'] = rx.just(
            problem['problem']
        ).pipe(
            map(correct_text_quotation)
        ).run()
    except RuntimeError:
        print(f'警告：第 {problem["chapter"]} 章第 {problem["index"]} 道题目无法自动纠正引号不匹配错误，请手动处理：')
        print(f'\t{problem["problem"]}')
        problem["problem"] = input()

    problem['options'] = rx.from_(problem['options']).pipe(
        map(translate_chinese_letter)
    ).run()

    for i, option_text in enumerate(problem['options']):
        try:
            problem['options'][i] = correct_text_quotation(option_text)
        except RuntimeError:
            print(f'警告：第 {problem["chapter"]} 章第 {problem["index"]} 道题目选项 {i} 无法自动纠正引号不匹配错误，请手动处理：')
            print(f'\t{option_text}')
            problem['options'][i] = input()

    return problem


if __name__ == '__main__':
    origin_text_problems_path = 'temp/problems.json'
    corrected_problems_save_path = 'temp/corrected_text_problems.json'

    rx.from_iterable(
        load_json(origin_text_problems_path)
    ).pipe(
        map(correct_problem),
        to_iterable()
    ).subscribe(
        partial(save_json, path=corrected_problems_save_path)
    )
