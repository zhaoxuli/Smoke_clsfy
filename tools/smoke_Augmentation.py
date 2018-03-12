# -*- coding: utf-8 -*-
import os
import  cv2
import copy as cp
import numpy as np
#from skimage  import exposure

def Contrast(img,k=0.7):
    dst = cp.deepcopy(img)
    Avg = dst.mean()
    dst = (img-Avg)*k + img
    print 'finish constrat'
    return dst

def EquHist(img):
    w,h,c = img.shape
    dst = cp.deepcopy(img)
    for i in range(c):
        img[:,:,i] = cv2.equalizeHist(img[:,:,i])
    return img

def  Illuminate(img):
    gamma1 = float(np.random.randint(1,19))/10
    illu_img= exposure.adjust_gamma(img_data, gamma1)
    return  illu_img

def local_high(img,alpha=1.2,b=10,k1=0.2,k2=0.3):
    #k1,k2 is the range of img_size  defalut 0.2-0.3
   # bias = np.random.randint(0,b)
   # value = img[w,h,c]*alpha +bias
    #mask = zeros(img.shape)
    max_k = max(k1,k2)
    min_k = min(k1,k2)
    max_k = max_k+0.01


    img_w,img_h= img.shape
    dst = cp.deepcopy(img)
    x_loc = np.random.randint(1,img_w)
    y_loc = np.random.randint(1,img_h)
    width = np.random.randint(img_w*min_k,img_w*max_k)
    height  = np.random.randint(img_h*min_k,img_h*max_k)
    if x_loc < int(img_w/2):
        x_loc_end = x_loc + width
    else :
        x_loc_end = x_loc
        x_loc = x_loc - width
    if y_loc < int(img_h/2):
        y_loc_end = y_loc + height
    else :
        y_loc_end = y_loc
        y_loc = y_loc - height
   # print x_loc,x_loc_end,'       ',y_loc,y_loc_end
    for w in range(x_loc,x_loc_end):
        for h in range(y_loc,y_loc_end):
                if b >0:
                    bias = np.random.randint(0,b)
                else :
                    bias = np.random.randint(b-1,0)

                value = img[w,h]*alpha +bias
                if value > 255:
                    value = 255
                if value < 0:
                    value = 0
                dst[w,h] = value
    return dst

def noise(img,type_noise,kernel_size=(5,5),sigma=0,slat_ratio=0.008,papper_radtio=0.01):
    img_w,img_h = img.shape
    if type_noise == 'gaussian':
        img = cv2.GaussianBlur(img,kernel_size,sigma)

    if type_noise == 'salt':
        count_all = img.shape[0] * img.shape[1]
        salt_num = int(count_all*slat_ratio)
        for n in range(salt_num):
            m = np.random.randint(1,img_w)
            n = np.random.randint(1,img_h)
            img[m,n] = 255

    if type_noise == 'papper':
        count_all = img.shape[0] * img.shape[1]
        papper_num = int(count_all*papper_ratio)
        for n in range(papper_num):
            m = np.random.randint(1,img_w)
            n = np.random.randint(1,img_h)
            img[m,n] = 0


    if type_noise == 'all':
        img = cv2.GaussianBlur(img,kernel_size,sigma)
        count_all = img.shape[0] * img.shape[1]
        salt_num = int(count_all*slat_ratio)
        for n in range(salt_num):
            m = np.random.randint(1,img_w)
            n = np.random.randint(1,img_h)
            rand_key = np.random.randint(0,2)
            if rand_key ==1:
                 img[m,n] = 255
            else:
                 img[m,n] = 0
    return img


def rotate(img,center,angle,scale=1):
    #rotate_format: x_new = int(x_old*np.sin(angle) + y_old*np.cos(angle))
    img_w,img_h = img.shape
    print img.shape
    if center == 'normal':
        center_points = (img_w/2,img_h/2)
    if center == 'random':
        width = img_w*0.1
        height = img_h*0.1
        x = np.random.randint(img_w/2-width , img_w/2+width)
        y = np.random.randint(img_h/2-height , img_h/2+height)
        center_points = (x,y)

    M = cv2.getRotationMatrix2D(center_points ,angle, scale)
    rotated = cv2.warpAffine(img,M,(img_h,img_w))
    print 'finish rotate'
    return  rotated


