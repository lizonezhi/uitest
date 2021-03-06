#!/usr/bin/env python
# coding=utf-8

class ListUtil:

    def strip(self, org_list):
        '''
        去掉list里的换行符和空格元素
        '''
        result_list = []
        for i in org_list:
            if i != '':
                i = i.strip()
                if i != '':
                    result_list.append(i)
        return result_list