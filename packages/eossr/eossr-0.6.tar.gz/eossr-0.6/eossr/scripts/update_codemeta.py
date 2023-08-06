import argparse
from pathlib import Path

from eossr import ROOT_DIR
from eossr.utils import update_codemeta


def build_argparser():
    """
    Construct main argument parser for the ``codemet2zenodo`` script

    :return:
    argparser: `argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser(description="Update Codemeta")

    parser.add_argument(
        '--codemeta_path',
        '-c',
        type=str,
        dest='codemeta_path',
        help='Path to codemeta.json',
        default=Path(ROOT_DIR).joinpath('codemeta.json'),
        required=False,
    )
    return parser


if __name__ == '__main__':

    parser = build_argparser()
    args = parser.parse_args()
    html = update_codemeta(codemeta_path=args.codemeta_path)
