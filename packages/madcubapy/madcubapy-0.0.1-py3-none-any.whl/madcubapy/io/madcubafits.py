import astropy
from astropy.table import Table
import os
from pathlib import Path

class MadcubaFits:
    """A basic class describing a MADCUBA Fits object with its hist file.

    The MadcubaFits class contains the only object shared by MADCUBA
    maps, cubes, and spectra: an Astropy Table describing the history
    file exported by MADCUBA.

    Parameters
    ----------
    hist : `astropy.table.Table`
        An astropy Table object containing the history information of the fits
        file, which is stored in a separate _hist.csv file.

    """
    def __init__(
        self,
        hist: astropy.table.Table = None,
    ):
        if hist is not None and not isinstance(hist, astropy.table.Table):
            raise TypeError(
                "The hist must be an astropy Table")
        self._hist = hist

    @property
    def hist(self):
        """
        `astropy.table.Table` : Table of the hist file.
        """
        return self._hist

    @hist.setter
    def hist(self, value):
        if value is not None and not isinstance(value, astropy.table.Table):
            raise TypeError(
                "The hist must be an astropy Table")
        self._hist = value

    def add_hist(self, filename):
        """Load the hist table from a csv file.

        Parameters
        ----------
        filename : str or pathlib.Path
            Path of the history csv file.

        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"file not found.")
        self._hist = Table.read(filename, format='csv')

    def __repr__(self):
        # If hist is None, display that it's missing
        if self._hist is None:
            hist_repr = "None"
        # If hist is present, display a summary of the table
        else: hist_repr = (
            f"<Table length={len(self._hist)} rows, " +
            f"{len(self._hist.columns)} columns>"
        )
        return f"<MadcubaFits(hist={hist_repr})>"
