#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    :   captchachallenger\challenger\solver\hcaptcha\model_runner\yolo_runner.py
# @Time    :   2022-08-10 18:15:55
# @Author  :   Bingjie Yan
# @Email   :   bj.yan.pa@qq.com
# @License :   Apache License 2.0

import os
from typing import Optional, Union
import cv2
import numpy as np
from ..constants import special_image_size_gallery, model_url_prefix, model_path
from ...onnx_runner.base_runner import BaseRunner


class YOLORunner(BaseRunner):
    classes = [
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "backpack",
        "umbrella",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "dining table",
        "toilet",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush",
    ]

    def __init__(self, cfg=None) -> None:
        super().__init__(cfg)

        self.model_path = os.path.join(model_path, f"{self.cfg.get('name')}.onnx")
        self.model_url = f"{model_url_prefix}/{self.cfg.get('name')}.onnx"
        print(f"Downloading {self.model_path} from {self.model_url}")
        self.download(self.model_path, self.model_url)

        self.net = cv2.dnn.readNetFromONNX(self.model_path)

        self.image_size = self.cfg.get("size", (128, 128))

    def infer(
        self, img_stream, label: str, confidence: float = 0.4, nms_thresh: float = 0.4
    ) -> bool:
        img_arr = np.frombuffer(img_stream, np.uint8)
        img = cv2.imdecode(img_arr, flags=1)
        height, width, _ = img.shape

        class_ids = []
        confidences = []
        boxes = []

        # fixme: dup-code
        if img.shape[0] == special_image_size_gallery.WATERMARK:
            img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

        img = cv2.resize(img, self.image_size)
        blob = cv2.dnn.blobFromImage(
            img, 1 / 255.0, self.image_size, (0, 0, 0), swapRB=True, crop=False
        )

        self.net.setInput(blob)
        outs = self.net.forward()

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                max_conf = scores[class_id]
                if max_conf > confidence:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - (w / 2)
                    y = center_y - (h / 2)
                    class_ids.append(class_id)
                    confidences.append(float(max_conf))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence, nms_thresh)

        labels = [str(self.classes[class_ids[i]]) for i in indices]
        return bool(label in labels)
