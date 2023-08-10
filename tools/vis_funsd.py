import argparse
import os

from datasets import load_dataset
from eda.funsd.vis import vis_sample
from tqdm import tqdm


def run_visualize(args):
    # make dst folder
    dst_path = args.dst
    dataset_name = args.dataset_name
    os.makedirs(dst_path)

    # vis all samples in FUNSD dataset
    for split in ["train", "test"]:
        samples = load_dataset(dataset_name)[split]

        # vis samples one by one
        for sample in tqdm(samples, desc=f"processing {split} dataset ..."):
            vis_sample(sample, dst_path)


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument("--dst", type=str, default="funsd_vis_output")
    parser.add_argument("--dataset_name", type=str, default="jinho8345/funsd")
    args, left_argv = parser.parse_known_args()

    run_visualize(args)
