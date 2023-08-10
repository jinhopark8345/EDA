import itertools
import os
from copy import deepcopy
from random import random
from typing import Any, Dict, List, Tuple

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def draw_words(ax, boxes: List[List[int]], labels: List[str]):
    # draw word boxes and their indices
    for idx, (box, label) in enumerate(zip(boxes, labels)):
        x1, y1, x2, y2 = box
        width, height = x2 - x1, y2 - y1

        # draw box
        rect = patches.Rectangle(
            (x1, y1),
            width,
            height,
            linewidth=1,
            edgecolor="r",
            alpha=0.5,
            facecolor="none",
        )
        ax.add_patch(rect)

        # draw box idx on bottom right corner of the box
        ax.annotate(str(idx), (x2, y2), color="red", fontsize=8)

        # draw label on top right corner of the box
        ax.annotate(str(label), (x1, y2), color="blue", fontsize=8)


def vis_sample(sample: Dict[str, Any], dst_path: str):
    """visualize sample's words"""

    # dict_keys(['img', 'labels', 'words', 'bboxes', 'filename'])
    img = sample["img"]
    width, height = sample["img"].size
    filename = sample["filename"]
    words = sample["words"]
    bboxes = sample["bboxes"]
    labels = sample["labels"]

    # convert all imgs to RGB for color support
    img = img.convert("RGB")

    # Create figure and axes
    fig = plt.figure(figsize=(width / 100, height / 100), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])

    ax.imshow(img)

    # draw "word" information (boxes, indices, labels)
    draw_words(ax, bboxes, labels)

    # save figure
    fig.savefig(os.path.join(dst_path, filename), dpi=200)

    # clear plt to prevent memory leak
    plt.cla()  # clear the current axes
    plt.clf()  # clear the current figure
    plt.close()  # closes the current figure
