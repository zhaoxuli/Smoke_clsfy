import os
import glob
import argparse
import sys
src_folders = '/data/zhaoxu.li/smoke_data/train_folders.txt'


def skip_comments_and_blank(file, cm='#'):
    lines = list()
    for line in file:
        line = line.strip()
        if not line.startswith(cm) and not line.isspace():
            lines.append(line)
    return lines


if __name__ == '__main__':
    dir_types = {}
    lines = skip_comments_and_blank(open(src_folders))
    for sub_dir in lines:
        dir_type = sub_dir.split(os.sep)[-1]
        if dir_type not in dir_types:
            print 'add', dir_type, 'in dir_types'
            dir_types[dir_type] = 0

        # count the number of files
        num = len(glob.glob(sub_dir+'/*'))
        dir_types[dir_type] += num
        print sub_dir, num

    print 'sum up:', dir_types
