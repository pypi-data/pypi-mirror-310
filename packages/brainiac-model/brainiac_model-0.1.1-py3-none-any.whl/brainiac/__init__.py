from typing import TYPE_CHECKING

from transformers.utils import (
    OptionalDependencyNotAvailable,
    _LazyModule,
    is_torch_available,
)

# Version of the brainiac package
__version__ = "0.1.0"

_import_structure = {
    "configuration_brainiac": ["BrainiacConfig"],
}

try:
    if not is_torch_available():
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    pass
else:
    _import_structure["modeling_brainiac"] = ["BrainiacModel"]

if TYPE_CHECKING:
    from .configuration_brainiac import BrainiacConfig
    from .modeling_brainiac import BrainiacModel

    if is_torch_available():
        from transformers import AutoModel, AutoConfig
        # Register the model architecture
        AutoConfig.register("brainiac", BrainiacConfig)
        AutoModel.register(BrainiacConfig, BrainiacModel)

else:
    import sys
    sys.modules[__name__] = _LazyModule(
        __name__,
        globals()["__file__"],
        _import_structure,
        module_spec=__spec__,
    )
    
    # Register the model architecture
    if is_torch_available():
        from transformers import AutoModel, AutoConfig
        from .configuration_brainiac import BrainiacConfig
        from .modeling_brainiac import BrainiacModel
        
        AutoConfig.register("brainiac", BrainiacConfig)
        AutoModel.register(BrainiacConfig, BrainiacModel)