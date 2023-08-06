import argparse
from pathlib import Path

from eossr.metadata import codemeta


def build_argparser():
    """
    Construct main argument parser for the ``codemet2zenodo`` script

    :return:
    argparser: `argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser(
        description="Validate a codemeta file. "
        "Raises warnings for recommended changes "
        "and errors for unvalid entries"
    )

    parser.add_argument('filename', type=Path, help='Path to codemeta.json')
    parser.add_argument(
        '--catch-all-errors',
        action='store_true',
        help="If passed, all errors will be raised and displayed. " "It not, the program stops at the first error.",
    )
    return parser


def main():

    parser = build_argparser()
    args = parser.parse_args()

    codemeta_handler = codemeta.Codemeta.from_file(args.filename)

    if not args.catch_all_errors:
        codemeta_handler.validate()
    else:
        for error in codemeta_handler.error_generator():
            try:
                raise error
            except codemeta.CodemetaRequiredError as e:
                print(e)

        print(
            f"There are {codemeta.CodemetaRecommendedWarning.counter} warnings \
        and {codemeta.CodemetaRequiredError.counter} errors to take care of"
        )


if __name__ == '__main__':
    main()
