import argparse
import os

from datasets import load_dataset
from eda.sroie.vis import vis_sample
from tqdm import tqdm


def run_visualize(args):
    dst_path = args.dst
    dataset_name = args.dataset_name

    # vis all samples in SROIE dataset
    dataset = load_dataset(dataset_name)
    for split in dataset.keys():
        vis_save_path = os.path.join(dst_path, split)
        os.makedirs(vis_save_path, exist_ok=True)
        samples = dataset[split]

        # vis samples one by one
        for sample in tqdm(samples, desc=f"processing {split} dataset ..."):
            vis_sample(sample, vis_save_path)


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument("--dst", type=str, default="sroie_bio_vis_output")
    parser.add_argument("--dataset_name", type=str, default="jinho8345/sroie-bio")
    args, left_argv = parser.parse_known_args()

    run_visualize(args)
