#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------
# @ File       : thulac_rule.py
# @ Description:  
# @ Author     : Alex Chung
# @ Contact    : yonganzhong@outlook.com
# @ License    : Copyright (c) 2017-2018
# @ Time       : 2020/4/22 上午10:11
# @ Software   : PyCharm
#-------------------------------------------------------
import os
import re
import thulac
import pathlib


tag_map = {
            'n_begin': 'B-EVA',
            'n_internal': 'I-EVA',
            'v_begin': 'B-TRG',
            'v_internal': 'I-TRG',
            'other': 'O'
        }

def content_process(content):

    # remove special char
    content = content.replace('\n', '')
    content = content.replace('\t', '')
    content = content.replace("'", '')

    # remove space
    content = re.sub('\s', "", content)
    content = re.sub('\s+', "", content)

    return content


def file_tag(src_dir, dst_dir, user_dict_path):
    src_dir = pathlib.Path(src_dir)
    dst_dir = pathlib.Path(dst_dir)

    seg = thulac.thulac(user_dict=user_dict_path)

    for src_file in src_dir.glob('*.txt'):
        assert src_file.is_file(), "Not found {0}".format(src_file)

        tag_path = pathlib.Path(dst_dir / src_file.name)

        # read file and process
        fr = src_file.open(mode='r')
        contents = []
        for line in fr.readlines():

            # remove space blank
            if len(line.strip()) == 0:
                continue
            line = content_process(line)
            contents.append(line)

        # word tag
        with tag_path.open('w') as fw:
            for content in contents:
                for seg_clip in seg.cut(content):
                    words, tag = seg_clip[0], seg_clip[1]
                    word_status = 'o'
                    for word in words:
                        print(words, len(words))
                        # filter url
                        if tag in ['nz', 'ns', 'n', 'ni', 'uw'] and len(words) > 1 and len(words)< 10:
                            if word_status in ['IT', 'o']:
                                fw.write(word + ' ' + tag_map['n_begin'] + '\n')
                                word_status = 'BE'
                            else:
                                fw.write(word + ' ' + tag_map['n_internal'] + '\n')
                                word_status = 'IE'
                        elif tag in ['v', 'vn'] and len(words) > 1 and len(words)< 10:
                            if word_status in ['IE', 'o']:
                                fw.write(word + ' ' + tag_map['v_begin'] + '\n')
                                word_status = 'BT'
                            else:
                                fw.write(word + ' ' + tag_map['v_internal'] + '\n')
                                word_status = 'IT'
                        else:
                            fw.write(word + ' ' + tag_map['other'] + '\n')


if __name__ == "__main__":

    # src_path = os.path.join(file_path, '990.txt')
    # dst_path = os.path.join(os.path.curdir, 'data', 'thulac_result.txt')


    src_dir = '/home/alex/linewell/weibo_tag/raw_data'
    dst_dir = '/home/alex/linewell/weibo_tag/tag_data'
    user_dict_path = os.path.join(os.path.curdir, 'data', 'thulac_user_dict.txt')
    file_tag(src_dir, dst_dir, user_dict_path)