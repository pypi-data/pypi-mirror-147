from einops.layers.torch import Rearrange
from torch import nn
from torch.nn.modules.utils import _pair

from .layers import PermutatorBlock

__all__ = ['ViPS14', 'ViPS7', 'ViPM7', 'ViPL7']


class BasicLayer(nn.Module):
    def __init__(self, dim, input_resolution, depth, segment, mlp_ratio=3., drop=0., patch_merging=False):
        super().__init__()
        self.blocks = nn.ModuleList([PermutatorBlock(dim=dim, input_resolution=input_resolution, segment=segment,
                                                     mlp_dim=dim * mlp_ratio, drop=drop) for _ in range(depth)])

        if patch_merging:
            self.patch_merging = nn.Sequential(
                Rearrange('b (h hs w ws) c -> b (h w) (ws hs c)', hs=2, ws=2, h=input_resolution[0] // 2),
                nn.LayerNorm(4 * dim),
                nn.Linear(4 * dim, 2 * dim, bias=False))
        else:
            self.patch_merging = None

    def forward(self, x):
        for blk in self.blocks:
            x = blk(x)
        if self.patch_merging is not None:
            x = self.patch_merging(x)
        return x


class Permutator(nn.Module):
    """Vision Permutator.
    A PyTorch implement of : `Vision Permutator: A Permutable MLP-Like Architecture for Visual Recognition
    <https://arxiv.org/abs/2106.12368>`_"""

    def __init__(self, *, image_size, channels=3, patch_size, dim, depths, mlp_ratio=3, segments, drop=0., num_classes,
                 **kwargs):
        super().__init__()
        image_height, image_width = _pair(image_size)
        patch_height, patch_width = _pair(patch_size)

        assert image_height % patch_height == 0 and image_width % patch_width == 0, \
            'Image size must be divisible by patch size!'

        patches_resolution = (image_height // patch_height, image_width // patch_width)
        patch_dim = channels * patch_height * patch_width

        self.patch_embedding = nn.Sequential(
            Rearrange('b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=patch_height, p2=patch_width),
            nn.Linear(patch_dim, dim))

        self.drop = nn.Dropout(drop)
        num_layers = len(depths)
        dims = [dim * 2 ** i for i in range(num_layers)]
        input_resolutions = [(patches_resolution[0] // 2 ** i, patches_resolution[1] // 2 ** i) for i in
                             range(num_layers)]
        patch_mergings = [True if i < num_layers - 1 else False for i in range(num_layers)]

        # build layers
        self.layers = nn.ModuleList()
        for dim, input_resolution, depth, segment, patch_merging in \
                zip(dims, input_resolutions, depths, segments, patch_mergings):
            self.layers.append(BasicLayer(dim=dim, input_resolution=input_resolution, depth=depth, segment=segment,
                                          mlp_ratio=mlp_ratio, drop=drop, patch_merging=patch_merging))

        self.mlp_head = nn.Sequential(nn.LayerNorm(dims[-1]), nn.Linear(dims[-1], num_classes))

    def forward(self, x):
        x = self.patch_embedding(x)
        x = self.drop(x)

        for layer in self.layers:
            x = layer(x)

        x = x.mean(dim=1)
        return self.mlp_head(x)


def vip_params(model_name):
    params_dict = {
        'vip-s14': {'patch_size': 14, 'depths': (18,), 'dim': 384, 'segments': (24,)},
        'vip-s7': {'patch_size': 7, 'depths': (4, 14), 'dim': 192, 'segments': (6, 24)},
        'vip-m7': {'patch_size': 7, 'depths': (7, 17), 'dim': 256, 'segments': (8, 32)},
        'vip-l7': {'patch_size': 7, 'depths': (8, 28), 'dim': 256, 'segments': (8, 32)},
    }
    return params_dict[model_name]


class ViPS14(Permutator):
    def __init__(self, **kwargs):
        super().__init__(**{**vip_params('vip-s14'), **kwargs})


class ViPS7(Permutator):
    def __init__(self, **kwargs):
        super().__init__(**{**vip_params('vip-s7'), **kwargs})


class ViPM7(Permutator):
    def __init__(self, **kwargs):
        super().__init__(**{**vip_params('vip-m7'), **kwargs})


class ViPL7(Permutator):
    def __init__(self, **kwargs):
        super().__init__(**{**vip_params('vip-l7'), **kwargs})
