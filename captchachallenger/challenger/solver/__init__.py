#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\solver\__init__.py
# @Time    :   2022-08-10 13:57:57
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0


from .hcaptcha import hCaptchaSolver

solver_factory = {
    "hcaptcha": hCaptchaSolver(),
}


def build_solver(solver_name: str):
    if solver_name not in solver_factory:
        raise ValueError(f"unknown solver: {solver_name}")
    return solver_factory[solver_name]
