import io

import numpy as np


def np_to_bytes(arr: np.ndarray) -> bytes:
    with io.BytesIO() as buf:
        np.save(buf, arr, allow_pickle=False)
        buf.seek(0)
        data = buf.read()
    return data


def np_from_bytes(data: bytes) -> np.ndarray:
    with io.BytesIO(data) as buf:
        arr = np.load(buf, allow_pickle=False)
    return arr
