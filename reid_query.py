import os
from os import pardir
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from feature_extract.utils.util import get_distance
from numpy.core.defchararray import title

"""
author: liuyalei
email: liuyalei@mail.ustc.edu.cn
date: 2/12/2021
"""

def imshow(path, title=None):
    im = cv.imread(path)
    im = cv.resize(im,(256,512))
    im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
    plt.imshow(im)
    if title is not None:
        plt.title(title)



# 计算两个图像之间的距离，放到列表里
def rank(probe_ft, gallery_ft, title):

    # import pdb
    # pdb.set_trace()

    distance = []
    oushi = []

    for i in range(len(gallery_ft)):
        temp_dist = get_distance(probe_ft, gallery_ft[i][0])
        distance.append([temp_dist, gallery_ft[i][1]])
        oushi.append(temp_dist)
    oushi = np.array(oushi)
    distance_array = np.array(distance)

    dis_T = distance_array.T
    dis = dis_T[0]
    # gallery_label = dis_T[1]
    rank_path = dis_T[1]

    dis = dis[oushi.argmin()]
    # gallery_label = gallery_label[oushi.argsort()]
    rank_path = rank_path[oushi.argmin()]
    return dis, rank_path

probe_ft=np.load('E:\\python_prj\\Video-Person-Search\\feature_extract\\probeft-2048.npy', allow_pickle=True)
shot_path = "E:\\python_prj\\yolov5-master\\runs\\detect\\exp_2\\crops\\person\\shot_feature"
distance = []
oushi = []


def get_shot_num(path):
    strs = path.split("\\")
    name = strs[len(strs) - 1]
    return name[9: 12]


for root, dirs, files in os.walk(shot_path):
    for file in files:
        feature_path = os.path.join(root, file)
        gallery_ft = np.load(feature_path, allow_pickle=True)
        for probe in probe_ft:
            pro_path = probe[1]
            dis, rank_path = rank(probe[0], gallery_ft, probe[1])
            distance.append([dis, rank_path])
            oushi.append(float(dis))

    oushi = np.array(oushi)
    distance_array = np.array(distance)

    dis_T = distance_array.T
    dis = dis_T[0]
    # gallery_label = dis_T[1]
    rank_path = dis_T[1]

    dis = dis[oushi.argsort()]
    # gallery_label = gallery_label[oushi.argsort()]
    rank_path = rank_path[oushi.argsort()]

    print('距离排序\n', dis[:20])
    print('rank排序\n', rank_path[:10])
    # print('gallery lable\n', gallery_label[:10])

    plt.figure(pro_path, figsize=(10, 5))
    ax = plt.subplot(1, 11, 1)
    ax.axis('off')

    imshow(pro_path, 'probe')
    for i in range(10):
        shot_num = get_shot_num(rank_path[i])
        print(shot_num)
        ax = plt.subplot(1, 11, i + 2)
        ax.axis('off')
        ax.set_title(shot_num)

        imshow(rank_path[i], shot_num)
    plt.savefig("E:\\python_prj\\Video-Person-Search\\feature_extract\\res.png")


