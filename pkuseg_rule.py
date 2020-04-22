#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------
# @ File       : pkuseg_rule.py
# @ Description:  
# @ Author     : Alex Chung
# @ Contact    : yonganzhong@outlook.com
# @ License    : Copyright (c) 2017-2018
# @ Time       : 2020/4/22 上午10:07
# @ Software   : PyCharm
#-------------------------------------------------------
import os
import re
import pkuseg


file_path = '/home/alex/linewell/weibo_tag/raw_data'

def content_process(content):

    # remove special char
    content = content.replace('\n', '')
    content = content.replace('\t', '')
    content = content.replace("'", '')

    # remove space
    content = re.sub('\s', "", content)
    content = re.sub('\s+', "", content)

    return content



if __name__ == "__main__":

    src_path = os.path.join(file_path, '502.txt')
    dst_path = os.path.join(os.path.curdir, 'data', 'pkuseg_result.txt')
    fr = open(src_path, 'r')

    seg = pkuseg.pkuseg(model_name="web", postag=True)

    # content = []
    # content = fr.read()
    # content = content_process(content)
    # for seg_clip in seg.cut(content):
    #     print(seg_clip)
    contents = []
    for line in fr.readlines():

        # remove space blank
        if len(line.strip()) == 0:
            continue
        line = content_process(line)
        contents.append(line)

    tag_map = {
        'n_begin': 'B-EVA',
        'n_internal': 'I-EVA',
        'v_begin': 'B-TRG',
        'v_internal': 'I-TRG',
        'other': 'O'
    }
    # word tag
    with open(dst_path, 'w', encoding='utf8') as fw:
        for content in contents:
            for seg_clip in seg.cut(content):
                words, tag = seg_clip[0], seg_clip[1]
                word_status = 'o'
                for word in words:
                    print(words, len(words))
                    if tag in ['nz', 'ns', 'n'] and len(words) > 1:
                        if word_status in ['IT', 'o']:
                            fw.write(word + '\t' + tag_map['n_begin'] + '\t' + tag + '\n')
                            word_status = 'BE'
                        else:
                            fw.write(word + '\t' + tag_map['n_internal'] + '\t' + tag + '\n')
                            word_status = 'IE'
                    elif tag in ['v', 'vn'] and len(words) > 1:
                        if word_status in ['IE', 'o']:
                            fw.write(word + '\t' + tag_map['v_begin'] + '\t' + tag + '\n')
                            word_status = 'BT'
                        else:
                            fw.write(word + '\t' + tag_map['v_internal'] + '\t' + tag + '\n')
                            word_status = 'IT'
                    else:
                        fw.write(word + '\t' + tag_map['other'] + '\t' +  tag + '\n')
