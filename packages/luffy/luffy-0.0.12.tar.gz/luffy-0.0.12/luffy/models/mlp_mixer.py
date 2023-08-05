from einops.layers.torch import Rearrange
from torch import nn
from torch.nn.modules.utils import _pair

from .layers import MLPMixerBlock

__all__ = ['MixerS32', 'MixerS16', 'MixerB32', 'MixerB16', 'MixerL32', 'MixerL16', 'MixerH14']


class MLPMixer(nn.Module):
    """MLP-Mixer.
    A PyTorch implement of : `MLP-Mixer: An all-MLP Architecture for Vision
    <https://arxiv.org/abs/2105.01601>`_"""

    def __init__(self, *, image_size, channels=3, patch_size, dim, depth, mlp_ratio1=0.5, mlp_ratio2=4, drop=0.,
                 num_classes, **kwargs):
        super().__init__()
        image_height, image_width = _pair(image_size)
        patch_height, patch_width = _pair(patch_size)

        assert image_height % patch_height == 0 and image_width % patch_width == 0, \
            'Image size must be divisible by patch size!'

        seq_length = (image_height // patch_height) * (image_width // patch_width)
        patch_dim = channels * patch_height * patch_width

        self.patch_embedding = nn.Sequential(
            Rearrange('b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=patch_height, p2=patch_width),
            nn.Linear(patch_dim, dim))

        self.drop = nn.Dropout(drop)

        self.blocks = nn.ModuleList(
            [MLPMixerBlock(dim, seq_length, int(dim * mlp_ratio1), int(dim * mlp_ratio2), drop) for _ in range(depth)])

        self.mlp_head = nn.Sequential(nn.LayerNorm(dim), nn.Linear(dim, num_classes))

    def forward(self, img):
        x = self.patch_embedding(img)
        x = self.drop(x)

        for blk in self.blocks:
            x = blk(x)
        x = x.mean(dim=1)

        return self.mlp_head(x)


def mixer_params(model_name):
    params_dict = {
        'mixer-s32': {'patch_size': 32, 'depth': 8, 'dim': 512},
        'mixer-s16': {'patch_size': 16, 'depth': 8, 'dim': 512},
        'mixer-b32': {'patch_size': 32, 'depth': 12, 'dim': 768},
        'mixer-b16': {'patch_size': 16, 'depth': 12, 'dim': 768},
        'mixer-l32': {'patch_size': 32, 'depth': 24, 'dim': 1024},
        'mixer-l16': {'patch_size': 16, 'depth': 24, 'dim': 1024},
        'mixer-h14': {'patch_size': 14, 'depth': 32, 'dim': 1280}
    }
    return params_dict[model_name]


class MixerS32(MLPMixer):
    def __init__(self, **kwargs):
        super().__init__(**{**mixer_params('mixer-s32'), **kwargs})


class MixerS16(MLPMixer):
    def __init__(self, **kwargs):
        super().__init__(**{**mixer_params('mixer-s16'), **kwargs})


class MixerB32(MLPMixer):
    def __init__(self, **kwargs):
        super().__init__(**{**mixer_params('mixer-b32'), **kwargs})


class MixerB16(MLPMixer):
    def __init__(self, **kwargs):
        super().__init__(**{**mixer_params('mixer-b16'), **kwargs})


class MixerL32(MLPMixer):
    def __init__(self, **kwargs):
        super().__init__(**{**mixer_params('mixer-l32'), **kwargs})


class MixerL16(MLPMixer):
    def __init__(self, **kwargs):
        super().__init__(**{**mixer_params('mixer-l16'), **kwargs})


class MixerH14(MLPMixer):
    def __init__(self, **kwargs):
        super().__init__(**{**mixer_params('mixer-h14'), **kwargs})
