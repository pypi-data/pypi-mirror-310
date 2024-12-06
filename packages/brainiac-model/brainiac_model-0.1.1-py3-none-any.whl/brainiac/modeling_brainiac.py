import torch
import torch.nn as nn
from typing import Optional
from transformers import PreTrainedModel
from .configuration_brainiac import BrainiacConfig
from monai.networks.nets import resnet50

class BrainiacModel(PreTrainedModel):
    config_class = BrainiacConfig
    base_model_prefix = "brainiac"
    
    def __init__(self, config: BrainiacConfig):
        super().__init__(config)
        self.config = config
        
        # Initialize ResNet50 from MONAI
        self.resnet = resnet50(pretrained=False)
        # Modify first conv layer for 3D input
        self.resnet.conv1 = nn.Conv3d(
            config.in_channels, 
            64, 
            kernel_size=7, 
            stride=2, 
            padding=3, 
            bias=False
        )
        # Replace final FC layer with Identity
        self.resnet.fc = nn.Identity()
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.resnet(x)

    def _init_weights(self, module):
        if isinstance(module, nn.Conv3d):
            nn.init.kaiming_normal_(module.weight, mode='fan_out', nonlinearity='relu')
        elif isinstance(module, (nn.BatchNorm3d, nn.GroupNorm)):
            nn.init.constant_(module.weight, 1)
            nn.init.constant_(module.bias, 0)