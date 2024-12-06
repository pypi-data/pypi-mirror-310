"""Script to interact with Google Cloud Storage.

It requires the `google-cloud-storage` Python package,
and uses the `metadata.json` to store the state of the currently used files.

Note: this script the env variable `GOOGLE_APPLICATION_CREDENTIALS` is exported.
"""

import glob
import json
import os
import pathlib

import fire  # type: ignore
from google.cloud import storage  # type: ignore

METADATA_FILE = "metadata.json"
BUCKET_NAME = "llm-wheels"


class Commands(object):
    """
    This CLI utility can be used to upload and download
    versioned directories to a GCS bucket.
    """

    def info(self) -> None:
        """Print information about the default values used by the commands of this CLI."""
        print(f"Metadata file: {METADATA_FILE}")
        print(f"Contents metadata: {read_metadata(METADATA_FILE)}")
        print(f"Default bucket name: {BUCKET_NAME}")

    def list(self, version: int = 0) -> None:
        """List the files in the default BUCKET_NAME.

        If a version is not passed then, the current versions of the tracked files are used.
        """
        metadata = read_metadata(METADATA_FILE)

        blobs = list_gcs_bucket(bucket_name=BUCKET_NAME)
        print(f">>> The contents of the {BUCKET_NAME} GCS bucket are:")
        for dir_key in metadata.keys():
            if version == 0:
                version = metadata[dir_key]

            for b in blobs:
                if f"{dir_key}_V{version:03d}" in b.name:  # type: ignore
                    print(f"- {b.name}")  # type: ignore

    def update(self, directory: str) -> None:
        """Update a directory."""
        directory = directory[:-1] if directory.endswith("/") else directory
        metadata = read_metadata(metadata_file=METADATA_FILE)

        if directory in metadata.keys():
            dir_version = int(metadata[directory]) + 1
        else:
            dir_version = 1

        destination_dir = f"{directory}_V{dir_version:03d}"
        print(f">>> Going to upload as {destination_dir}")
        upload_failed = False
        try:
            upload_directory_to_bucket(
                bucket_name=BUCKET_NAME,
                source_dir=directory,
                destination_dir=destination_dir,
            )
        except Exception as e:
            print(f"Exception: {e}")
            upload_failed = True

        if not upload_failed:
            metadata[directory] = dir_version
            write_metadata(metadata_file=METADATA_FILE, metadata=metadata)

    def get(self, directory: str, version: int = 0) -> None:
        """Download a directory."""
        directory = directory[:-1] if directory.endswith("/") else directory
        metadata = read_metadata(metadata_file=METADATA_FILE)
        assert directory in metadata.keys(), "Directory not tracked by metadata.json"

        if version == 0:
            dir_version = metadata[directory]
        else:
            dir_version = version
        source_dir = f"{directory}_V{dir_version:03d}"

        download_directory_from_bucket(
            bucket_name=BUCKET_NAME,
            source_dir=source_dir,
            destination_dir=directory,
        )


def read_metadata(metadata_file: str) -> dict:
    """Read the metadata file used to track versions of directories."""
    if not os.path.exists(metadata_file):
        return dict()

    with open(metadata_file, "rb") as f:
        metadata: dict = json.load(f)
    return metadata


def write_metadata(
    metadata_file: str,
    metadata: dict,
) -> None:
    """Write the metadata file."""
    with open(metadata_file, "w") as f:
        json.dump(metadata, f)


def list_gcs_bucket(bucket_name: str) -> list[str]:
    """List files and directories in the root of a GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    return list(blobs)


def upload_file_to_bucket(
    bucket_name: str,
    source_file_name: str,
    destination_blob_name: str,
) -> None:
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def download_file_from_bucket(
    bucket_name: str,
    source_blob_name: str,
    destination_file_name: str,
) -> None:
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def upload_directory_to_bucket(
    bucket_name: str,
    source_dir: str,
    destination_dir: str,
) -> None:
    """Uploads a directory and all its files to a GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    source_dir = str(pathlib.Path(source_dir).resolve(strict=True))
    source_files = [p for p in sorted(glob.glob(source_dir + "/*")) if os.path.isfile(p)]
    print(f"Uploading {source_dir}")
    for file_path in source_files:
        relative_path = os.path.relpath(file_path, source_dir)
        gcs_blob_path = os.path.join(destination_dir, relative_path)
        blob = bucket.blob(gcs_blob_path)
        blob.upload_from_filename(file_path)

        print(f"\t- File {file_path} uploaded to {gcs_blob_path}")
    print("---")


def download_directory_from_bucket(
    bucket_name: str,
    source_dir: str,
    destination_dir: str,
) -> None:
    """Downloads a directory and all its files from a GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    blobs = bucket.list_blobs(prefix=source_dir)

    for blob in blobs:
        if blob.name.endswith("/"):
            continue

        relative_path = os.path.relpath(blob.name, source_dir)
        local_file_path = os.path.join(destination_dir, relative_path)

        local_dir = os.path.dirname(local_file_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        blob.download_to_filename(local_file_path)
        print(f"Downloaded {blob.name} to {local_file_path}")


if __name__ == "__main__":
    fire.Fire(Commands)
