#!/bin/bash
# Copyright 2021 Huawei Technologies Co., Ltd
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

echo "=============================================================================================================="
echo "Please run the script as: "
echo "bash run.sh DATA_PATH"
echo "For example: bash run.sh /path/dataset 0"
echo "It is better to use the absolute path."
echo "=============================================================================================================="
EXE_PATH=$(pwd)
DATA_PATH=$1
export DEVICE_ID=$2

python train.py  \
    --epochs 25 \
    --train_url "$EXE_PATH" \
    --data_url "$DATA_PATH" \
    --device_target "GPU" \
    --device_num 1 \
    > train.log 2>&1 &
echo "start training"
cd ../
