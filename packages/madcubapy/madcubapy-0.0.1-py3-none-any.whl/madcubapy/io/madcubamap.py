import astropy
from astropy.io import fits
from astropy.nddata import CCDData
from astropy.table import Table
import numpy as np
import os
from pathlib import Path

from .madcubafits import MadcubaFits

class MadcubaMap(MadcubaFits):
    """A container for MADCUBA fits maps, using the
    `radioastro.madcubaio.MadcubaFits` interface.

    This class is basically a wrapper to read MADCUBA exported fits and their
    hist files with astropy.

    Parameters
    ----------
    data : numpy.ndarray
        The data array associated with the FITS file.
    header : astropy.io.fits.Header
        The header object associated with the FITS file.
    wcs : astropy.wcs.WCS
        The WCS object associated with the FITS file.
    unit : astropy.units.Base.unit
        The unit of the data of the FITS file.
    hist : astropy.table.Table
        An astropy Table object containing the history information of the fits
        file, which is stored in a separate _hist.csv file.
    ccddata : astropy.nddata.CCDData
        An astropy CCDData object loaded with astropy as a failsafe.

    """
    def __init__(
        self,
        data: np.ndarray = None,
        header: astropy.io.fits.Header = None,
        wcs: astropy.wcs.WCS = None,
        unit: astropy.units.UnitBase = None,
        hist: astropy.table.Table = None,
        ccddata: astropy.nddata.CCDData = None,
    ):
        # inherit hist
        super().__init__(hist)  # Initialize the parent class with hist

        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError("the data must be a numpy array.")
        self._data = data

        if header is not None and not isinstance(header, astropy.io.fits.Header):
            raise TypeError("the header must be an astropy.io.fits.Header.")
        self._header = header

        if wcs is not None and not isinstance(wcs, astropy.wcs.WCS):
            raise TypeError("the header must be an astropy.wcs.WCS.")
        self._wcs = wcs

        if unit is not None and not isinstance(unit, astropy.units.UnitBase):
            raise TypeError("the data must be an astropy unit.")
        self._unit = unit

        if ccddata is not None and not isinstance(ccddata, astropy.nddata.CCDData):
            raise TypeError("the ccddata must be a CCDData instance.")
        self._ccddata = ccddata

    @property
    def ccddata(self):
        """
        `astropy.nddata.CCDData` : CCDData object of the fits map.
        """
        return self._ccddata

    @ccddata.setter
    def ccddata(self, value):
        if value is not None and not isinstance(value, CCDData):
            raise TypeError("the ccddata must be a CCDData instance.")
        self._ccddata = value

    @property
    def data(self):
        """
        `numpy.ndarray` : The data of the fits map.
        """
        return self._data

    @data.setter
    def data(self, value):
        if value is not None and not isinstance(value, np.ndarray):
            raise TypeError("the data must be a numpy array.")
        self._data = value

    @property
    def header(self):
        """
        `astropy.io.fits.Header` : The header of the fits map.
        """
        return self._header

    @header.setter
    def header(self, value):
        if value is not None and not isinstance(value, astropy.io.fits.Header):
            raise TypeError("the header must be an astropy.io.fits.Header.")
        self._header = value

    @property
    def wcs(self):
        """
        `astropy.wcs.WCS` : The header of the fits map.
        """
        return self._wcs

    @wcs.setter
    def wcs(self, value):
        if value is not None and not isinstance(value, astropy.wcs.WCS):
            raise TypeError("the header must be an astropy.wcs.WCS.")
        self._wcs = value

    @property
    def unit(self):
        """
        `astropy.units.Unit` : The data of the fits map.
        """
        return self._unit

    @unit.setter
    def unit(self, value):
        if value is not None and not isinstance(value, astropy.units.UnitBase):
            raise TypeError("the data must be an astropy unit.")
        self._unit = value

    @classmethod
    def read(cls, filename: str, **kwargs):
        """
        Generate a MadcubaMap object from a FITS file. This method creates an
        Astropy CCDData from the fits file.

        Parameters
        ----------
        filename : str
            Name of fits file.
        kwargs
            Additional keyword parameters passed through to the Astropy
            CCDData.read() class method.

        """
        fits_filename = filename
        # Check if the fits file exists
        if not os.path.isfile(fits_filename):
            raise FileNotFoundError(f"File {fits_filename} not found.")
        # Load the CCDData from the .fits file
        ccddata = CCDData.read(fits_filename, **kwargs)
        # Load the Table from the .csv file if present
        hist_filename = os.path.splitext(fits_filename)[0] + "_hist.csv"
        if not os.path.isfile(hist_filename):
            print("WARNING: Default hist file not found.")
            hist = None
        else:
            hist = Table.read(hist_filename, format='csv')
        # Store the attributes
        data = ccddata.data
        header = ccddata.header
        # header = fits.getheader(fits_filename)
        wcs = ccddata.wcs
        unit = ccddata.unit
        # Return an instance of MadcubaFits
        madcuba_map = cls(
            data=data,
            header=header,
            wcs=wcs,
            unit=unit,
            hist=hist,
            ccddata=ccddata,
        )
        return madcuba_map

    def __repr__(self):
        # If hist is None, display that it's missing
        if self._hist is None:
            hist_r = "hist=None"
        # If hist is present, display a summary of the table
        else: hist_r = (
            f"hist=<Table length={len(self._hist)} rows, " +
            f"{len(self._hist.columns)} columns>"
        )
        if self._data is None:
            data_r = "data=None"
        else:
            data_r = f"data=<numpy.ndarray shape={self._data.shape}>"
        if self._unit is None:
            unit_r = "unit=None"
        else:
            unit_r = f"unit={self._unit}"

        return f"<MadcubaMap({data_r}, {unit_r}, {hist_r})>"
