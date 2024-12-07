from astropy.table import Table
import pytest
from madcubapy.io.madcubamap import MadcubaMap

@pytest.fixture
def example_madcuba_map():
    # Create and return a Map instance to be used in tests
    return MadcubaMap.read(
        "madcubapy/io/tests/data/IRAS16293_SO_2-1_moment0_madcuba.fits"
    )

def test_read_madcuba_map(example_madcuba_map):
    # Test if the obligatory attributes are correctly initialized
    assert example_madcuba_map.ccddata is not None
    assert example_madcuba_map.data is not None
    assert example_madcuba_map.header is not None
    assert (example_madcuba_map.hist is None or
            isinstance(example_madcuba_map.hist, Table))

def test_invalid_file():
    with pytest.raises(FileNotFoundError):
        MadcubaMap.read("nonexistent_file.fits")
