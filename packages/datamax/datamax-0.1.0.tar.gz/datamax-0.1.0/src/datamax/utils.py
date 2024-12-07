import hashlib
import os
import shutil
import tarfile
from pathlib import Path
from tempfile import tempdir
from typing import Optional

import faker


def get_file_digest(file: Optional[Path] = None):
    sha256 = hashlib.sha256()
    if not file:
        return {"digest": f"sha256:{sha256.hexdigest()}", "size": 2}
    with open(file, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return {"digest": f"sha256:{sha256.hexdigest()}", "size": file.stat().st_size}


def make_tarfile(output_filename: Path, source_dir: Path):
    with tarfile.open(output_filename, "w:gz", encoding="utf-8") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return output_filename


def generate_name(name: str, word_count: int = 1):
    if name == "":
        return "_".join(faker.Faker().words(nb=word_count))
    return name


def move_file_to_blobs(blobs_dir: Path, file: Path, digest: str):
    digest_algo, digest_hash = digest.split(":")
    digest_destination_dir = blobs_dir / digest_algo
    digest_destination_dir.mkdir(parents=True, exist_ok=True)
    digest_destination = digest_destination_dir / digest_hash
    with open(file, "rb") as src, open(digest_destination, "wb") as dest:
        shutil.copyfileobj(src, dest)
