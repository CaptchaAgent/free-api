#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\constants.py
# @Time    :   2022-08-10 14:08:17
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0


import os
import ezkfg as ez
import yaml


model_url_prefix = (
    "https://github.com/QIN2DIM/hcaptcha-challenger/releases/download/model"
)
model_path = os.path.join(os.path.dirname(__file__), "model", "hcaptcha")
os.makedirs(model_path, exist_ok=True)


class special_image_size_gallery(object):
    WATERMARK = 100
    GENERAL = 128
    GAN = 144


class model_infer_image_size(object):
    IMAGE_LABEL_BINARY = (64, 64)


model_cfg = ez.Config(
    **yaml.load(
        open(
            os.path.join(os.path.dirname(__file__), "model_cfg.yaml"), encoding="utf-8"
        ),
        Loader=yaml.FullLoader,
    )
)

print(model_cfg)

bad_code = {
    "а": "a",
    "е": "e",
    "e": "e",
    "i": "i",
    "і": "i",
    "ο": "o",
    "с": "c",
    "ԁ": "d",
    "ѕ": "s",
    "һ": "h",
    "ー": "一",
    "土": "士",
}
