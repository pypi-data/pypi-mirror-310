import logging
import os
import pickle

import polars as pl

from giotto_llm.bucket.deserialize import deserialize
from giotto_llm.consts import ROOT_PATH
from giotto_llm.logs import get_named_logger


def deserialize_task(serialized_train_grids: list) -> dict[str, list]:
    assert len(serialized_train_grids) % 2 == 0, f"Need an even number of grid in training"

    pairs = list()
    for idx_pair in range(0, len(serialized_train_grids), 4):
        idx_in = idx_pair + 1
        idx_out = idx_pair + 3
        if serialized_train_grids[idx_pair][-1] == "T":
            # Note: skipping test pairs
            continue

        grid_in = deserialize(serialized_train_grids[idx_in])
        grid_out = deserialize(serialized_train_grids[idx_out])
        pairs.append({"input": grid_in.tolist(), "output": grid_out.tolist()})

    return {"train": pairs[:-1], "test": [pairs[-1]]}


if __name__ == "__main__":

    logger = get_named_logger(
        name="get_synth_data",
        log_level=logging.INFO,
        enable_log_to_file=True,
        project_root=str(ROOT_PATH),
        output_dir="logs",
    )
    simon_synth_datasets = [
        {
            "category": "combine-v155",
            "url": "hf://datasets/neoneye/simon-arc-combine-v155/data.jsonl",
        },
        {
            "category": "ray-v5",
            "url": "hf://datasets/neoneye/simon-arc-solve-ray-v5/data.jsonl",
        },
        {
            "category": "mass-v24",
            "url": "hf://datasets/neoneye/simon-arc-mass-v24/data.jsonl",
        },
        {
            "category": "outline-v2",
            "url": "hf://datasets/neoneye/simon-arc-solve-outline-v2/data.jsonl",
        },
        {
            "category": "probecolor-v9",
            "url": "hf://datasets/neoneye/simon-arc-solve-probecolor-v9/data.jsonl",
        },
        {
            "category": "reverse-v2",
            "url": "hf://datasets/neoneye/simon-arc-solve-reverse-v2/data.jsonl",
        },
        {
            "category": "rotate-v8",
            "url": "hf://datasets/neoneye/simon-arc-solve-rotate-v8/data.jsonl",
        },
        {
            "category": "scale-v6",
            "url": "hf://datasets/neoneye/simon-arc-solve-scale-v6/data.jsonl",
        },
        {
            "category": "skew-v3",
            "url": "hf://datasets/neoneye/simon-arc-solve-skew-v3/data.jsonl",
        },
        {
            "category": "span-v11",
            "url": "hf://datasets/neoneye/simon-arc-solve-span-v11/data.jsonl",
        },
        {
            "category": "symmetry-v25",
            "url": "hf://datasets/neoneye/simon-arc-solve-symmetry-v25/data.jsonl",
        },
        {
            "category": "augment-v3",
            "url": "hf://datasets/neoneye/simon-arc-solve-augment-v3/data.jsonl",
        },
        {
            "category": "mask-v6",
            "url": "hf://datasets/neoneye/simon-arc-solve-mask-v6/data.jsonl",
        },
        {
            "category": "halfplane-v3",
            "url": "hf://datasets/neoneye/simon-arc-solve-halfplane-v3/data.jsonl",
        },
        {
            "category": "fractal-v7",
            "url": "hf://datasets/neoneye/simon-arc-solve-fractal-v7/data.jsonl",
        },
        {
            "category": "flip-v3",
            "url": "hf://datasets/neoneye/simon-arc-solve-flip-v3/data.jsonl",
        },
        {
            "category": "edge-v6",
            "url": "hf://datasets/neoneye/simon-arc-solve-edge-v6/data.jsonl",
        },
        {
            "category": "gravity-v13",
            "url": "hf://datasets/neoneye/simon-arc-solve-gravity-v13/data.jsonl",
        },
        {
            "category": "erosion-v2",
            "url": "hf://datasets/neoneye/simon-arc-solve-erosion-v2/data.jsonl",
        },
        {
            "category": "cross-v4",
            "url": "hf://datasets/neoneye/simon-arc-solve-cross-v4/data.jsonl",
        },
        {
            "category": "compress-v6",
            "url": "hf://datasets/neoneye/simon-arc-solve-compress-v6/data.jsonl",
        },
        {
            "category": "color-v15",
            "url": "hf://datasets/neoneye/simon-arc-solve-color-v15/data.jsonl",
        },
        {
            "category": "boundingbox-v7",
            "url": "hf://datasets/neoneye/simon-arc-solve-boundingbox-v7/data.jsonl",
        },
        {
            "category": "bool-v4",
            "url": "hf://datasets/neoneye/simon-arc-solve-bool-v4/data.jsonl",
        },
        {
            "category": "grid-v5",
            "url": "hf://datasets/neoneye/simon-arc-solve-grid-v5/data.jsonl",
        },
        {
            "category": "count-v7",
            "url": "hf://datasets/neoneye/simon-arc-solve-count-v7/data.jsonl",
        },
        {
            "category": "zindex-v9",
            "url": "hf://datasets/neoneye/simon-arc-solve-zindex-v9/data.jsonl",
        },
    ]

    for dataset_info in simon_synth_datasets:
        logger.info(f">>> Starting cleaning {dataset_info}")
        category = dataset_info["category"]
        url = dataset_info["url"]
        logger.info(f">>> URL: {url}")

        # Note: the following line will do
        df_input = pl.read_ndjson(url)
        logger.info(f">>> Got {len(df_input)} samples")
        logger.info(f">>> Got {df_input.head()} head")

        synth_data = dict()
        count_inconsistent_samples = 0
        for idx_sample in range(len(df_input)):
            if idx_sample % 20_000 == 0:
                logger.info(f">>> Processing sample at index {idx_sample} in {category=}")

            task_id = f"{category}_{idx_sample:06d}"
            sample_train = df_input[idx_sample, "input"]
            serialized_train_grids = sample_train.split("\n")
            if (
                (len(serialized_train_grids) < 8)
                or (serialized_train_grids[0] != "I0")
                or (serialized_train_grids[4] != "I1")
            ):
                count_inconsistent_samples += 1
                continue
            # Note: ignoring sample_test = df_input[idx_sample, "output"]
            task = deserialize_task(serialized_train_grids=serialized_train_grids)
            synth_data[task_id] = task

        logger.info(
            f">>> Finished processing {category}. Found {count_inconsistent_samples} inconsistent samples"
        )

        output_dir_path = ROOT_PATH / "synth_data"
        output_file_path = output_dir_path / f"{category}.pickle"
        os.makedirs(output_dir_path, exist_ok=True)

        logger.info(f">>> Writing to Pickle file {output_file_path}")
        with open(output_file_path, "wb") as file_handle:
            pickle.dump(synth_data, file_handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info(f">>> Done")
