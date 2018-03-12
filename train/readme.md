# train 脚本说明
`bn_smoke.py`    是整个训练文件。结构很简单，就不拉出来单写了symbol了。  
`train_full.py`  调用bn_smoke.py用小时和分钟挂做后缀，生成log文件。  
`pick_epoch.py`  通过log得到best的epoch数  
`draw_loss.py`   通过log画loss，暂时为ce，可以自己改。
