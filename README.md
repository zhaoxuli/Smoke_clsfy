# Smoking Classification Project document
## [Pre_setting]    
You can modify [./env_011.sh](./env_011.sh) to choose the mxnet_path which you want to .  

## [Introduce]
抽烟分类是一个简单的二分类任务。  
大体流程可以分为三部分：`Data_Process`,`Train`,`Evalution`
## Step 1 . Data_Process
* 在得到gt文件后，针对两个类别的数量差要做适量比例的Augmentation。除此之外，  Augmentation也有提升模型性能的作用。For smoking 有两套Augmentation的脚本流程。

###  Augmentation.1
* 这套流程的augmentation 方式为旋转，通过img_matrix 乘上一个 wrap 矩阵，实现img的转的。 

```
$cd ./tools/
##  find the path of each class write into train_folders.txt 
$python list_train_folders.py  \
-root_dir=/data/zhaoxu.li/smoke_data/data \  # 待训练图片存放位置，根据类别分为'smoke|normal'
-dir_type="smoke|normal"   >  /data/zhaoxu.li/smoke_data/train_folders.txt

##  get image numbers of each class  by train_foders.txt
$python  count_num.py   

##  change the ratio of two classes by the images_num of each class
##  remember modify the ratio parameters in this script
$python   get_dis_symbol.py          
$sh disturb.sh  #do disturb

## Write groudthruth  and img_url into txt for trainning/testing
$python  list_smoke_classify_train_files.py  \
/data/zhaoxu.li/smoke_data/smoke_20180126_train_test/train \
 -recursive=1 > /data/zhaoxu.li/smoke_data/mx_data/0126_data/train.txt     

$python  list_smoke_classify_train_files.py  \
/data/zhaoxu.li/smoke_data/smoke_20180126_train_test/test \
 -recursive=1 > /data/zhaoxu.li/smoke_data/mx_data/0126_data/test.txt 

 ## transform  txt to lst for mxnet trainning/testing
 $python  convert_caffeList_to_mxnetList.py  \
     /data/zhaoxu.li/smoke_data/mx_data/0126_data/test.txt  \
     /data/zhaoxu.li/smoke_data/mx_data/0126_data/test.lst
 $python  convert_caffeList_to_mxnetList.py  \
      /data/zhaoxu.li/smoke_data/mx_data/0126_data/train.txt  \
      /data/zhaoxu.li/smoke_data/mx_data/0126_data/train.lst

## get rec data
$cd /data/zhaoxu.li/smoke_data/mx_data/0126_data/
$python  ~/Yolo/mxnet-yolo/mxnet/tools/im2rec.py  \
        --color=0 --encoding='.png' --quality=9   \
        --num-thread=4 --resize=32    ./  ./
```
### Augmentation.2
* 这套流程采用不同的Augmentation方式，具体可以参考[./tools/smoke_Augmentation.py](./tools/smoke_Augmentation.py).

```
$cd ./tools
##  find the path of each class write into train_folders.txt 
$python list_train_folders.py  \
-root_dir=/data/zhaoxu.li/smoke_data/data \  # 待训练图片存放位置，根据类别分为'smoke|normal'
-dir_type="smoke|normal"   >  /data/zhaoxu.li/smoke_data/train_folders.txt

##  get image numbers of each class  by train_foders.txt
$python  count_num.py   

## do distrub on data  modify the input/output path and the radio of two classes
$python smoke_Augmentation.py

##  move the out_augmentation_data to the --root_dir path
$mv /where/output/Augmentation_data  /data/zhaoxu.li/smoke_data/data

##  get  train/test  mxnet_lst 
$python get_smoke_mxlst.py

## get rec data
$cd /data/zhaoxu.li/smoke_data/mx_data/0126_data/
$python  ~/Yolo/mxnet-yolo/mxnet/tools/im2rec.py  \
        --color=0 --encoding='.png' --quality=9   \
        --num-thread=4 --resize=32    ./  ./
```
## Step2 . Train_symbol
各个脚本作用，参考[./train/readme.md](./train/readme.md)
```
$cd ./train
python tran_full.py
```

## Step3 . Evalution
```
$cd   ./evalution
$ python get_reslut.py  model_path  best_epoch_num  result_folder
$ python draw_curve.py  result_folder
```
各个脚本作用，参考[./evalution/readme.md](./evalution/readme.md)
