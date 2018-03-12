#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 00:59:14 2017

@author: zhaoxu
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import sys
def get_score_list(file,normal_score_list,ground_truth_list):
 #normal=1
  info_list=[]
  label='None'
  with open(file, 'r') as result_file:
    for line in result_file.readlines():  #Each line
       if line.find('data path') != -1:
            label = str(line).split('/')[-1]
       if label.find('normal')!=-1:
                if line.find('result') != -1:
                    class_score = str(line).split()[2]
                    normal_score=class_score.split(':')[-1]
                    normal_score_list.append(float(normal_score))
                    ground_truth_list.append(1)
       if label.find('smoke')!=-1:
                if line.find('result') != -1:
                    class_score = str(line).split()[2]
                    normal_score=class_score.split(':')[-1]
                    normal_score_list.append(float(normal_score))
                    ground_truth_list.append(0)
    # print 'ongoing'
    for i in range(len(ground_truth_list)):
        info_split={'score':float(normal_score_list[i]),'truth':int(ground_truth_list[i])}
        info_list.append(info_split)
    Truth_normal_num=sum(ground_truth_list)
    return info_list,Truth_normal_num,normal_score_list,ground_truth_list
    #return normal_score_list,ground_truth_list


def draw_curve(info_list,normal_score_list,ground_truth_list):
    #normal_score_list=info_list['score']
    glass_score_list=[]
    normal_score_dist=[]
    glass_score_dist=[]
    T_glass=0
    T_normal=0
    for score in normal_score_list:
        glass_score_list.append(1-score)
    Truth_normal_num=sum(ground_truth_list)
    Truth_glass_num=len(ground_truth_list)-Truth_normal_num


    for i in np.arange(0, 1.0, 0.1):
        num = 0
        if i == 0.9:
            for ele in info_list:
                if (ele['score']>=i)and(ele['score']<=i+0.1)and(ele['truth']==1):
                        num +=1
        else:
            for ele in info_list:
                if (ele['score']>=i)and(ele['score']<i+0.1)and(ele['truth']==1):
                        num +=1
        normal_score_dist.append(float(num) / Truth_normal_num)
#    print num,Truth_normal_num
#    print 'nomal_dist',normal_score_dist

    for i in np.arange(0, 1.0, 0.1):
        num = 0
        if i == 0.9:
            for ele in info_list:
                if (1-ele['score']>=i)and(1-ele['score']<=i+0.1)and(ele['truth']==0):
                        num +=1
        else:
           for ele in info_list:
                if (1-ele['score']>=i)and(1-ele['score']<i+0.1)and(ele['truth']==0):
                        num +=1
        glass_score_dist.append(float(num) / Truth_glass_num)
#    print num,Truth_glass_num
#    print 'glass_dist',glass_score_dist

    accuracy_vs_threshold = []
    for i in np.arange(0, 1.1, 0.1):
        num = 0
        T_glass=0
        T_normal=0
        for ele in info_list:
            if float(ele['score']) <i and ele['truth']==0:
                T_glass+=1
            if float(ele['score']) >=i and ele['truth']==1:
                T_normal+=1

        accuracy_vs_threshold.append(float(T_glass+T_normal) / len(ground_truth_list))
#    print len(ground_truth_list),T_glass,T_normal
#    print accuracy_vs_threshold
    x_values = np.arange(0, 1, 0.1)
    x_values_2 = np.arange(0, 1.1, 0.1)

#    x_values = np.arange(0.05, 1.05, 0.1)

    # plt.plot(x_values, open_score0_dist)
    plt.bar(x_values, normal_score_dist, width=0.1, facecolor='lightskyblue', edgecolor='white')
    plt.xlim(0, +1.0)
    for x, y in zip(x_values, normal_score_dist):
        plt.text(x + 0.05, y, '%.3f' % y, ha='center', va='bottom')
    plt.title('Normal distribution')
    plt.xlabel('Probability')
    plt.ylabel('Num')
    plt.grid(True)

    plt.figure(2)
    # plt.plot(x_values, close_score1_dist)
    plt.bar(x_values,glass_score_dist, width=0.1, facecolor='lightskyblue', edgecolor='white')
    plt.xlim(0, +1.0)
    for x, y in zip(x_values, glass_score_dist):
        plt.text(x + 0.05, y, '%.3f' % y, ha='center', va='bottom')
    plt.title('smoke distribution')
    plt.xlabel('Probability')
    plt.ylabel('Num')
    plt.grid(True)

    plt.figure(3)
    plt.plot(x_values_2, accuracy_vs_threshold)
    for x, y in zip(x_values_2, accuracy_vs_threshold):
        plt.text(x, y - 0.03, '%.3f' % y, ha='center', va='bottom')
    plt.title('Accuracy')
    plt.xlabel('Threshold')
    plt.ylabel('Accuracy')
    plt.grid(True)


