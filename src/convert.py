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
def split_dataset_with_txt(trainval_percent,train_percent):
    total_xml = os.listdir(annotation_dir)
    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)
    ftrainval = open('trainval.txt', 'w', encoding='utf-8')
    ftest = open('test.txt', 'w', encoding='utf-8')
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
        else:
            ftest.write(name)
    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()
 
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
 
def convert_annotation(image_id):
    out_file = open(txt_dir+'%s.txt' % image_id, 'w', encoding='utf-8')
    in_file = open(annotation_dir+'%s.xml' % image_id, encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
 
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
 
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        print(b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    in_file.close()
    out_file.close()
 
 
if __name__ == '__main__':
 
    # 类名
    classes = ['fall']
    # 划分训练验证测试集，自行修改
    sets = ['train', 'test', 'val']
    root_dir = r"/root/autodl-tmp/falldetection/data/v3/"
    annotation_dir = root_dir + "Annotations/"
    image_dir = root_dir + "images/"
    txt_dir = root_dir + 'labels/'
 
    if not os.path.isdir(annotation_dir):
            os.mkdir(annotation_dir)
    if not os.path.isdir(image_dir):
            os.mkdir(image_dir)
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
 
    clear_hidden_files(image_dir)
    clear_hidden_files(annotation_dir)
    
    # 切分数据集,txt文件处理
    trainval_percent = 1    # 训练验证集与测试集比例
    train_percent = 0.8     # 训练集验证集比例
    split_dataset_with_txt(trainval_percent, train_percent)
 
    # 对训练集，验证集，测试集进行处理
    for image_set in sets:
        image_ids = open('%s.txt' % (image_set), encoding='utf-8').read().strip().split()
        # 打开对应的train.txt 文件对其进行写入准备
        list_file = open(root_dir+'%s.txt' % (image_set), 'w', encoding='utf-8')
        # 将对应的文件_id以及全路径写进去并换行
        for image_id in image_ids:
            list_file.write(image_dir+'%s.jpg\n' % (image_id))
            convert_annotation(image_id)
        # 关闭文件
        list_file.close()

