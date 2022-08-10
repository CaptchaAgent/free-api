#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\solver\hcaptcha\hcaptcha_solver.py
# @Time    :   2022-08-10 18:08:47
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

import ezkfg as ez
import re
from ..base_solver import BaseSolver
from .model_runner import BinaryRunner, YOLORunner
from .constants import model_cfg, bad_code


class hCaptchaSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        # switch hcaptcha challenge to solver
        self.challenger_factory = {
            "image_label_binary": self.image_label_binary,
        }
        # pre build model runner
        self.model_runner_factory = {}
        self.label_alias = {
            "zh": {
                "自行车": "bicycle",
                "火车": "train",
                "卡车": "truck",
                "公交车": "bus",
                "巴士": "bus",
                "飞机": "airplane",
                "一条船": "boat",
                "船": "boat",
                "摩托车": "motorcycle",
                "垂直河流": "vertical river",
                "天空中向左飞行的飞机": "airplane in the sky flying left",
                "请选择天空中所有向右飞行的飞机": "airplanes in the sky that are flying to the right",
                "汽车": "car",
                "大象": "elephant",
                "鸟": "bird",
                "狗": "dog",
            },
            "en": {
                "airplane": "airplane",
                "motorbus": "bus",
                "bus": "bus",
                "truck": "truck",
                "motorcycle": "motorcycle",
                "boat": "boat",
                "bicycle": "bicycle",
                "train": "train",
                "vertical river": "vertical river",
                "airplane in the sky flying left": "airplane in the sky flying left",
                "Please select all airplanes in the sky that are flying to the right": "airplanes in the sky that are flying to the right",
                "car": "car",
                "elephant": "elephant",
                "bird": "bird",
                "dog": "dog",
            },
        }

        self.supported_lang = []

        # special processing for yolo runner

        # build model runner binary runner

        for challenge in model_cfg:
            if challenge.startswith("__"):
                continue
            if challenge not in self.model_runner_factory:
                self.model_runner_factory[challenge] = {}
            print(f"building {challenge} model runner")
            # print(f"model_cfg[challenge]: {model_cfg[challenge]}")
            for model in model_cfg[challenge]:
                # build model runner
                print(f"building {model} runner")
                runner_ = self.build_model_runner(model)

                for lang in model.lang:
                    if lang.startswith("__"):
                        continue
                    # statistics supported lang
                    if lang not in self.supported_lang:
                        self.supported_lang.append(lang)
                    if lang not in self.model_runner_factory[challenge]:
                        self.model_runner_factory[challenge][lang] = {}

                    # register model runner
                    for alias in model.lang[lang]:
                        if alias.startswith("__"):
                            continue
                        self.model_runner_factory[challenge][lang][alias] = runner_
                        self.label_alias[lang][alias] = model.name

        print("init hcaptcha solver done")
        print(f"supported lang: {self.supported_lang}")
        print(f"label alias: {self.label_alias}")
        print(f"model runner factory: {self.model_runner_factory}")
        print(f"challenger factory: {self.challenger_factory}")

    def solve(self, challenge: str, prompt: str, content, lang: str = "en"):
        if challenge not in self.challenger_factory:
            raise ValueError(
                f"unknown challenge: {challenge}, supported: {self.challenger_factory.keys()}"
            )

        if lang not in self.supported_lang:
            raise ValueError(
                f"unsupported lang: {lang}, supported: {self.supported_lang}"
            )

        return self.challenger_factory[challenge](
            prompt=prompt, content=content, lang=lang
        )

    def image_label_binary(self, prompt: str, content, lang: str = "en"):
        # prompt to label
        label = self.get_label(prompt, lang)

        # get model runner
        runner = self.model_runner_factory["image_label_binary"][lang][label]

        result = []
        for img in content:
            # infer image
            result_ = runner.infer(img.read())
            # append result
            result.append(result_)

        return result

    def build_model_runner(self, model: ez.Config):
        if "yolo" in model.name:
            return YOLORunner(model)
        else:
            return BinaryRunner(model)

    @staticmethod
    def label_cleaning(raw_label: str) -> str:
        clean_label = raw_label
        for c in bad_code:
            clean_label = clean_label.replace(c, bad_code[c])
        return clean_label

    @staticmethod
    def split_prompt_message(prompt: str, lang: str = "en") -> str:
        labels_mirror = {
            "zh": re.split(r"[包含 图片]", prompt)[2][:-1] if "包含" in prompt else prompt,
            "en": re.split(r"containing a", prompt)[-1][1:].strip().replace(".", "")
            if "containing" in prompt
            else prompt,
        }
        return labels_mirror[lang]

    def get_label(self, prompt: str, lang: str = "en"):
        label = self.split_prompt_message(prompt, lang)
        return self.label_cleaning(label)
