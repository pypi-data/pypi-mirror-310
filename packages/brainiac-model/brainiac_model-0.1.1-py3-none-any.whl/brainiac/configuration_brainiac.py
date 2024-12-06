from transformers import PretrainedConfig

class BrainiacConfig(PretrainedConfig):
    model_type = "brainiac"
    
    def __init__(
        self,
        in_channels: int = 1,
        out_features: int = 2048,
        **kwargs
    ):
        self.in_channels = in_channels
        self.out_features = out_features
        super().__init__(**kwargs)

    @classmethod
    def get_config_dict(cls, pretrained_model_name_or_path: str, **kwargs):
        config_dict = super().get_config_dict(pretrained_model_name_or_path, **kwargs)
        config_dict["model_type"] = "brainiac"
        return config_dict