import json
import requests
import time

data_path = 'temp/data.json'
save_path = 'temp/problems.json'


def ocr_img(img_url: str) -> str:
    r = requests.get('http://39.101.136.93:8080/ocr', params={'url': img_url})
    r.encoding = 'utf-8'
    return r.text


def ocr_problem(problem: dict):
    # 识别题目中的图片数据
    # print(json.dumps(problem, sort_keys=True, indent=4, separators=(',', ': ')))
    problem_img_url = problem['problem']
    problem['problem'] = ocr_img(problem_img_url)
    print(problem['problem'])

    options_img_url = problem['options']
    options_text = []
    for option_img_url in options_img_url:
        option_text = ocr_img(option_img_url)
        options_text.append(option_text)
        print(option_text)

    problem['options'] = options_text


def ocr_problems(problems: list):
    total = len(problems)
    count = 0

    start = time.time()

    for problem in problems:
        ocr_problem(problem)

        time.sleep(60)

        count += 1
        avg = (time.time() - start) / count

        print('progress: %.1f' % (count / total * 100) + '%, ' + 'rest time: %.1fmin' % (avg * (total - count) / 60))


if __name__ == '__main__':
    # 读取题目列表 json 数据
    with open(data_path, 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)

    ocr_problems(data)

    problems_json = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    with open(save_path, 'w', encoding='utf-8') as save_file:
        save_file.write(problems_json)
