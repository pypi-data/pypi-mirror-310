from __future__ import annotations

import numpy as np
import numpy.typing as npt

import array_typing.numpy as tn


def scale(x: npt.ArrayLike, a: float = 0, b: float = 1) -> npt.NDArray:
    x: npt.NDArray[...] = tn.as_numpy(x)
    x = (x - x.min()) / np.ptp(x)
    x = x * (b - a) + a
    return x
