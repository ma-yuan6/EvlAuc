#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/6/14 9:58
# @Author   : MJX
# @Describe : 天猫用户复购模型效果评估

import pandas as pd
import streamlit as st
from utils import cal_score, ColumnNotFoundException
from sou import instructions, data


@st.cache_data
def convert_df():
    df = pd.DataFrame(data, columns=['user_id', 'merchant_id', 'label_real'])
    del df['label_real']
    return df.to_csv(index=False).encode("utf-8")


st.title('天猫用户复购模型评估')

with st.expander('食用方法😋'):
    st.markdown(instructions)

csv = convert_df()
st.download_button(
    label='点击下载测试集',
    data=csv,
    file_name='test.csv',
    mime='xlsx/csv',
)

uploaded_file = st.file_uploader('上传文件')

if st.button('提交'):
    if uploaded_file:
        if not uploaded_file.name.endswith('.csv'):
            st.warning('请上传.csv')
            st.stop()
    else:
        st.warning('请先上传文件')
        st.stop()
    auc, acc = 0, 0
    try:
        auc, acc = cal_score(pd.read_csv(uploaded_file))
    except ColumnNotFoundException as e:
        st.error(e)
        st.stop()
    col1, col2 = st.columns(2)
    col1.metric('准确率', f'{acc * 100:.2f}%')
    col2.metric('auc值', f'{auc * 100:.2f}%')
    st.toast('评估成功！')
