#!/bin/bash
# Copyright 2020 Huawei Technologies Co., Ltd
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

if [ $# != 3 ] && [ $# != 4 ]
then 
    echo "Usage: bash run_standalone_train.sh [cifar10|imagenet2012] [DATASET_PATH] [DEVICE_ID] [PRETRAINED_CKPT_PATH](optional)"
exit 1
fi

if [ $1 != "cifar10" ] && [ $1 != "imagenet2012" ]
then 
    echo "error: the selected dataset is neither cifar10 nor imagenet2012"
exit 1
fi

get_real_path(){
  if [ "${1:0:1}" == "/" ]; then
    echo "$1"
  else
    echo "$(realpath -m $PWD/$1)"
  fi
}

PATH1=$(get_real_path $2)
if [ ! -d $PATH1 ]
then 
    echo "error: DATASET_PATH=$PATH1 is not a directory"
exit 1
fi

if [ $# == 4 ]
then
    PATH2=$(get_real_path $4)
    if [ ! -f $PATH2 ]
    then
        echo "error: PRETRAINED_CKPT_PATH=$PATH2 is not a file"
        exit 1
    fi
fi

ulimit -u unlimited
export DEVICE_NUM=1
export DEVICE_ID=$3
export RANK_ID=0
export RANK_SIZE=1

BASE_PATH=$(cd ./"`dirname $0`" || exit; pwd)
if [ $# -ge 1 ]; then
  if [ $1 == 'cifar10' ]; then
    CONFIG_FILE="${BASE_PATH}/../default_config.yaml"
  elif [ $1 == 'imagenet2012' ]; then
    CONFIG_FILE="${BASE_PATH}/../default_config_imagenet.yaml"
  else
    echo "Unrecognized parameter"
    exit 1
  fi
else
  CONFIG_FILE="${BASE_PATH}/../default_config.yaml"
fi

if [ -d "train" ];
then
    rm -rf ./train
fi
mkdir ./train
cp ../*.py ./train
cp ../*.yaml ./train
cp *.sh ./train
cp -r ../src ./train
cd ./train || exit
echo "start training for device $DEVICE_ID"
env > env.log
if [ $# == 3 ]
then
    python train.py --config_path=$CONFIG_FILE --dataset=$1 --dataset_path=$PATH1 &> log.txt &
fi

if [ $# == 4 ]
then
    python train.py --config_path=$CONFIG_FILE --dataset=$1 --dataset_path=$PATH1 --pre_trained=$PATH2 &> log.txt &
fi
cd ..
