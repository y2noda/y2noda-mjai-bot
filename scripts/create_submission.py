#!/usr/bin/env python3
import os
import shutil
import zipfile


def create_submission_zip():
    # 一時ディレクトリの作成
    tmp_dir = "tmp_submission"
    os.makedirs(tmp_dir, exist_ok=True)

    # 必要なファイルをコピー
    shutil.copy("src/bot.py", os.path.join(tmp_dir, "bot.py"))

    # zipファイルの作成
    with zipfile.ZipFile("submission.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(tmp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, tmp_dir)
                zf.write(file_path, arcname)

    # 一時ディレクトリの削除
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    create_submission_zip()
