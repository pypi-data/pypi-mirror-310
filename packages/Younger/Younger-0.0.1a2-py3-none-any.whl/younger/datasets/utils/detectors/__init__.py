#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2024-04-12 10:28
#
# This source code is licensed under the Apache-2.0 license found in the
# LICENSE file in the root directory of this source tree.


from younger.datasets.utils.detectors.langs import detect_natural_langs, detect_program_langs
from younger.datasets.utils.detectors.tasks import detect_task
from younger.datasets.utils.detectors.datasets import detect_dataset_name, detect_dataset_split
from younger.datasets.utils.detectors.metrics import detect_metric_name, normalize_metric_value