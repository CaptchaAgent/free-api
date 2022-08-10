#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\solver\onnx_runner\binary_runner.py
# @Time    :   2022-08-10 15:15:52
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

import os
from typing import Optional, Union
import cv2
import numpy as np
from ..constants import special_image_size_gallery, model_url_prefix, model_path
from ...onnx_runner.base_runner import BaseRunner


class BinaryRunner(BaseRunner):
    def __init__(self, cfg=None) -> None:
        super().__init__(cfg)

        self.model_path = os.path.join(model_path, f"{self.cfg.get('name')}.onnx")
        self.model_url = f"{model_url_prefix}/{self.cfg.get('name')}.onnx"
        print(f"Downloading {self.model_path} from {self.model_url}")
        self.download(self.model_path, self.model_url)

        self.net = cv2.dnn.readNetFromONNX(self.model_path)

        self.image_size = self.cfg.get("size", (64, 64))

    def infer(self, img_stream, label: int = 0) -> bool:
        img_arr = np.frombuffer(img_stream, np.uint8)
        img = cv2.imdecode(img_arr, flags=1)

        # fixme: dup-code
        if img.shape[0] == special_image_size_gallery.WATERMARK:
            img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

        img = cv2.resize(img, self.image_size)
        blob = cv2.dnn.blobFromImage(
            img, 1 / 255.0, self.image_size, (0, 0, 0), swapRB=True, crop=False
        )

        self.net.setInput(blob)
        out = self.net.forward()

        if not np.argmax(out, axis=1)[label]:
            return True
        return False
