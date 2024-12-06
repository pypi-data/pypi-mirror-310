import arty.core as core
import numpy as np
from arty.core.edge.gradient import Gradient

def lines(image: np.ndarray, to_blur: bool = False, to_noise: bool = False) -> np.ndarray:
    """
    Apply lines filter to the image, method is based on gradient and algorithmic edge detection approach.
    :param image: input image, numpy array
    :param to_blur: apply blur to the image
    :param to_noise: apply noise to the image
    :return:
    """
    if to_blur:
        image = core.filter.blur.gauss(image)

    if to_noise:
        image = core.filter.noise(image)

    gradient = Gradient(image)
    dx, dy = gradient.grad_x, gradient.grad_y
    edges = gradient.gradient
    angles = core.angle.gradient_truth(dx, dy)
    lines = core.filter.lines(image, angles, edges)

    return lines
