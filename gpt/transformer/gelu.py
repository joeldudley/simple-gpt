import math

import torch
import torch.nn as nn
from torch import Tensor


class GaussianErrorLinearUnit(nn.Module):
    @staticmethod
    def forward(x: Tensor) -> Tensor:
        return 0.5 * x * (1.0 + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * torch.pow(x, 3.0))))
