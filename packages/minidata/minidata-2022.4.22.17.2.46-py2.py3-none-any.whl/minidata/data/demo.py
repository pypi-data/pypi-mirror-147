#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : minidata.
# @File         : demo
# @Time         : 2022/4/22 下午4:34
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *



# joblib.dump(df, '同花顺相似问.pkl')


print(joblib.load('同花顺相似问.pkl'))
