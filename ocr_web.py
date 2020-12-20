import web
import requests
from cv2 import imread, imwrite
import os

urls = ('/ocr', 'ocr')


def download_img(url: str, path: str) -> bool:
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)
        return True

    return False


def cover_img(img):
    sp = img.shape
    width = sp[0]
    height = sp[1]
    for yh in range(height):
        for xw in range(width):
            color_d = img[xw, yh]
            if color_d[3] == 0:
                img[xw, yh] = [255, 255, 255, 255]


def rec_img(path: str) -> str:
    with os.popen('python3 tools/infer/predict_system.py --image_dir="%s" '
                  '--det_model_dir="./inference/ch_ppocr_server_v1.1_det_infer/" '
                  '--rec_model_dir="./inference/ch_ppocr_server_v1.1_rec_infer/" --use_angle_cls=false '
                  '--use_space_char=True --use_gpu=False' % path) as res:
        return res.read()


download_path = './temp/origin.png'
save_path = './temp/process.png'


class ocr:
    def GET(self) -> str:
        url = web.input(url='').url
        if url == '':
            return ''

        if not download_img(url, download_path):
            return ''

        # 读入原始图片
        img = imread(download_path, -1)
        # 将透明背景改为白色
        cover_img(img)
        # 保存更改背景后的图片
        imwrite(save_path, img)

        # 识别图片内容
        rec = rec_img(save_path)
        print(rec)

        # 提取输出
        lines = rec.split('\n')
        if len(lines) <= 5:
            return ''

        lines = lines[3:-2]
        capt = ['' if len(line) <= 7 else line[:-7] for line in lines]

        return ''.join(capt)

    def POST(self):
        pass


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
