import importlib
import pytest

from importlib import resources

# Note that this is copied from lahman._fetch_data, but repeated here, so
# we can test the unpacking on import behavior
SOURCE_DIR = resources.files("lahman") / "data" 

@pytest.fixture(scope="session")
def cleanup():
    # Note that data is only removed at the end of the entire session
    yield

    from lahman import _fetch_data
    _fetch_data.remove_data()

# resources.files imports the module, so this test doesn't work...
@pytest.mark.xfail
def test_nodata():
    assert len(list(SOURCE_DIR.glob("*.csv"))) == 0

def test_data_after_import(cleanup):
    import lahman

    # 27 files of data
    assert len(lahman._lahman_fnames) == 27
    assert "allstar_full" in lahman._accessors

def test_data_load(cleanup):
    import lahman
    import pandas as pd

    assert isinstance(lahman.allstar_full(), pd.DataFrame)
    
