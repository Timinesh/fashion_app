# image_processing.py

import base64
import io
import math

import numpy as np
from PIL import Image

from constants import (
    NAMED_COLORS,
    MAX_IMAGE_SIZE,
    CENTER_SAMPLE_SIZE,
)


def color_distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def nearest_color_name(rgb):
    best_name = None
    best_distance = float("inf")

    for name, value in NAMED_COLORS:
        d = color_distance(rgb, value)

        if d < best_distance:
            best_distance = d
            best_name = name

    return best_name


def resize_image(image: Image.Image):
    image = image.convert("RGB")

    w, h = image.size

    scale = min(1, MAX_IMAGE_SIZE / max(w, h))

    new_size = (
        int(w * scale),
        int(h * scale),
    )

    return image.resize(new_size, Image.Resampling.LANCZOS)


def center_crop(image):
    image = image.convert("RGB")

    w, h = image.size

    size = min(w, h)

    left = (w - size) // 2
    top = (h - size) // 2

    return image.crop(
        (
            left,
            top,
            left + size,
            top + size,
        )
    )


def dominant_color(image):
    image = center_crop(image)

    image = image.resize(
        (
            CENTER_SAMPLE_SIZE,
            CENTER_SAMPLE_SIZE,
        ),
        Image.Resampling.LANCZOS,
    )

    arr = np.array(image)

    r = np.median(arr[:, :, 0])
    g = np.median(arr[:, :, 1])
    b = np.median(arr[:, :, 2])

    rgb = (
        int(r),
        int(g),
        int(b),
    )

    return rgb, nearest_color_name(rgb)


def image_to_base64(image):
    buffer = io.BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=85,
    )

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def prepare_image(uploaded_file):
    image = Image.open(uploaded_file)

    resized = resize_image(image)

    rgb, color_name = dominant_color(resized)

    encoded = image_to_base64(resized)

    return {
        "image": resized,
        "rgb": rgb,
        "color_name": color_name,
        "base64": encoded,
    }
