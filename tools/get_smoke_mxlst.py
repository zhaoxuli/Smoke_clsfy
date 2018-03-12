# -*- coding: utf-8 -*
import os
import cv2

all_path = './data'
train_folders = './train_folders.txt'

folders = open(train_folders,'r').readlines()

train_list = []
test_list = []
test_index = 0
train_index = 0
num = 0

for ele in folders:
    fld_path = ele[:-1]
    key  =  ele.split(os.sep)[-1][:-1]
    img_list = os.listdir(fld_path)
    for img in img_list:
        img_url = fld_path+os.sep+img
        print img_url
        if key == 'normal':
            cls_id = 1
        if key == 'smoke':
            cls_id = 0
        if num ==5:
            num = 0
            test_list.append('\t'.join([str(test_index)]+[str(cls_id)]+[str(img_url)])+'\n')
            test_index +=1
        else:
            train_list.append('\t'.join([str(train_index)]+[str(cls_id)]+[str(img_url)])+'\n')
            train_index +=1
        num = num+1

if test_list:
    import random
    random.shuffle(test_list)
    test_name = './mx_temp_lst/test.lst'
    with open(test_name, 'w') as f:
        for line in test_list:
            f.write(line)
if train_list:
    import random
    random.shuffle(train_list)
    test_name = './mx_temp_lst/train.lst'
    with open(test_name, 'w') as ft:
        for line in train_list:
            ft.write(line)

