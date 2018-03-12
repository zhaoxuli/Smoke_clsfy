import os
import sys
import time
path= sys.argv[1]
date = time.strftime('%m_%d_%H_%M',time.localtime(time.time()))
command = 'python '+path+'  2>&1  |tee ./'+str(date)+'.log'

#print command
os.system(command)
#24data    64 16 16
