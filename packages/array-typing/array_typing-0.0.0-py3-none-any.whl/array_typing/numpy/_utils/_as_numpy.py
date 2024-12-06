from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np

import array_typing as at


def as_numpy(obj: Any) -> np.ndarray:
    if at.is_numpy(obj):
        return obj
    if at.is_torch(obj):
        return obj.numpy(force=True)
    return np.asarray(obj)


def as_dict_of_numpy(obj: Mapping[str, at.ArrayLike] | None) -> dict[str, np.ndarray]:
    if obj is None:
        return {}
    return {k: at.as_numpy(v) for k, v in obj.items()}
