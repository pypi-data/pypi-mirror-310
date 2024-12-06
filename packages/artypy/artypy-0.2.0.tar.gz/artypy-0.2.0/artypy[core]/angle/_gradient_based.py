import numpy as np
from math import degrees, atan2


def gradient_truth(gradientX: np.ndarray, gradientY: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    h, w = gradientX.shape
    res = np.zeros_like(gradientX)
    n = kernel_size
    for y in range(h):
        for x in range(w):
            dx = gradientX[max(0, y - n // 2):y + (n + 1) // 2, max(0, x - n // 2):x + (n + 1) // 2 - 1].sum()
            dy = gradientY[max(0, y - n // 2):y + (n + 1) // 2 - 1, max(0, x - n // 2):x + (n + 1) // 2].sum()
            res[y, x] = -degrees(atan2(dy, dx)) % 180
    return res
