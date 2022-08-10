#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\solver\onnx_runner\base_runner.py
# @Time    :   2022-08-10 14:47:10
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

import cv2


class BaseRunner(object):
    def __init__(self, model_path: str) -> None:
        self.net = cv2.dnn.readNetFromONNX(model_path)

    def infer(self, image) -> bool:
        raise NotImplementedError()