def do_distrub(img_url,new_img_url):
    img = cv2.imread(img_url,0)
    Rotate_angle = np.random.randint(-15,15)
    Rotate_scale = 1
    lh_alpha = np.random.randint(2,11)*0.1
    lh_bias = np.random.randint(-40,10)
    lh_k1 = min(np.random.randint(1,4)*0.1,np.random.randint(1,4)*0.1)
    lh_k2 = max(np.random.randint(1,4)*0.1,np.random.randint(1,4)*0.1)
    if lh_k2 == lh_k1:
        lh_k2 +=0.1
    cst_k = np.random.randint(3,9)*0.1
    type_key = np.random.randint(0,4)
    if type_key == 0:
        img = Contrast(img,cst_k)
        img = rotate(img,'normal',Rotate_angle,Rotate_scale)

    if type_key == 1:
        img = rotate(img,'normal',Rotate_angle,Rotate_scale)
        img = local_high(img,lh_alpha,lh_bias,lh_k1,lh_k2)
 #       img = rotate(img,'normal',Rotate_angle,Rotate_scale)

    if type_key == 2:
        img = Contrast(img,cst_k)
 #       img = noise(img , 'all')
        img = local_high(img,lh_alpha,lh_bias,lh_k1,lh_k2)
    if type_key == 3:
        img = rotate(img,'normal',Rotate_angle,Rotate_scale)
        img = noise(img , 'all')
    cv2.imwrite(str(new_img_url),img)
    print 'finish write'
    return




if __name__ == '__main__':
    out_path = '/data/zhaoxu.li/smoke_data/train_data_Augmentation'
    input_path = '/data/zhaoxu.li/smoke_data/data/'
    ratio = '2:2'  #smoke:normal

    all_smoke_list = []
    all_normal_list = []

    all_folder = open('/data/zhaoxu.li/smoke_data/train_folders.txt').readlines()
    for ele in all_folder:
        if 'normal' in ele:
            normal_folder = ele[:-1]
            img_key_list = os.listdir(normal_folder)
            for img_key in img_key_list:
                img_url = normal_folder +os.sep+ img_key
                all_normal_list.append(img_url)
        if 'smoke' in ele:
            smoke_folder = ele[:-1]
            img_key_list = os.listdir(smoke_folder)
            for img_key in img_key_list:
                img_url = smoke_folder +os.sep+ img_key
                all_smoke_list.append(img_url)

    smoke_num = int(ratio.split(':')[0])*len(all_smoke_list)
    normal_num = int(ratio.split(':')[1])*len(all_normal_list)

    count =1
    #get all  target counts  when  count < normal_num  dont distrub
    #when cout >normal_num  do distrub
#####################################################
    while(count< normal_num ):

        if count <len(all_normal_list):
            img_url = all_normal_list[count]
            lst = img_url.split(os.sep)
            #new_img_url = img_url.replace(input_path,out_path)
            new_img_url = out_path+os.sep+lst[-3]+os.sep+lst[-2]+os.sep+lst[-1]

            #print img_url
            new_folder = os.sep.join(new_img_url.split(os.sep)[:-1])
            #new_img_url = out_path + img_url.split('data')[]
            #print new_folder
            if os.path.exists(new_folder) == False:
                os.makedirs(new_folder)
            #cmd = 'cp '+img_url +' '+new_img_url
            #os.system(cmd)
            #print cmd
        else:
            num = count -((int(count/len(all_normal_list)))*len(all_normal_list))
            img_url = all_normal_list[num]
            lst = img_url.split(os.sep)
            new_img_url = out_path+os.sep+lst[-3]+os.sep+lst[-2]+os.sep+lst[-1]

            print 'new_img_url:',out_path+os.sep+lst[-2]+os.sep+lst[-1]
            #print  new_img_url[:-4]+'_'+str((int(count/len(all_normal_list))))+'.png'
            do_distrub(img_url,new_img_url)
        count +=1

    while(count< smoke_num ):
        if count <len(all_smoke_list):
            img_url = all_smoke_list[count]
            lst = img_url.split(os.sep)
            #new_img_url = img_url.replace(input_path,out_path)
            new_img_url = out_path+os.sep+lst[-3]+os.sep+lst[-2]+os.sep+lst[-1]

            #print img_url
            new_folder = os.sep.join(new_img_url.split(os.sep)[:-1])
            #new_img_url = out_path + img_url.split('data')[]
            #print new_folder
            if os.path.exists(new_folder) == False:
                os.makedirs(new_folder)
            #cmd = 'cp '+img_url +' '+new_img_url
            #os.system(cmd)
            #print cmd
        else:
            num = count -((int(count/len(all_smoke_list)))*len(all_smoke_list))
            img_url = all_smoke_list[num]
            lst = img_url.split(os.sep)

#            new_img_url = img_url.replace(input_path,out_path)
            new_img_url = out_path+os.sep+lst[-3]+os.sep+lst[-2]+os.sep+lst[-1]

            print 'new_img_url:',out_path+os.sep+lst[-2]+os.sep+lst[-1]
            #print  new_img_url[:-4]+'_'+str((int(count/len(all_normal_list))))+'.png'
            do_distrub(img_url,new_img_url)
        count +=1


