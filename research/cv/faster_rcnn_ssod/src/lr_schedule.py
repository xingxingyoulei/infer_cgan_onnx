# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""lr generator for fasterrcnn"""

import math
from bisect import bisect_right


def linear_warmup_learning_rate(current_step, warmup_steps, base_lr, init_lr):
    lr_inc = (float(base_lr) - float(init_lr)) / float(warmup_steps)
    learning_rate = float(init_lr) + lr_inc * current_step
    return learning_rate


def a_cosine_learning_rate(current_step, base_lr, warmup_steps, decay_steps):
    base = float(current_step - warmup_steps) / float(decay_steps)
    learning_rate = (1 + math.cos(base * math.pi)) / 2 * base_lr
    return learning_rate


def dynamic_lr(config):
    """dynamic learning rate generator"""
    base_lr = config.base_lr
    total_steps = int(config.max_iter)
    warmup_steps = int(config.warmup_step)
    lr = []
    for i in range(total_steps):
        if i < warmup_steps:
            lr.append(linear_warmup_learning_rate(i, warmup_steps, base_lr, base_lr * config.warmup_ratio))
        else:
            lr.append(a_cosine_learning_rate(i, base_lr, warmup_steps, total_steps))

    return lr


def multi_step_learning_rate(current_step, milestones, base_lr, gamma):
    learning_rate = base_lr * gamma ** bisect_right(milestones, current_step)
    return learning_rate


def warmup_multi_step_lr(cfg):
    max_steps = int(cfg.max_iter)
    warmup_steps = int(cfg.warmup_step)
    milestones = cfg.milestones
    base_lr = cfg.base_lr
    gamma = cfg.gamma
    warmup_ratio = cfg.warmup_ratio

    if not list(milestones) == sorted(milestones):
        raise ValueError("Milestones should be a list of increasing integers. Got {}".format(milestones))

    lr = []
    for i in range(max_steps):
        if i < warmup_steps:
            lr.append(linear_warmup_learning_rate(i, warmup_steps, base_lr, base_lr * warmup_ratio))
        else:
            lr.append(multi_step_learning_rate(i, milestones, base_lr, gamma))

    return lr
