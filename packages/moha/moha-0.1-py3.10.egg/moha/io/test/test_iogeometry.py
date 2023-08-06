from moha import *

import numpy as np
import pytest
import os

def molecules():
    options_list = [
        ("h2o", 'water', 3, 'C1'),
    ]
    for p in options_list:
        yield p


@pytest.mark.parametrize('file_name, title, size, symmetry', molecules())
def test_load_xyz(file_name, title, size, symmetry):
    """Test cases with plain scf slover.
    """
    dir_path = os.getcwd()
    path = os.path.join(dir_path,'{0:s}.xyz'.format(file_name))
    mol = load_xyz(path)

    assert mol.title == title 
    assert mol.size == size
    assert mol.symmetry == symmetry


