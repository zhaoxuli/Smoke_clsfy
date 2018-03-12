# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sys
import numpy as np

log_path = sys.argv[1]
img_name = sys.argv[2]

test_list =[]
train_list = []
with open(log_path,'r') as log_file:
    for line in log_file:
        if 'Train-cross-entropy' in line:
            train_loss = float(line.split('=')[-1])
            train_list.append(train_loss)
        if 'Validation-cross-entropy' in line:
            test_loss = float(line.split('=')[-1])
            test_list.append(test_loss)
idx = np.arange(len(test_list))

test=[float(x)for x in test_list]
train=[float(x)for x in train_list]
plt.figure()
plt.xlabel('Epoch')
plt.ylabel('cross_loss')
plt.plot(test,color='b',label='test_loss')
plt.plot(train,color='r',label='train_loss')

plt.legend(loc='best')
plt.xticks(range(min(idx),max(idx)+1,50))
plt.yticks(np.arange(0,1,0.2))
plt.ylim([0,1])
plt.savefig(img_name)
#plt.show()
