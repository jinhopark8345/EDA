import itertools
import os
from copy import deepcopy
from random import random
from typing import Any, Dict, List, Tuple

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def draw_entities(
    ax, boxes: List[List[int]], labels: List[str], links: List[List[List[int]]]
):
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
        ax.annotate(str(label), (x2, y1), color="red", fontsize=8)

    for l in links:
        # filter out weird links
        if not l or len(l[0]) < 2:
            continue

        from_idx, to_idx = l[0]
        from_box, to_box = boxes[from_idx], boxes[to_idx]

        # from: top_left, to: bottom_right
        from_x, from_y = from_box[0], from_box[1]
        to_x, to_y = to_box[2], to_box[3]

        curved_arrow = patches.FancyArrowPatch(
            (from_x, from_y),
            (to_x, to_y),  # (x, y) of arrow start and end
            color="red",  # arrow color
            alpha=0.4,  # for transparency
            arrowstyle="->",  # style of arrow head
            mutation_scale=20,  # arrow head size
            connectionstyle="arc3,rad=-.2",  # to give curve to arrow
        )
        curved_arrow.set_linewidth(1)
        ax.add_patch(curved_arrow)


def draw_text_box_list(
    ax, text_box_list: List[Dict[str, Any]], xytext_offset: Tuple[int, int] = (3, 3)
):
    for idx, e in enumerate(text_box_list):
        x1, y1, x2, y2 = e["box"]
        width, height = x2 - x1, y2 - y1

        # make rectangle
        rect = patches.Rectangle(
            (x1, y1),
            width,
            height,
            linewidth=1,
            edgecolor="g",
            alpha=0.3,
            facecolor="none",
        )

        # add rectangle to the ax
        ax.add_patch(rect)

        # draw box idx on bottom right corner of the box
        ax.annotate(
            str(idx),
            (x1 + xytext_offset[0], y2 + xytext_offset[1]),
            color="g",
            fontsize=6,
        )


def vis_sample(sample: Dict[str, Any], dst_path: str):
    """visualize sample's words"""
    img = sample["img"]
    width, height = sample["img"].size
    boxes = sample["boxes"]
    words = sample["words"]
    links = sample["linkings"]
    filename = sample["filename"]
    labels = sample["labels"]
    text_box_list = list(itertools.chain.from_iterable(words))

    # convert all imgs to RGB for color support
    img = img.convert("RGB")

    # Create figure and axes
    fig = plt.figure(figsize=(width / 100, height / 100), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])

    ax.imshow(img)

    # 1. draw "word" information (boxes, indices, labels)
    draw_entities(ax, boxes, labels, links)

    # 2. draw text_box boxes on axes
    draw_text_box_list(ax, text_box_list)

    # 3. save figure
    fig.savefig(os.path.join(dst_path, filename), dpi=200)

    # clear plt to prevent memory leak
    plt.cla()  # clear the current axes
    plt.clf()  # clear the current figure
    plt.close()  # closes the current figure
