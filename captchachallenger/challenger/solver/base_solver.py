#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\solver\base_solver.py
# @Time    :   2022-08-10 14:54:24
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0


class BaseSolver(object):
    def __init__(self):
        pass

    def solve(self, challenge, prompt, content):
        raise NotImplementedError()
