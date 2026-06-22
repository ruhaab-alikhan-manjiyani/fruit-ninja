import cv2
import numpy as np


def overlay_png(background, overlay, x, y):

    h, w = overlay.shape[:2]

    if x >= background.shape[1] or y >= background.shape[0]:
        return

    if x + w <= 0 or y + h <= 0:
        return

    x1 = max(x, 0)
    y1 = max(y, 0)

    x2 = min(x + w, background.shape[1])
    y2 = min(y + h, background.shape[0])

    overlay_x1 = x1 - x
    overlay_y1 = y1 - y

    overlay_x2 = overlay_x1 + (x2 - x1)
    overlay_y2 = overlay_y1 + (y2 - y1)

    overlay_crop = overlay[
        overlay_y1:overlay_y2,
        overlay_x1:overlay_x2
    ]

    if overlay_crop.shape[2] < 4:
        background[y1:y2, x1:x2] = overlay_crop
        return

    alpha = overlay_crop[:, :, 3] / 255.0

    for c in range(3):
        background[y1:y2, x1:x2, c] = (
            alpha * overlay_crop[:, :, c] +
            (1 - alpha) * background[y1:y2, x1:x2, c]
        )