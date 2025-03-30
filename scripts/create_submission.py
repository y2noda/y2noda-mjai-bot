#!/usr/bin/env python3
import shutil
import zipfile
from pathlib import Path


def create_submission_zip() -> None:
    """提出用のzipファイルを作成します。"""
    # 一時ディレクトリの作成
    tmp_dir = Path("tmp_submission")
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)

    # srcディレクトリの中身全体を一時ディレクトリにコピー
    src_dir = Path("src")
    shutil.copytree(src_dir, tmp_dir / src_dir.name)

    # zipファイルの作成
    zip_filename = "submission.zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in tmp_dir.rglob("*"):
            if item.is_file():
                arcname = item.relative_to(tmp_dir)
                zf.write(item, arcname)

    # 一時ディレクトリの削除
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    create_submission_zip()
