import json
import os
from datetime import date
from pathlib import Path
from zipfile import ZipFile

import remotezip
import requests
import urllib3.exceptions
from markdown import markdown

from . import ROOT_DIR

__all__ = [
    'ZipUrl',
    'get_codemeta_from_zipurl',
    'zip_repository',
]


class ZipUrl(remotezip.RemoteZip, ZipFile):
    def __init__(self, url, initial_buffer_size=48 * 1024, **kwargs):
        # Zenodo imposes a limit on the zipfile to be read.
        # Some tests show that a limit with 48*1024 works fine.
        try:
            super().__init__(url, initial_buffer_size=initial_buffer_size, **kwargs)
        except requests.packages.urllib3.exceptions.ProtocolError as e:
            raise urllib3.exceptions.ProtocolError(f"{str(e)}\nTry lowering the initial buffer size for this zipfile")

    def find_files(self, filename):
        """
        return the path of files in the archive matching `filename`

        :param filename: string
        :return: list[str]
        """
        matching_files = [f for f in self.namelist() if Path(f).name == filename]
        if len(matching_files) == 0:
            raise FileNotFoundError(f"No file named {filename} in {self.url}")
        else:
            return matching_files

    def get_codemeta(self):
        codemeta_paths = self.find_files('codemeta.json')
        # if there are more than one codemeta file in the archive, we consider the one in the root directory, hence the
        # one with the shortest path
        codemeta_path = min(codemeta_paths, key=len)
        with self.open(codemeta_path) as file:
            codemeta = json.load(file)
        return codemeta


def get_codemeta_from_zipurl(url):
    """
    Extract and reads codemeta metadata from a zip url.
    A codemeta.json file must be present in the zip archive.

    :param url: string
        url to a zip file
    :return: dictionnary
        metadata in the codemeta.json file in the zip archive
    """
    zipurl = ZipUrl(url)
    return zipurl.get_codemeta()


def zip_repository(repository_path, zip_filename=None, overwrite=True):
    """
    Zip the content of `repository_path`
    `.git` subdirectories in the target directory will be excluded

    :param repository_path: str or Path
        Path to the directory to be zipped
    :param zip_filename: str
        Zip filename name, used to name the zip file. If None, the zip will be named as the directory provided.
    :param overwrite: bool
        True to overwrite existing zip archive

    :return: zip_filename: path to the zip archive
    """
    # prepare zip archive
    directory = Path(repository_path).resolve()
    zip_filename = f'{directory.absolute().name}.zip' if zip_filename is None else zip_filename
    if Path(zip_filename).exists() and not overwrite:
        raise FileExistsError(f"{zip_filename} exists. Set overwrite=True")

    print(f" * Zipping the content of {directory.absolute()} into {zip_filename}")

    with ZipFile(zip_filename, 'w') as zipObj:
        for folder_name, subfolders, filenames in os.walk(directory):
            # don't zip .git/ content nor the .git dir itself
            if '.git/' in folder_name or folder_name.endswith('.git'):
                continue
            # we want the relative path only inside the archive
            relpath = os.path.relpath(folder_name, directory.parent)
            for filename in filenames:
                abs_file_path = Path(folder_name).joinpath(filename).resolve()
                # avoid archiving the zip file itself
                if abs_file_path == Path(zip_filename).resolve():
                    continue
                rel_file_path = Path(relpath).joinpath(filename)
                zipObj.write(abs_file_path, rel_file_path)

    print(f"Zipping done: {zip_filename}")
    return zip_filename


def readme_to_html(readme_path=Path(ROOT_DIR).joinpath('README.md').as_posix()):
    """
    Read README.md and return html transcript
    :param readme_path: str
    :return: str
        text in readme converted to html
    """
    html = markdown(open(readme_path).read(), extensions=['fenced_code'])
    html = html.replace('\n', '')
    return html


def update_codemeta(codemeta_path=Path(ROOT_DIR).joinpath('codemeta.json').as_posix(), published=True, overwrite=True):
    """
    Update codemeta.json file for dates and description based on README.md

    :param codemeta_path: Path
    :param published: boolean
        if True, datePublished is updated.
    :param overwrite: boolean
        overwrite codemeta file
    :return:
    """
    with open(codemeta_path) as file:
        metadata = json.load(file)
    metadata['description'] = readme_to_html()
    metadata['dateModified'] = f'{date.today()}'

    if published:
        metadata['datePublished'] = f'{date.today()}'

    if overwrite:
        with open(codemeta_path, 'w') as file:
            json.dump(metadata, file, indent=4)
    return metadata
