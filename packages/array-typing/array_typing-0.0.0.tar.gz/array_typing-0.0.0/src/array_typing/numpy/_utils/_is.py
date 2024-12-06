from __future__ import annotations

from typing import Any, TypeGuard

import numpy as np

import array_typing as at


def is_numpy(obj: Any) -> TypeGuard[np.ndarray]:
    return at.is_instance_named_partial(obj, "numpy.ndarray")
