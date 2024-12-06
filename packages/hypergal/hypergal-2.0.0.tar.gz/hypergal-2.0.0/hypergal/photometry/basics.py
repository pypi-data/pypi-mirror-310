""" Basic Photometry tools """

import pandas
import warnings
import numpy as np
import pandas as pd

from .astrometry import WCSHolder


def get_filter(name, as_dataframe=True, sep=" ", **kwargs):
    """ """
    import os
    from .. import _PACKAGE_ROOT

    file_ = os.path.join(_PACKAGE_ROOT, f"data/filters/{name}.dat")
    if not os.path.isfile(file_):
        raise IOError(f"not such file {file_}")
    if as_dataframe:
        return pandas.read_csv(file_, sep=sep, header=None, names=["lbda", "trans"], **kwargs)

    return np.asarray([l.split(sep) for l in open(file_).read().splitlines()], dtype="float").T


def get_filter_efflbda(name):
    """ """
    name = np.atleast_1d(name)
    efflbda = []
    for name_ in name:
        l, f = get_filter(name_, as_dataframe=False)
        efflbda.append(np.average(l, weights=f))

    if len(efflbda) == 1:
        return efflbda[0]

    return np.asarray(efflbda)


class CutOut(WCSHolder):

    def __init__(self, instdata=None, radec=None):
        """ 
        Set ra, dec and instrument data

        Parameters
        ----------
        ra, dec: floats  -optional-
            Position in degrees

        instdata: list of Instrument object  -optional-

        Returns
        --------
        """
        self.set_instdata(instdata=instdata)
        if radec is not None:
            self.set_radec(*radec)

    # ================ #
    #  Initialisation  #
    # ================ #
    @classmethod
    def from_radec(cls, ra, dec, load_cutout=True, size=180, client=None,  filters=None):
        """ 
        Load cutout from ra, dec datas

        Parameters
        ----------
        ra,dec: floats
            Position in degrees

        size: float
            Image size in pixels\n
            Default is 140

        filters: strings -optional-
            String with filters to include\n
            If None, load all the filters

        client: Dask Client -optional-
            Provide a dask client for using Dask multiprocessing.\n
            If so, a list of futures will be returned.

        Returns
        --------
        List of cutout
        """

        if load_cutout:
            instdata = cls.download_cutouts(
                ra, dec, size=size, filters=filters, client=client)
        else:
            instdata = None

        return cls(instdata=instdata, radec=[ra, dec])

    @classmethod
    def from_sedmfile(cls, filename, load_cutout=True, size=180, client=None,  filters=["g", "r", "i", "z", "y"]):
        """ 
        Load cutout from SEDM file, according to the ra, dec information in the header

        Parameters
        ----------
        filename: string
            Path of the sedm object

        size: float
            Image size in pixels\n
            Default is 140

        filters: strings  -optional-
            String with filters to include \n
            If None, load all the filters

        client: Dask Client  -optional-
            Provide a dask client for using Dask multiprocessing.\n
            If so, a list of futures will be returned.

        Returns
        --------
        List of cutout
        """
        from astropy.io import fits
        from astropy import coordinates, units

        header = fits.getheader(filename)
        coords = coordinates.SkyCoord(header.get("OBJRA"), header.get("OBJDEC"),
                                      frame='icrs', unit=(units.hourangle, units.deg))
        ra, dec = coords.ra.deg, coords.dec.deg
        # -
        return cls.from_radec(ra, dec, load_cutout=load_cutout, size=size, client=client, filters=filters)

    # ================ #
    #  StaticMethods   #
    # ================ #
    @staticmethod
    def download_cutouts(ra, dec, size=180, filters=None, client=None, ignore_warnings=True):
        """ """
        raise NotImplementedError(
            " Object inheriting from CutOut must implemente download_cutouts")

    # ================ #
    #   Methods        #
    # ================ #
    def to_cube(self, header_id=0, influx=True, binfactor=None, xy_center=None, **kwargs):
        """ 
        Transform CutOuts object into 3d Cube, according to the wavelength of each image.

        Parameters
        ----------
        xy_center: None or string or float -optional-
            Center coordinates (in pixel) or the returned cube.\n
            - if None: this is ignored\n
            - if string: 'target', this will convert the self.ra and self.dec into xy_center and set it\n
            - else; used as centroid

        influx: bool  -optional-
            If True, return data in flux in erg.s-1.cm-2.AA-1\n
            If False, return data in counts.

        binfactor: int -optional-
            Apply a binning [binfactor x binfactor] on the images

        Returns
        --------
        WCSCube object
        """
        if xy_center is not None and xy_center == 'target':
            xy_center = self.radec_to_xy(self.ra, self.dec).flatten()

        from ..spectroscopy import WCSCube
        return WCSCube.from_cutouts(self, header_id=header_id, influx=influx,
                                    binfactor=binfactor, xy_center=xy_center, **kwargs)

    def to_dataframe(self,  which=['data', 'err'], binfactor=2, filters=None, influx=True, as_cigale=True):
        """
        Get Panda DataFrame from Cutouts

        Parameters
        ----------
        which: string/list of string
            What do you want in your dataframe\n
            Might be 'data', 'err', 'var'\n
            Default is ['data', 'err']

        binfactor: int
            If >1, apply binning on the images data/err/var.\n
            Default is 2.

        filters: string/list of string
            For which filter(s) do you want [which]. \n
            If None, '*', 'all', consider all availbales filters\n
            Default is None

        influx: bool
            Do you want [which] in flux (erg/s/cm2/AA) or in counts\n
            Default is True

        as_cigale: bool
            In case you intend to use this dataframe from Cigale SedFitting, replace '.' by '_'\n
            Default is True

        Returns
        -------
        Pandas DataFrame with ravels datas
        """
        import warnings
        if binfactor is not None:
            binfactor = int(binfactor)
            if binfactor == 1:
                warnings.warn("binfactor=1, this means nothing to do.")
        else:
            binfactor = 1

        from ..utils import array
        import pandas as pd
        df = pd.DataFrame()
        which = which.split() if type(which) == str else which
        filters = filters.split() if type(filters) == str else filters
        if which is None or which in ['*', 'all']:
            which = ['data', 'err']
        if filters is None or filters in ['*', 'all']:
            filters = self.filters

        for w in which:
            to_add = self._get_which_(w, filters, influx)

            if w == 'data':
                if binfactor > 1:
                    to_add = np.sum(array.restride(
                        to_add, (1, binfactor, binfactor)), axis=(-2, -1))
                to_add = to_add.reshape(
                    (to_add.shape[0], to_add.shape[-1]*to_add.shape[-2]))
                df = df.assign(**dict(zip(filters, to_add)))
            elif w in ['err', 'error']:
                if binfactor > 1:
                    to_add = np.sum(array.restride(
                        to_add, (1, binfactor, binfactor)), axis=(-2, -1))
                to_add = to_add.reshape(
                    (to_add.shape[0], to_add.shape[-1]*to_add.shape[-2]))
                df = df.assign(
                    **dict(zip([s + '_' + w for s in filters], to_add)))
            elif w in ['var', 'variance']:
                if binfactor > 1:
                    to_add = np.sum(array.restride(to_add**0.5, (1, binfactor, binfactor)),
                                    axis=(-2, -1))**2
                to_add = to_add.reshape(
                    (to_add.shape[0], to_add.shape[-1]*to_add.shape[-2]))
                df = df.assign(
                    **dict(zip([s + '_' + w for s in filters], to_add)))

        if as_cigale:
            df.columns = df.columns.str.replace(".", "_")

        return df

    # -------- #
    #  SETTER  #
    # -------- #
    def set_instdata(self, instdata, load_wcs=True):
        """ 
        Set Instrument Data

        Parameters
        ----------

        instdata: list of Instrument object 

        load_wcs: bool
            Do you want to load wcs information from Instrument header?

        Returns
        -------
        """
        if instdata is None:
            return

        self._instdata = np.atleast_1d(instdata)
        if self.ninst > 0 and load_wcs:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.load_wcs(self.instdata[0].header)

    def set_radec(self, ra, dec):
        """ 
        Set Right Ascension and Declination

        Parameters
        ----------

        ra, dec: floats
            Position in degrees

        Returns
        -------
        """
        self._ra, self._dec = ra, dec

    # -------- #
    #  GETTER  #
    # -------- #

    def get_index(self, filters=None):
        """ Get cutout index from filter name information.

        Parameters
        ----------
        filters: [String or list of strings]
            Name of the filter(s) (for instance "ps1.r" or ["ps1.g", "ps1.i"])\n
            If filters is None or in ['*', "all"], return all the indices.\n
            Default is None.

        Returns
        -------- 
        list of index

        """
        if filters is None or filters in ["*", "all"]:
            return np.arange(self.ninst)

        return [self.filters.index(f_) for f_ in np.atleast_1d(filters)]

    def get_data(self, filters=None, influx=False):
        """ 
        Get datas from cutouts 

        Parameters
        ----------
        filters : string or list of strings
            Name of the filter(s) (for instance 'ps1.r' or ['ps1.g', 'ps1.i']) \n
            If filters is None or in ['*', 'all'], consider all the available filters.\n
            Default is None.

        influx : bool -optional-
            If True, return datas in flux in erg.s-1.cm-2.AA-1\n
            If False, return datas in counts.\n
            Default is False.

        Returns
        -------- 
        List of array of size [image_size]
        """
        return self._get_which_("data", filters=filters, influx=influx)

    def get_error(self, filters=None, influx=False):
        """ 
        Get errors from cutouts 

        Parameters
        ----------
        filters : string or list of strings
            Name of the filter(s) (for instance 'ps1.r' or ['ps1.g', 'ps1.i'])\n
            If filters is None or in ['*', 'all'], consider all the available filters.\n
            Default is None.

        influx : bool -optional-
            If True, return errors in flux in erg.s-1.cm-2.AA-1\n
            If False, return errors in counts.\n
            Default is False.

        Returns
        -------- 
        List of array of size [image_size]
        """
        return self._get_which_("error", filters=filters, influx=influx)

    def get_variance(self, filters=None, influx=False):
        """ 
        Get variances from cutouts 

        Parameters
        ----------
        filters : String or list of strings
            Name of the filter(s) (for instance 'ps1.r' or ['ps1.g', 'ps1.i'])\n
            If filters is None or in ['*', 'all'], consider all the available filters.\n
            Default is None.

        influx : bool -optional-
            If True, return variances in flux in erg.s-1.cm-2.AA-1\n
            If False, return variances in counts.\n
            Default is False.

        Returns
        -------- 
        List of array of size [image_size]
        """
        return self._get_which_("variance", filters=filters, influx=influx)

    def _get_which_(self, which, filters=None, influx=False):
        """ 
        Get [which] from cutouts 

        Parameters
        ----------

        which: string
            Might be "data", "var"/"variance", "err"/"error"

        filters : string or list of strings
            Name of the filter(s) (for instance 'ps1.r' or ['ps1.g', 'ps1.i'])\n
            If filters is None or in ['*, 'all'], consider all the available filters.\n
            Default is None.

        influx : bool -optional-
            If True, return [which] in flux in erg.s-1.cm-2.AA-1\n
            If False, return [which] in counts.\n
            Default is False.

        Returns
        -------- 
        List of array of size [image_size]
        """

        if which == "data":
            data = self.data.copy()
            coef = 1 if not influx else self.flux_per_count[:, None, None]
        elif which in ["var", "variance"]:
            data = self.variance.copy()
            coef = 1 if not influx else self.flux_per_count[:, None, None]**2
        elif which in ["err", "error"]:
            data = np.sqrt(self.variance.copy())
            coef = 1 if not influx else self.flux_per_count[:, None, None]
        else:
            raise ValueError(
                f"get_which only implemented for 'data', 'variance' or 'error', {which} given")

        # data in flux or counts
        data *= coef
        # returns
        if filters is None or filters in ["*", "all"]:
            return np.asarray(data)

        return np.asarray(data)[self.get_index(filters)]

    # -------- #
    #  Apply   #
    # -------- #
    def extract_sources(self, filter_, thres=2, show=False, savefile=None, figprop={}, **kwargs):
        """ 
        Extract sources datas from cutouts. Use sep package to delimit a threshold area around the object.

        Parameters
        ----------
        filter_: string/list of string
            Which filter(s) do you want to consider?

        thres: float
            Threshold pixel value for detection. \n
            Interpreted as a relative threshold: the absolute threshold at pixel (j, i) will be thresh * err[j, i]\n
            Default is 2.

        show: bool
            Boolean option to show or not the extracted sources with its sep contour\n
            Default is False

        savefile: string
            If *show* == True, save the plot at *savefile*.\n
            Default is None.

        **kwargs:
            Go to sep.extract

        Returns
        -------
        Dataframe of extracted sources.
        """
        import sep
        from astropy import table

        flux = np.squeeze(self.get_data(filters=filter_))
        err = np.squeeze(self.get_error(filters=filter_))

        sources = table.Table(sep.extract(
            flux, thres, err=err, **kwargs)).to_pandas()
        if show:
            self.show(filter_=filter_, sourcedf=sources,
                      savefile=savefile, **figprop)

        return sources
    # -------- #
    # PLOTTER  #
    # -------- #

    def show(self, ax=None, filter_=None, vmin="1", vmax="99",
             sourcedf=None, sourcescale=5, propsource={},
             savefile=None, **kwargs):
        """ 
        Show function for a given filter.

        Parameters
        ----------
        ax: Matplotlib.Axes -optional-
            If given, dim(ax) should be 1.

        filter_: string -optional-
            Which band do you want to plot?\n 
            Default is the first available

        vmin: string, float -optional-
            If string, set colormap scale min below *vmin* percentile.\n
            If float, set colormap scale min below *vmin*.
            Default is '1'.

        vmax: string, float -optional-
            If string, set colormap scale max above *vmax* percentile.\n
            If float, set colormap scale max above *vmax*.
            Default is '99'.

        sourcedf: Pandas.DataFrame -optional-
            Dataframe with extracted source information (see self.extract_sources for instance). \n
            Will draw an Ellipse around the detected sources.

        savefile: string -optional-
            Where do you want to save the plot?\n
            Default is None (not saved)

        Returns
        -------
        Matplotlib.Axes

        """
        import matplotlib.pyplot as mpl
        from ..utils.tools import parse_vmin_vmax
        if filter_ is None:
            filter_ = self.filters[0]
            warnings.warn(f"no filter given, first used: {filter_}")

        flux = np.squeeze(self.get_data(filters=filter_))

        if ax is None:
            fig = mpl.figure(figsize=[6, 6])
            ax = fig.add_subplot(111)
        else:
            fig = ax.figure

        if vmin is None:
            vmin = "1"
        if vmax is None:
            vmax = "99"
        vmin, vmax = parse_vmin_vmax(flux, vmin, vmax)
        prop = dict(origin="lower", vmin=vmin, vmax=vmax, cmap="cividis")
        sc = ax.imshow(flux, **{**prop, **kwargs})

        if sourcedf is not None:
            from .astrometry import get_source_ellipses
            prop = {**dict(facecolor="None", edgecolor="C1"), **propsource}
            e_xy = get_source_ellipses(sourcedf=sourcedf, sourcescale=sourcescale,
                                       system="xy", **prop)
            _ = [ax.add_patch(e_) for e_ in e_xy]

        if savefile is not None:
            fig.savefig(savefile)

        return ax

    # ================ #
    #  Internal        #
    # ================ #

    def _call_down_(self, what, isfunc, index=None, *args, **kwargs):
        """ 
        Get [what] attribut from Instrument object: 

        Parameters
        ----------

        what: String
            Which attribut do you want to get from the intrument object \n
            (for instance 'lbda', 'bandname', 'mab0' ...)

        isfun : bool
            Does the atribut you want is callable

        index : int or list of int -optional-
            Index of the Instrument object to consider (see self.get_index)

        *args,**kwargs: Arguments
            Go to callable attribut if isfunc is True   

        Returns
        -------- 
        Asked attribut for the Instrument object
        """
        if index is None:
            instrus = self.instdata
        else:
            instrus = self.instdata[index]

        if not isfunc:
            return [getattr(s_, what) for s_ in instrus]
        return [getattr(s_, what)(*args, **kwargs) for s_ in instrus]

    def _map_down_(self, method, onwhat, index=None, *args, **kwargs):
        """ call inst_.{method}( inst_.{onwhat}, *args, **kwargs) looping over the instruments """
        if index is None:
            instrus = self.instdata
        else:
            instrus = self.instdata[index]

        return [getattr(s_, method)(getattr(s_, onwhat), *args, **kwargs) for s_ in instrus]

    # ================ #
    #  Properties      #
    # ================ #
    @property
    def instdata(self):
        """ 
        (list of) Instrument object
        """
        return self._instdata

    @property
    def ninst(self):
        """ 
        Number of available Instrument object
        """
        return len(self.instdata)
    #
    # calldown

    @property
    def data(self):
        """ 
        Data available (in counts) for all availables Instrument object
        """
        return self._call_down_("data", isfunc=False)

    @property
    def variance(self):
        """ 
        Variance available (in counts) for all availables Instrument object
        """
        return self._call_down_("var", isfunc=False)

    @property
    def headers(self):
        """ 
        Return DatFrame of the headers for all availables Instrument object
        """
        return pandas.DataFrame([dict(h_) for h_ in self._call_down_("header", isfunc=False)])

    @property
    def filters(self):
        """ 
        List of available filters 
        """
        return self._call_down_("bandname", isfunc=False)

    @property
    def lbda(self):
        """ 
        List of images wavelength
        """
        return self._call_down_("lbda", isfunc=False)

    @property
    def mab0(self):
        """ 
        AB zero point for all the images
        """
        return self._call_down_("mab0", isfunc=False)

    @property
    def flux_per_count(self):
        """ 
        Conversion factor from 1 count to flux in erg.s-1.cm-2.AA-1
        """
        mab0 = np.asarray(self.mab0)
        lbda = np.asarray(self.lbda)
        return 10**(-(2.406+mab0) / 2.5) / (lbda**2)
    #
    # Coordinates

    @property
    def ra(self):
        """ 
        Right ascension in degrees
        """
        return self._ra

    @property
    def dec(self):
        """ 
        Declination in degrees
        """
        return self._dec
