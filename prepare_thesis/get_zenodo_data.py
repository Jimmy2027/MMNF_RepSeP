"""Download trianed models and evaluation results from zenodo"""
from pathlib import Path

from modun.download_utils import download_zip_from_url

download_zip_from_url(url="https://zenodo.org/record/5588294/files/data.zip?download=1",
                      dest_folder=Path(__file__).parent.parent, verbose=True)
