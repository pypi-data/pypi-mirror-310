from astropy.table import Table
import numpy as np
import pytest
from madcubapy.io.madcubafits import MadcubaFits

def test_initialization_with_none():
    madcuba_map = MadcubaFits()
    assert madcuba_map.hist is None

def test_initialization_with_table():
    data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
    table = Table(data)
    madcuba_map = MadcubaFits(hist=table)
    assert isinstance(madcuba_map.hist, Table)
    assert len(madcuba_map.hist) == 3  # Check table length

def test_invalid_initialization_type():
    with pytest.raises(TypeError):
        MadcubaFits(hist="string")
    with pytest.raises(TypeError):
        MadcubaFits(hist=3)
    with pytest.raises(TypeError):
        MadcubaFits(hist=0.4)
    with pytest.raises(TypeError):
        MadcubaFits(hist=np.zeros(4,5))

def test_hist_setter():
    data = {'col1': [1, 2], 'col2': [3, 4]}
    table = Table(data)
    madcuba_map = MadcubaFits()
    # Set hist to a valid table
    madcuba_map.hist = table
    assert isinstance(madcuba_map.hist, Table)
    assert len(madcuba_map.hist) == 2
    # Set hist to None
    madcuba_map.hist = None
    assert madcuba_map.hist is None

def test_add_invalid_hist_file():
    with pytest.raises(FileNotFoundError):
        madcuba_fits = MadcubaFits()
        madcuba_fits.add_hist("nonexistent_file.csv")
