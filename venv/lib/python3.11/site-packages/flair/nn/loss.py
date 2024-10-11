from typing import Optional

import torch
from torch import Tensor
from torch.nn import NLLLoss, Sigmoid
from torch.nn.modules.loss import _WeightedLoss


class SigmoidLoss(_WeightedLoss):
    def __init__(
        self, weight: Optional[Tensor] = None, size_average=None, reduce=None, reduction: str = "mean"
    ) -> None:
        super().__init__(weight, size_average, reduce, reduction)

        self.nll_loss = NLLLoss()
        self.sigmoid = Sigmoid()

    def forward(self, input: Tensor, target: Tensor) -> Tensor:
        log_sigmoided_logits = torch.log(self.sigmoid(input))

        return self.nll_loss(log_sigmoided_logits, target)
