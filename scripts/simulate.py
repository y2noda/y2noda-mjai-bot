from pathlib import Path

import mjai


def main():
    submissions = [
        "examples/shanten.zip",
        "examples/tsumogiri.zip",
        "examples/tsumogiri.zip",
        "submission.zip",
    ]
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    logs_dir = project_root / "logs"
    mjai.Simulator(submissions, logs_dir=logs_dir, timeout=20.0).run()


if __name__ == "__main__":
    main()
