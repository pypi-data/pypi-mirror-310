import random
import scipy
import bisect

import cv2
import math
import numpy as np

from tqdm import tqdm

import matplotlib.pyplot as plt

from arty.core.brush import Brush
from arty.core.filter.color import generate_color_set, extend_color_set
from arty.core.edge.gradient import Gradient


class RandomGrid:
    def __init__(self, height, width, scale):
        self.height = height
        self.width = width
        self.scale = scale

    def generate(self):
        radius = self.scale // 2

        grid = [
            ((y + random.randint(-radius, radius)) % self.height,
             (x + random.randint(-radius, radius)) % self.width)
            for y in range(0, self.height, self.scale)
            for x in range(0, self.width, self.scale)
        ]

        random.shuffle(grid)

        return grid


class ImagePainter:
    def __init__(self, image, preset):
        self.image = image
        self.preset = preset
        self.brush = Brush(self.preset.brush_type)
        self.stroke_scale = self._compute_stroke_scale()
        self.gradient_smoothing_radius = self._compute_smoothing_radius()
        self.color_set = None
        self.gradient = None
        self.k = 9
        self.result = None
        self.gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def _compute_stroke_scale(self):
        return int(
            math.ceil(max(self.image.shape) / 1000)) if self.preset.stroke_scale == 0 else self.preset.stroke_scale

    def _compute_smoothing_radius(self):
        return int(round(
            max(self.image.shape) / 50)) if self.preset.gradient_smoothing_radius == 0 else self.preset.gradient_smoothing_radius

    def prepare_color_set(self):
        """Generate and extend the color set."""
        print("Computing color set...")
        image = self.gray_image if self.preset.grayscale else self.image
        max_img_size = 200
        self.color_set = generate_color_set(image, self.preset.palette_size, max_img_size)
        print("Extending color color set...")

        if not self.preset.grayscale:
            self.color_set = extend_color_set(self.color_set, [(0, 50, 0), (15, 30, 0), (-15, 30, 0)])

    def compute_gradient(self):
        """Compute the gradient of the image."""
        print("Computing gradient...")
        self.gradient = Gradient(self.gray_image, self.preset.gradient_type, self.preset.gradient_smoothing_type,
                                 self.gradient_smoothing_radius)

    def _color_probabilities(self, pixels):
        """Compute color probabilities for the given pixels."""
        distances = scipy.spatial.distance.cdist(pixels, self.color_set)
        inverted_distances = np.max(distances, axis=1, keepdims=True) - distances
        normalized_distances = inverted_distances / inverted_distances.sum(axis=1, keepdims=True)
        scaled_distances = np.exp(self.k * len(self.color_set) * normalized_distances)
        probabilities = scaled_distances / scaled_distances.sum(axis=1, keepdims=True)

        return np.cumulative_sum(probabilities, axis=1, dtype=np.float32)

    def _get_color(self, probabilities):
        """Select a color from the set based on probabilities."""
        r = random.uniform(0, 1)
        i = bisect.bisect_left(probabilities, r)

        return self.color_set[i] if i < len(self.color_set) else self.color_set[-1]

    def paint(self):
        """Perform the painting operation."""
        print("Painting image...")

        if self.preset.has_cardboard:
            result = cv2.medianBlur(self.image, 11) if not self.preset.grayscale else cv2.medianBlur(self.gray_image, 11)
        else:
            result = np.full_like(self.image, 255, dtype=np.uint8)

        grid = RandomGrid(self.image.shape[0], self.image.shape[1], scale=self.preset.grid_scale).generate()

        batch_size = 10000

        for h in tqdm(range(0, len(grid), batch_size)):
            batch = grid[h:min(h + batch_size, len(grid))]
            pixels = np.array([self.image[y, x] for y, x in batch])
            color_probabilities = self._color_probabilities(pixels)

            for i, (y, x) in enumerate(batch):
                color = self._get_color(color_probabilities[i])
                angle = math.degrees(self.gradient.angle(y, x)) + 90

                if self.preset.length_type == "base":
                    length = max(int(round(self.stroke_scale + self.stroke_scale * math.sqrt(
                        self.gradient.strength(y, x))) * self.preset.length_scale), 1)
                elif self.preset.length_type == "inverse":
                    length = max(
                        1,
                        int(1 / round(self.stroke_scale + self.stroke_scale * math.sqrt(
                            self.gradient.strength(y, x))) ** 1.9 * 10 * self.preset.length_scale)
                    )
                else:
                    raise ValueError(f"Invalid length function: {self.preset.length_type}")

                self.brush.apply(result, (x, y), length, color, self.stroke_scale, angle, self.preset.length_first_flag)

        self.result = result

        return result

    # function to show the result
    def show_result(self):
        plt.figure(figsize=(10, 10))
        plt.subplot(1, 1, 1)
        if self.preset.grayscale:
            plt.imshow(self.result)
        else:
            plt.imshow(cv2.cvtColor(self.result, cv2.COLOR_BGR2RGB))
        plt.show()
