import math
import pandas as pd
from pathlib import Path
import warnings
from .base import get_data_path

def find_all_cids(path=None):
    cids = set()
    path = path or get_data_path()
    for archive in path.iterdir():
        if archive.name == 'more':
            cids |= set(find_all_cids(archive))
        possible_molecules_file = (archive / 'molecules.csv')
        if possible_molecules_file.is_file():
            try:
                df = pd.read_csv(possible_molecules_file, index_col=0)
            except Exception as e:
                warnings.warn("Could not read %s." % possible_molecules_file)
            else:
                cids |= set(df.index)
    cids = sorted([x for x in cids if x>0 and not math.isnan(x)])
    return cids