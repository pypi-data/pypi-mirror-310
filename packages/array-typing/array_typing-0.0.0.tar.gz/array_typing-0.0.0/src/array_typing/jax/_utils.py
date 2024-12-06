from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeGuard

import array_typing as at

if TYPE_CHECKING:
    import jax


def is_jax(obj: Any) -> TypeGuard[jax.Array]:
    return at.is_instance_named_partial(obj, "jax.Array")
