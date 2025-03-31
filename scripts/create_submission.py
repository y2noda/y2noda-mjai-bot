#!/usr/bin/env python3
import zipfile
from pathlib import Path


def create_submission_zip() -> None:
    """提出用のzipファイルを作成します。"""
    zip_filename = "submission.zip"
    src_root = Path("src")
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in src_root.rglob("*"):
            if item.is_file():
                arcname = item.relative_to(src_root)
                zf.write(item, arcname)


if __name__ == "__main__":
    create_submission_zip()
