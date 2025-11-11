#!/usr/bin/env python3
"""Pack/unpack FAISS index for artifact storage."""

import argparse
import shutil
from pathlib import Path


def pack_index(source_dir: Path, output_file: Path):
    """Pack vector store into a single archive."""
    print(f"Packing {source_dir} -> {output_file}")
    shutil.make_archive(str(output_file.with_suffix("")), "zip", source_dir)
    print(f"✅ Packed to {output_file}")


def unpack_index(archive_file: Path, target_dir: Path):
    """Unpack vector store archive."""
    print(f"Unpacking {archive_file} -> {target_dir}")
    shutil.unpack_archive(archive_file, target_dir)
    print(f"✅ Unpacked to {target_dir}")


def main():
    parser = argparse.ArgumentParser(description="Pack/unpack vector store")
    parser.add_argument(
        "--action",
        choices=["pack", "unpack"],
        required=True,
        help="Action to perform",
    )
    parser.add_argument(
        "--source",
        default="storage/vector_store",
        help="Source directory (for pack)",
    )
    parser.add_argument(
        "--archive",
        default="storage/vector_store.zip",
        help="Archive file path",
    )
    parser.add_argument(
        "--target",
        default="storage/vector_store",
        help="Target directory (for unpack)",
    )

    args = parser.parse_args()

    if args.action == "pack":
        pack_index(Path(args.source), Path(args.archive))
    else:
        unpack_index(Path(args.archive), Path(args.target))


if __name__ == "__main__":
    main()
