import numpy as np
from typing import Callable, Union

def getCurveReducer(reducer: Union[str, Callable[[np.ndarray], float]]) -> Callable[[np.ndarray], float]:
    if reducer == 'auc':
        return np.mean

    if reducer == 'end':
        return lambda m: np.mean(m[-int(m.shape[0] * .1):])

    if isinstance(reducer, str):
        raise Exception("Unknown reducer type")

    return reducer
