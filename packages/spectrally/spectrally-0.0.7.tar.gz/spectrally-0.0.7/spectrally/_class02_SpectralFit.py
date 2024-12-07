# #!/usr/bin/python3
# -*- coding: utf-8 -*-


import copy


from ._class01_SpectralModel import SpectralModel as Previous
from . import _class02_check_fit as _check_fit
from . import _class02_show as _show
from . import _class02_binning as _binning
from . import _class02_compute_fit as _compute_fit
from . import _class02_plot_valid as _plot_valid
from . import _class02_plot_fit as _plot_fit


__all__ = ['SpectralFit']


#############################################
#############################################
#       Spectral Lines
#############################################


class SpectralFit(Previous):

    _ddef = copy.deepcopy(Previous._ddef)

    # _show_in_summary_core = ['shape', 'ref', 'group']
    _dshow = dict(Previous._dshow)

    _ddef['params']['dobj'] = {
    }

    # ###################
    # -------------------
    # Spectral models
    # -------------------

    def _get_show_obj(self, which=None):
        if which == self._which_fit:
            return _show._show
        else:
            return super()._get_show_obj(which)

    # ###################
    # -------------------
    # Spectral fits
    # -------------------

    # -------------------
    # add spectral fit
    # -------------------

    def add_spectral_fit(
        self,
        # keys
        key=None,
        key_model=None,
        key_data=None,
        key_sigma=None,
        absolute_sigma=None,
        # wavelength
        key_lamb=None,
        # optional 2d fit
        key_bs=None,
        key_bs_vect=None,
        # fit parameters
        dparams=None,
        dvalid=None,
        # compute options
        chain=None,
    ):

        _check_fit._check(
            coll=self,
            # keys
            key=key,
            key_model=key_model,
            key_data=key_data,
            key_sigma=key_sigma,
            absolute_sigma=absolute_sigma,
            # wavelength
            key_lamb=key_lamb,
            # optional 2d fit
            key_bs=key_bs,
            key_bs_vect=key_bs_vect,
            # fit parameters
            dparams=dparams,
            dvalid=dvalid,
            # compute options
            chain=chain,
        )

        return

    # -------------------
    # spectral fit binning
    # -------------------

    def get_spectral_fit_binning_dict(
        self,
        binning=None,
        lamb=None,
        iok=None,
        axis=None,
    ):
        """


        Returns
        -------
        dout: dict
            dict containing all useful parameters for binning

        """
        return _binning.main(
            coll=self,
            binning=binning,
            lamb=lamb,
            iok=iok,
            axis=axis,
        )

    # -------------------
    # compute spectral fit
    # -------------------

    def compute_spectral_fit(
        self,
        key=None,
        # binning
        binning=None,
        # solver options
        solver=None,
        dsolver_options=None,
        # options
        chain=None,
        dscales=None,
        dbounds_low=None,
        dbounds_up=None,
        dx0=None,
        # storing
        store=None,
        overwrite=None,
        # options
        strict=None,
        verb=None,
        timing=None,
    ):

        return _compute_fit.main(
            coll=self,
            key=key,
            # binning
            binning=binning,
            # solver options
            solver=solver,
            dsolver_options=dsolver_options,
            # options
            chain=chain,
            dscales=dscales,
            dbounds_low=dbounds_low,
            dbounds_up=dbounds_up,
            dx0=dx0,
            # storing
            store=store,
            overwrite=overwrite,
            # options
            strict=strict,
            verb=verb,
            timing=timing,
        )

    # ----------------------------------
    # plot spectral fit data validity
    # ----------------------------------

    def plot_spectral_fit_input_validity(
        self,
        key=None,
        keyY=None,
        dref_vectorY=None,
        # options
        dprop=None,
        vmin=None,
        vmax=None,
        cmap=None,
        plot_text=None,
        # figure
        dax=None,
        fs=None,
        dmargin=None,
        tit=None,
        # interactivity
        connect=True,
        dinc=None,
        show_commands=None,
    ):
        """ Plot the validity map if input data


        Parameters
        ----------
        key : str, optional
            DESCRIPTION. The default is None.
        keyY : str, optional
            DESCRIPTION. The default is None.
        dref_vectorY : dict, optional
            DESCRIPTION. The default is None.
        dprop : TYPE, optional
            DESCRIPTION. The default is None.
        vmin : float, optional
            DESCRIPTION. The default is None.
        vmax : float, optional
            DESCRIPTION. The default is None.
        cmap : str, optional
            DESCRIPTION. The default is None.
        plot_text : bool, optional
            DESCRIPTION. The default is None.
        dax : dict, optional
            DESCRIPTION. The default is None.
        fs : tuple, optional
            DESCRIPTION. The default is None.
        dmargin : dict, optional
            DESCRIPTION. The default is None.
        tit : str, optional
            DESCRIPTION. The default is None.
        connect : bool, optional
            DESCRIPTION. The default is True.
        dinc : dict, optional
            DESCRIPTION. The default is None.
        show_commands : bool, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        dax:    Collection
            collection of axes

        """

        return _plot_valid.plot(
            coll=self,
            key=key,
            keyY=keyY,
            dref_vectorY=dref_vectorY,
            # options
            dprop=dprop,
            vmin=vmin,
            vmax=vmax,
            cmap=cmap,
            plot_text=plot_text,
            # figure
            dax=dax,
            fs=fs,
            dmargin=dmargin,
            tit=tit,
            # interactivity
            connect=connect,
            dinc=dinc,
            show_commands=show_commands,
        )

    # ----------------------------
    # plot spectral fit
    # ----------------------------

    def plot_spectral_fit(
        self,
        key=None,
        keyY=None,
        # options
        details=None,
        # uncertainty propagation
        uncertainty_method=None,
        # plotting
        dprop=None,
        vmin=None,
        vmax=None,
        # lines labels
        lines_labels=True,
        lines_labels_color=None,
        lines_labels_rotation=None,
        lines_labels_horizontalalignment=None,
        # figure
        dax=None,
        fs=None,
        dmargin=None,
        tit=None,
        # interactivity
        nmax=None,
        connect=None,
        dinc=None,
        show_commands=None,
        # timing
        timing=None,
    ):

        """ Plot a spectral model using specified data

        lamb can be:
            - a key to an existing vector
            - a user-provided vector (1d np.ndarray)

        """

        return _plot_fit.main(
            coll=self,
            key=key,
            keyY=keyY,
            # options
            details=details,
            # uncertainty propagation
            uncertainty_method=uncertainty_method,
            # plotting
            dprop=dprop,
            vmin=vmin,
            vmax=vmax,
            # lines labels
            lines_labels=lines_labels,
            lines_labels_color=lines_labels_color,
            lines_labels_rotation=lines_labels_rotation,
            lines_labels_horizontalalignment=lines_labels_horizontalalignment,
            # figure
            dax=dax,
            fs=fs,
            dmargin=dmargin,
            tit=tit,
            # interactivity
            nmax=nmax,
            connect=connect,
            dinc=dinc,
            show_commands=show_commands,
            # timing
            timing=timing,
        )