import mxnet as mx
import argparse
import numpy as np
from collections import namedtuple
import cv2
import os
import sys


#python  get_result_file.py  model   epoch  out_dir_name
print  'python  get_result_file.py  model   epoch  '

model_version = ''
data_path =  '/data/zhaoxu.li/smoke_data/test_data/normal'
model_url =  sys.argv[1]
#model_url = '/home/users/dawei.yang/zhaoxu.li/mxnet_eye/eycls_scrip/cifar_10/1channel//models/model'


epoch = sys.argv[2]
epoch =  int(epoch)
out_dir_path = './'


Batch = namedtuple('Batch', ['data'])
#initialize mod
sym, arg_params, aux_params = mx.model.load_checkpoint(model_url, epoch)
mod = mx.mod.Module(symbol=sym, context=mx.cpu(), label_names=None)
mod.bind(for_training=False, data_shapes=[('data', (1,1,32,32))],
    label_shapes=mod._label_shapes)
mod.set_params(arg_params, aux_params, allow_missing=True)


def get_result(model_url, epoch, img_url):
#get img reshape img to  bacth,channel,h,w
    img = cv2.imread(img_url,0)
    img = cv2.resize(img,(32,32))

    img = img[np.newaxis, :]
    img = img[np.newaxis, :]
    size =  img.shape
    mod.forward(Batch([mx.nd.array(img)]))
#do predict
    prob = mod.get_outputs()[0].asnumpy()
    open_score = prob[0][0]
    close_score = prob[0][1]
    if (open_score - close_score) > 0:
        if open_score > 0.6:
            result = '0'
        else :
            result = '0'
    else:
        result = '1'
    prob = np.squeeze(prob)
    print prob

    #score is open score
    return  int(result),open_score

def get_file_list(data_dir):
    key_dirs = []
    dir_type = 'normal|smoke'
    sub_dirs = os.walk(data_dir)
    key_type = dir_type.split('|')
    for sub_dir_files in sub_dirs:
        sub_dir = sub_dir_files[0]
        if sub_dir.split(os.sep)[-1] in key_type:
            #print sub_dir,len(All_img)
            key_dirs.append(sub_dir)
    return key_dirs

def  get_small_scale(open_score ):
    if (open_score < 0.0001):
        open_score = 0.0001
    if ((1 - open_score) < 0.0001 ):
        open_score = 0.9999
    return open_score


if __name__ == '__main__':
    img_url = sys.argv[3]
    result,open_score = get_result(model_url,epoch,img_url)
    print '0/smoke_score',open_score
