# -*- coding: utf-8 -*-
import os

PRE_PRINT_RES = True

# 需要处理的文件夹列表
src_folders = '/data/zhaoxu.li/smoke_data/train_folders.txt'
# 存储的脚本名称
fn_cmd = "disturb_in_pic.sh"

# 扰动脚本
disturb_script = 'disturb_in_pic.py'
# 扰动倍数
disturb_times = {'normal':1, 'smoke':1,}
save_path = '/data/zhaoxu.li/smoke_data/smoke_20180201_train_test/'

def skip_comments_and_blank(file, cm='#'):
    lines = list()
    for line in file:
        #print line
        line = line.strip()
        if not line.startswith(cm) and not line.isspace():
            lines.append(line)
    return lines


if __name__ == '__main__':

    out_f = open(fn_cmd, 'w')

    lines = skip_comments_and_blank(open(src_folders))
    for line in lines:
        if line[-1] == os.sep:
            line = line[:-1]

        class_dir = line.split(os.sep)[-1] # a_close
        disturb_time = disturb_times[class_dir]
        out_line = 'python ' + disturb_script
        out_line += ' -pic_dir=' + line + ' -save_path=' + save_path + ' -disturb_time=' + str(disturb_time)

        if PRE_PRINT_RES:
            print out_line
        out_f.write(out_line + '\n')

    out_f.truncate(out_f.tell()-1)
    out_f.close()
