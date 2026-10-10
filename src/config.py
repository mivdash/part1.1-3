import argparse


def razobrat_parametry():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--vfs-path",
        dest="vfs_path",
        default=None,
    )
    parser.add_argument(
        "--script",
        dest="script",
        default=None,
    )
    return parser.parse_args()