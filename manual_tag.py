#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------
# @ File       : manual_tag.py
# @ Description:  
# @ Author     : Alex Chung
# @ Contact    : yonganzhong@outlook.com
# @ License    : Copyright (c) 2017-2018
# @ Time       : 2020/4/22 上午10:09
# @ Software   : PyCharm
#-------------------------------------------------------

import os

def content_tag(content, dst_file):
    fa = open(dst_file, mode='a')

    notify_map = {
        'a_begin': 'B-EVA',
        'a_internal': 'I-EVA',
        'b_begin': 'B-TRG',
        'b_internal': 'I-TRG',
        'other': 'O'
    }
    event_flag = False
    trigger_flag = False

    # head flag
    flag_index = 0
    for c in content:
        # modify flag status
        if c in ['A', 'B']:
            if c == 'A':
                event_flag = bool(1 - event_flag)
            elif c == 'B':
                trigger_flag = bool(1 - trigger_flag)
            # update head flag
            flag_index = 0
        else:
            # judge is event or trigger
            if event_flag or trigger_flag:
                if c in [" ", "\n"]:
                    continue
            if event_flag:
                if flag_index == 0:
                    fa.write(c + " " + notify_map['a_begin'] + '\n')
                    flag_index += 1
                else:
                    fa.write(c + " " + notify_map['a_internal'] + '\n')
                    flag_index += 1
            elif trigger_flag:
                if flag_index == 0:
                    fa.write(c + " " + notify_map['b_begin'] + '\n')
                    flag_index += 1
                else:
                    fa.write(c + " " + notify_map['b_internal'] + '\n')
                    flag_index += 1
            # non important char
            else:
                fa.write(c + " " + notify_map['other'] + '\n')
    # assert event_flag is False, "event notify not pair"
    # assert trigger_flag is False, "trigger notify not pair"
    fa.close()


def simple_notify(src_path):
    assert os.path.exists(src_path), "Invalid path"

    file_name = os.path.basename(src_path).split(".")[0]
    dir_name = os.path.dirname(src_path)
    dst_path = os.path.join(dir_name, file_name + '_tag.txt')

    fr = open(src_path, mode='r', encoding='utf8')
    for line in fr.readlines():
        line = line.strip()
        content_tag(line, dst_file=dst_path)