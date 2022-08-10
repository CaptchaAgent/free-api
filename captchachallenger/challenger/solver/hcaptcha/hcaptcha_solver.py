#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\solver\hcaptcha\hcaptcha_solver.py
# @Time    :   2022-08-10 18:08:47
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

import ezkfg as ez
from ..base_solver import BaseSolver
from .model_runner import BinaryRunner, YOLORunner
from .constants import model_cfg


class hCaptchaSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        # switch hcaptcha challenge to solver
        self.challenger_factory = {
            "image_label_binary": self.image_label_binary,
        }
        self.supported_lang = []
        # pre build model runner
        self.model_runner_factory = {}
        for challenge in model_cfg:
            for model in model_cfg[challenge]:
                # build model runner
                runner_ = self.build_model_runner(model)

                for lang in model.lang:
                    # statistics supported lang
                    if lang not in self.supported_lang:
                        self.supported_lang.append(lang)

                    # register model runner
                    for alias in lang:
                        self.model_runner_factory[(challenge, alias)] = runner_

    def solve(self, challenge: str, prompt: str, content, lang: str = "en"):
        # TODO: validate input
        if challenge not in self.challenger_factory:
            raise ValueError(f"unknown challenge: {challenge}")
        return self.challenger_factory[challenge](
            prompt=prompt, content=content, lang=lang
        )

    def image_label_binary(self, prompt: str, content, lang: str = "en"):
        # prompt to label

        # get model runner

        result = []
        for img in content:
            # infer image
            # get label
            pass

        return result

    def build_model_runner(self, model: ez.Config):
        if "yolo" in model.name:
            return YOLORunner(model)
        else:
            return BinaryRunner(model)
