#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\solver\onnx_runner\base_runner.py
# @Time    :   2022-08-10 18:52:31
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

import os
from typing import Optional
import requests
import cv2


class BaseRunner(object):
    def __init__(self, cfg=None) -> None:
        self.cfg = cfg

    def infer(self, img_stream) -> bool:
        raise NotImplementedError()

    @staticmethod
    def download(model_path: str, model_url: str, force: bool = False):
        """Download the de-stylized binary classification model"""

        if not model_url.lower().startswith("http"):
            raise ValueError from None

        # check file exist
        if os.path.exists(model_path) and not force:
            return

        with requests.get(model_url, stream=True) as response, open(
            model_path, "wb"
        ) as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
