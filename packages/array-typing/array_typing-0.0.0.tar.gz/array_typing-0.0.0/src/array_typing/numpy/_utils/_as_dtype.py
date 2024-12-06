from __future__ import annotations

import numpy as np
import numpy.typing as npt

import array_typing.numpy as tn


def as_dtype(x: npt.ArrayLike, dtype: npt.DTypeLike) -> npt.NDArray[...]:
    x: npt.NDArray = tn.as_numpy(x)
    dtype: np.dtype = np.dtype(dtype)
    if np.issubdtype(x.dtype, dtype):
        return x
    if np.isdtype(dtype, "bool"):
        if np.ptp(x) > 0:
            return x > np.median(x)
        return x > 0.5
    if np.isdtype(dtype, "integral"):
        x = np.rint(x)
    return x.astype(dtype)
