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

    def distinct(self, org_list):
        '''
        list去重
        '''
        result_list = []
        for i in org_list:
            if i not in result_list:
                result_list.append(i)
        return result_list

    def is_same(self, one_list, two_list):
        '''
        比较两个list拼接后是否相同
        '''
        one_list_str = ''.join(one_list).replace(' ', '').upper()
        two_list_str = ''.join(two_list).replace(' ', '').upper()
        if one_list_str != two_list_str:
            return False
        return True