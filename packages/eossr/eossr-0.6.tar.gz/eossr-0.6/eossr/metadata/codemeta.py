import json
from pathlib import Path
from warnings import warn

import pandas as pd
import pkg_resources

__all__ = [
    'schema',
    'codemeta_crosswalk',
    'Codemeta',
]


def schema():
    return json.load(pkg_resources.resource_stream(__name__, 'schema/codemeta.json'))


def codemeta_crosswalk():
    return pd.read_csv(
        pkg_resources.resource_stream(__name__, 'schema/escape_codemeta_crosswalk.csv'), comment='#', delimiter=';'
    )


class CodemetaRequiredError(KeyError):
    counter = 0

    def __init__(self, message):
        CodemetaRequiredError.counter += 1


class CodemetaRecommendedWarning(Warning):
    counter = 0

    def __init__(self, message):
        CodemetaRecommendedWarning.counter += 1


class Codemeta:
    def __init__(self, metadata: dict):
        self.metadata = metadata
        self._crosswalk_table = None

    @classmethod
    def from_file(cls, codemeta_filename):
        """Load `codemeta_filename` into the validator"""
        with open(codemeta_filename) as infile:
            controller = cls(json.load(infile))
        return controller

    @property
    def schema(self):
        return schema()

    @property
    def crosswalk_table(self):
        if self._crosswalk_table is None:
            self._crosswalk_table = codemeta_crosswalk()
        return self._crosswalk_table

    def error_generator(self):
        """
        Check the validity of the metadata dictionary
        """
        for ii, row in self.crosswalk_table.iterrows():
            if row['OSSR Requirement Level'] == 'required' and row['Property'] not in self.metadata.keys():
                yield CodemetaRequiredError(f"{row['Property']} not provided in the codemeta schema but is required")

            if row['OSSR Requirement Level'] == 'recommended' and row['Property'] not in self.metadata.keys():
                warn(
                    f"`{row['Property']}` not provided in the codemeta schema but is recommended",
                    CodemetaRecommendedWarning,
                )

    def validate(self):
        for error in self.error_generator():
            raise error

    def write(self, path='codemeta.json', overwrite=False):
        if Path(path).exists() and not overwrite:
            raise FileExistsError(f"File {path} exists. Use overwrite=True to overwrite")
        else:
            with open(path, 'w') as f:
                json.dump(self.metadata, f, indent=4)
