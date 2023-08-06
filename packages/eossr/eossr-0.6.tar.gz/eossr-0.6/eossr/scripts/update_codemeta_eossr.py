import argparse
from pathlib import Path

from eossr import ROOT_DIR
from eossr import __version__ as eossr_version
from eossr.metadata import codemeta
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


def update_version(codemeta_path):
    codemeta_handler = codemeta.Codemeta.from_file(codemeta_path)
    metadata = codemeta_handler.metadata

    metadata[
        'downloadUrl'
    ] = f'https://gitlab.in2p3.fr/escape2020/wp3/eossr/-/archive/v{eossr_version}/eossr-v{eossr_version}.zip'
    metadata['version'] = f"v{eossr_version}"
    metadata['softwareVersion'] = f"v{eossr_version}"

    codemeta_handler.write(path=codemeta_path, overwrite=True)


if __name__ == '__main__':

    parser = build_argparser()
    args = parser.parse_args()
    html = update_codemeta(codemeta_path=args.codemeta_path)
    update_version(args.codemeta_path)
