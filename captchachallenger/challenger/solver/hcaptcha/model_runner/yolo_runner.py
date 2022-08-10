#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\solver\hcaptcha\model_runner\yolo_runner.py
# @Time    :   2022-08-10 18:15:55
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

from ...onnx_runner.base_runner import BaseRunner


class YOLORunner(BaseRunner):
    def __init__(self, cfg=None):
        super().__init__(cfg)
