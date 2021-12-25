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
""" Export Checkpoint to Model """
import numpy as np
from mindspore import context, Tensor
from mindspore.train.serialization import export, load_checkpoint, load_param_into_net

from eval import KGEModel
from src.rotate import ModelBuilder
from src.dataset import get_entity_and_relation
from src.model_utils.config import config
from src.model_utils.device_adapter import get_device_id
from src.model_utils.moxing_adapter import moxing_wrapper

context.set_context(mode=context.GRAPH_MODE, device_target=config.device_target)
if config.device_target == "Ascend":
    context.set_context(device_id=get_device_id())


def modelarts_process():
    pass


@moxing_wrapper(pre_process=modelarts_process)
def export_rotate():
    """ export_rotate """
    entity2id, relation2id = get_entity_and_relation(config.data_path)
    config.num_entity, config.num_relation = len(entity2id), len(relation2id)

    model_builder = ModelBuilder(config)
    network = model_builder.get_eval_net()
    model_params = load_checkpoint(ckpt_file_name=config.eval_checkpoint)
    load_param_into_net(net=network, parameter_dict=model_params)
    infer_net_head = KGEModel(network=network, mode='head-mode')
    infer_net_tail = KGEModel(network=network, mode='tail-mode')
    infer_net_head.set_train(False)
    infer_net_tail.set_train(False)

    positive_sample = Tensor(np.ones([config.batch_size, 3]).astype(np.int32))
    negative_sample = Tensor(np.ones([config.batch_size, config.negative_sample_size]).astype(np.int32))
    filter_bias = Tensor(np.ones([config.batch_size, 1]).astype(np.float32))

    input_data = [positive_sample, negative_sample, filter_bias]
    export(
        infer_net_head,
        *input_data,
        file_name='{}-head'.format(config.experiment_name),
        file_format=config.file_format
    )
    export(
        infer_net_tail,
        *input_data,
        file_name='{}-tail'.format(config.experiment_name),
        file_format=config.file_format
    )


if __name__ == '__main__':
    export_rotate()