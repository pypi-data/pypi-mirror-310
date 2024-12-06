import array_typing as at


def as_scalar(x: at.ScalarLike) -> at.Scalar:
    if at.is_jax(x):
        return x.item()
    if at.is_numpy(x):
        return x.item()
    if at.is_torch(x):
        return x.item()
    return x  # pyright: ignore [reportReturnType]
