import re

import torch


# load checkpoint
def load_checkpoint(model, checkpoint_path):
    """
    function to load pretrained TCN model for continue training or evaluation
    :param model:
    :param checkpoint_path:
    :return:
    """
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint)
    match = re.search(r'_epoch(\d+).pth', checkpoint_path)
    if match:
        epoch_num = int(match.group(1))
        return model, checkpoint, epoch_num
    else:
        return model, checkpoint, None
