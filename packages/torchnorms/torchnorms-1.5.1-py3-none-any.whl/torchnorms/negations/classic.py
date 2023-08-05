# -*- coding: utf-8 -*-

import torch
from torch import Tensor
from torchnorms.negations.base import BaseNegation


class StandardNegation(BaseNegation):
    def __init__(self) -> None:
        super().__init__()
        self.__name__ = 'standard'

    @classmethod
    def __call__(cls,
                 a: Tensor) -> Tensor:
        return 1.0 - a


class AffineNegation(BaseNegation):
    def __init__(self) -> None:
        super().__init__()
        self.__name__ = 'affine'
        self.linear = torch.nn.Linear(1, 1, bias=True)
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.linear.weight[0, 0].data = torch.tensor(1, device=device)
        self.linear.bias[0].data = torch.tensor(-1,  device=device)

    def __call__(self,
                 a: Tensor) -> Tensor:
        return self.linear(a)


class StrictNegation(BaseNegation):
    def __init__(self) -> None:
        super().__init__()
        self.__name__ = 'strict'

    @classmethod
    def __call__(cls,
                 a: Tensor) -> Tensor:
        return 1.0 - torch.pow(a, 2)


class StrictCosNegation(BaseNegation):
    def __init__(self) -> None:
        super().__init__()
        self.__name__ = 'strict_cosine'

    @classmethod
    def __call__(cls,
                 a: Tensor) -> Tensor:
        pi = torch.acos(torch.zeros(1)).item() * 2
        res = 0.5 * (torch.cos(pi * a))
        return res