#def Calu_PR(info_list,Truth_normal_num):
    sorted_info_list={}
    print ("|  %-8s  | %-8s | %8s | %-8s | %-20s | %-4s |    " % (
    "TP", "FP", "FN", "TN",'ap','threshold'))
    #Truth_normal_num=sum(sorted_info_list['truth'])
    for j in np.arange(0.1, 1, 0.1):
        P=[]
        R=[]

        TP_normal=0
        FP_normal=0
        TN_normal=0
        FN_normal=0
        sorted_info_list=sorted(info_list,key=lambda x:x['score'],reverse=True)
        for ele in sorted_info_list:
            if float(ele['score']) >=j and ele['truth']==1:
                TP_normal+=1
            elif float(ele['score'])>=j  and  ele['truth']==0:
                FP_normal+=1
            elif float(ele['score'])<j and ele['truth']==1:
                FN_normal+=1
            elif float(ele['score'])<j and ele['truth']==0:
                TN_normal+=1
            #print TP_normal,FP_normal,FN_normal,TN_normal,ele['score'],ele['truth'],TP_normal+FP_normal,Truth_normal_num
            i=ele['score']
            P.append(float(TP_normal)/float(TP_normal+FP_normal+0.000000001))
            R.append(float(TP_normal)/float(Truth_normal_num))


        p_new=[0.00]+P
        for i in range(len(p_new)-2,0,-1):
            p_new[i]=max(p_new[i],p_new[i+1])
        r_new=[0]+R
        ap = 0
        for i in xrange(len(p_new)-1):
            if p_new[i+1] > 0.8: #0.9:
                ap += (r_new[i+1] - r_new[i])*p_new[i+1]
        print ("|  %-8s  | %-8s | %8s | %-8s | %-20s | %-9s |    " % (
        TP_normal,FP_normal,FN_normal,TN_normal,ap,j))

  #      print 'TP','    ','FP','    ','FN','    ','TN','    ','ap','               ','threshold'
  #      print TP_normal,FP_normal,FN_normal,TN_normal,ap,j
    #    print 'TP','FP','FN','TN','ap'
    #    print TP_normal,FP_normal,FN_normal,TN_normal,ap
        p_new=p_new[1:]
        r_new=r_new[1:]
        if j==0.5:
        #p_new=sorted(P)
            plt.figure(4)
            plt.plot(r_new, p_new,'b', label='PR'+str(j))
            plt.xlim(0,1,0.1)
            plt.ylim(0,1,0.1)
            plt.xlabel('recall')
            plt.ylabel('precesion')
            plt.legend(loc='center left')
    #plt.scatter(R,P)
    plt.show()


    #plt.savefig('/home/zhaoxu/try/test.jpg')
   # return p_new,r_new,ap
if __name__ == '__main__':
    filepath=sys.argv[1]
    normal_score_list=[]
    ground_truth_list=[]
    for root,dirs,files in os.walk(filepath):
        for file in files:#Each txt file
            #file=files[1]
            txtpath=(os.path.join(root, file))
            info_list,Truth_normal_num,normal_score_list,ground_truth_list=get_score_list(txtpath,normal_score_list,ground_truth_list)
            #y_scores,y_true=get_score_list(txtpath,normal_score_list,ground_truth_list)
            #print len(normal_score_list) ,len(ground_truth_list)
            #print 'ongoing'
        print  'Normal_Count:',sum(ground_truth_list)
        print  'Smoke_Count:',len(info_list)-sum(ground_truth_list)
        draw_curve(info_list,normal_score_list,ground_truth_list)
        #p_new,r_new,ap=Calu_PR(info_list,Truth_normal_num)





