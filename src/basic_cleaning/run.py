#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import os
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Download artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Load data")
    df = pd.read_csv(artifact_local_path)

    logger.info("Drop outliers and convert data string to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    logger.info("Save cleaned data as csv")
    filename = "clean_sample.csv"
    df.to_csv(filename, index=False)

    logger.info("Log cleaned artifact")
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    artifact.add_file(filename)
    run.log_artifact(artifact)

    os.remove(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help='Input artifact on W&B to download',
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help='Output artifact name to upload to W&B',
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help='Output type of the artifact',
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help='Output description of the artifact',
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help='Minimum rental price, lower prices will dropped',
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help='Maximum rental price, higher prices will dropped',
        required=True
    )

    args = parser.parse_args()

    go(args)
