# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import random


# 清理隐藏文件
def clear_hidden_files(path):
    dir_list = os.listdir(path)
    for i in dir_list:
        abspath = os.path.join(os.path.abspath(path), i)
        if os.path.isfile(abspath):
            if i.startswith("._"):
                os.remove(abspath)
        else:
            clear_hidden_files(abspath)


# 将数据集切分为train,test,val
def split_dataset_with_txt(train_percent):
    total_xml = os.listdir(image_dir)
    num = len(total_xml)
    list = range(num)
    tv = int(num)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)
    ftrainval = open('trainval.txt', 'w', encoding='utf-8')
    ftrain = open('train.txt', 'w', encoding='utf-8')
    fval = open('val.txt', 'w', encoding='utf-8')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
    ftrainval.close()
    ftrain.close()
    fval.close()


if __name__ == '__main__':

    # 类名
    classes = ['fall']
    # 划分训练验证测试集，自行修改
    sets = ['train', 'val']
    root_dir = "/root/autodl-tmp/falldetection/data/v3/"
    image_dir = root_dir + "images/"
    txt_dir = root_dir + 'labels/'

    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)

    clear_hidden_files(image_dir)

    # 切分数据集,txt文件处理
    train_percent = 0.8  # 训练集验证集比例
    split_dataset_with_txt(train_percent)

    # 对训练集，验证集，测试集进行处理
    for image_set in sets:
        image_ids = open('%s.txt' % (image_set), encoding='utf-8').read().strip().split()
        # 打开对应的train.txt 文件对其进行写入准备
        list_file = open(root_dir + '%s.txt' % (image_set), 'w', encoding='utf-8')
        # 将对应的文件_id以及全路径写进去并换行
        for image_id in image_ids:
            list_file.write(image_dir + '%s.jpg\n' % (image_id))
        # 关闭文件
        list_file.close()

    os.remove(r'train.txt')
    os.remove(r'val.txt')
    os.remove(r'trainval.txt')