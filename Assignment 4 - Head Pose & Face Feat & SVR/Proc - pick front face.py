# coding: utf-8
import os

import cv2

from module.face_yrp import FaceYRP

folder = 'IMG/DATA/A'

total = len(os.listdir(folder))

threshold = 10


def rotate(image, angle, center=None, scale=1.0):
    # 获取图像尺寸
    (h, w) = image.shape[:2]

    # 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)

    # 执行旋转
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    # 返回旋转后的图像
    return rotated


for index, fn in enumerate(os.listdir(folder)[539:759]):
    print('{} / {}'.format(index + 1, total))
    img_path = '{}/{}'.format(folder, fn)
    if os.path.exists(img_path):
        raw_img = cv2.imread(img_path)
        try:
            face_yrp = FaceYRP(raw_img, image_name=fn)
            face_yrp.launch()
            if face_yrp.result:
                if face_yrp.roll and -threshold < face_yrp.pitch < threshold and -threshold < face_yrp.yaw < threshold:
                    dest_path = 'IMG/OUTPUT/{}'.format(fn)
                    temp = raw_img.copy()
                    temp = rotate(temp, - face_yrp.roll)
                    cv2.imwrite(dest_path, temp)

        except Exception as e:
            print(e)
            print('[WARN] - error Image - {}'.format(img_path))

    else:
        print('!!!!', img_path)
