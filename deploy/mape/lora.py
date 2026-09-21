"""Low-rank adapters for the fp32 decision head. The INT8 encoder stays frozen."""
import torch
import torch.nn as nn
import torch.nn.functional as F


class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, rank=8, alpha=16):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad = False
        self.A = nn.Parameter(torch.randn(rank, base.in_features) * 0.01)
        self.B = nn.Parameter(torch.zeros(base.out_features, rank))
        self.scale = alpha / rank

    def forward(self, x):
        return self.base(x) + F.linear(F.linear(x, self.A), self.B) * self.scale

    def merge(self):
        with torch.no_grad():
            self.base.weight.add_(self.scale * (self.B @ self.A))
        return self.base


def _swap(module, rank):
    for name, child in list(module.named_children()):
        if isinstance(child, nn.Linear):
            setattr(module, name, LoRALinear(child, rank=rank))
        else:
            _swap(child, rank)


def inject(model, rank=8):
    """Adapt the decision head only. Encoder weights are quantized and not trainable."""
    for part in (model.head, model.scorer, model.act_head):
        if part is not None:
            _swap(part, rank)
    if hasattr(torch.backends, "mha"):
        torch.backends.mha.set_fastpath_enabled(False)
    return [p for p in model.parameters() if p.requires_grad]


def _merge_into(module):
    for name, child in list(module.named_children()):
        if isinstance(child, LoRALinear):
            setattr(module, name, child.merge())
        else:
            _merge_into(child)


def merge(model):
    for part in (model.head, model.scorer, model.act_head):
        if part is not None:
            _merge_into(part)
    if hasattr(torch.backends, "mha"):
        torch.backends.mha.set_fastpath_enabled(True)
