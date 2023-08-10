import json
import os
from copy import deepcopy

import datasets
import orjson
import pandas as pd
from datasets import Dataset, load_dataset, load_from_disk
from huggingface_hub import create_repo, notebook_login
from PIL import Image

INPUT_PATH = "./dataset"
HUGGINGFACE_TOKEN = ""
REPO_ID = "jinho8345/funsd"

def merge_splited_dataset_and_push_to_hub(
    test_path: str,
    train_path: str,
    save_path: str,
    push_to_hub: bool = False,
):
    repo_name = "funsd"
    train = load_from_disk(train_path)
    test = load_from_disk(test_path)

    merged_dataset = datasets.DatasetDict(
        {
            "train": train,
            "test": test,
        }
    )

    merged_dataset.save_to_disk(save_path)
    merged_dataset = load_from_disk(save_path)

    if push_to_hub:
        # make a repo
        create_repo(repo_name, token=HUGGINGFACE_TOKEN, repo_type="dataset")

        # push the data to hub
        merged_dataset.push_to_hub(repo_id=REPO_ID, token=HUGGINGFACE_TOKEN)


def download_funsd_and_make_dataset(
    hug_format_root: str = "./dataset/huggingface_format",
):
    # download original funsd dataset
    if not os.path.exists(INPUT_PATH):
        os.system("wget https://guillaumejaume.github.io/FUNSD/dataset.zip")
        os.system("unzip dataset.zip")
        os.system("rm -rf dataset.zip __MACOSX")

    # convert to huggingface dataset
    for split in ["train", "test"]:
        root = f"./dataset/{split}ing_data"
        anno_names = sorted(os.listdir(os.path.join(root, "annotations")))
        img_names = sorted(os.listdir(os.path.join(root, "images")))

        assert [anno.split(".")[0] for anno in anno_names] == [
            img.split(".")[0] for img in img_names
        ]

        words = []
        for anno_name, img_name in zip(anno_names, img_names):
            anno_path = os.path.join(root, "annotations", anno_name)
            img_path = os.path.join(root, "images", img_name)

            with open(anno_path, "r") as f:
                data = orjson.loads(f.read())
            img = Image.open(img_path)

            form = data["form"]

            word = {
                "img": img,
                "filename": img_name,
                "boxes": [e["box"] for e in form],
                "labels": [e["label"] for e in form],
                "words": [e["words"] for e in form],
                "linkings": [e["linking"] for e in form],
                "ids": [e["id"] for e in form],
            }

            words.append(word)

        columnized_words = {
            "img": [e["img"] for e in words],
            "filename": [e["filename"] for e in words],
            "boxes": [e["boxes"] for e in words],
            "labels": [e["labels"] for e in words],
            "words": [e["words"] for e in words],
            "linkings": [e["linkings"] for e in words],
            "ids": [e["ids"] for e in words],
        }

        dataset = Dataset.from_dict(columnized_words)
        dataset.save_to_disk(os.path.join(hug_format_root, split))


if __name__ == "__main__":
    hug_format_root = "./dataset/huggingface_format"

    download_funsd_and_make_dataset(hug_format_root)
    merge_splited_dataset_and_push_to_hub(
        test_path=os.path.join(hug_format_root, "test"),
        train_path=os.path.join(hug_format_root, "train"),
        save_path=os.path.join(hug_format_root, "merged"),
    )
