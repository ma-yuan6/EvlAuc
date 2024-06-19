#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/6/14 11:40
# @Author   : MJX
# @Describe : 封装一些常用的工具函数

import pandas as pd
from sklearn.metrics import roc_auc_score, accuracy_score


class ColumnNotFoundException(Exception):
    """
    自定义异常: 如果上传的csv文件没有prob列或label列则抛出异常
    """

    def __init__(self, e):
        super().__init__(e)


ans_df = pd.read_csv('test_label.csv')


def cal_score(test_df):
    """
    计算AUC分数
    :return: AUC分数、准确率
    """
    if 'prob' not in test_df.columns:
        raise ColumnNotFoundException('不存在 prob 列')
    elif 'label' not in test_df.columns:
        raise ColumnNotFoundException('不存在 label 列')
    dfm = pd.merge(ans_df, test_df, on=['user_id', 'merchant_id'], how='inner')  # 合并上传的数据和给的答案
    return roc_auc_score(dfm['label_real'], dfm['prob']), accuracy_score(dfm['label_real'], dfm['label'])
