# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:44:51 2024

@author: dvezinet
"""


import datastock as ds


import numpy as np


# local
from . import _class01_valid as _valid


#############################################
#############################################
#       fit CHECK
#############################################


def _check(
    coll=None,
    # key
    key=None,
    # model
    key_model=None,
    # data and noise
    key_data=None,
    key_sigma=None,
    absolute_sigma=None,
    # wavelength and phi
    key_lamb=None,
    key_bs_vect=None,
    key_bs=None,
    # dict
    dparams=None,
    dvalid=None,
    # compute options
    chain=None,
):

    # ---------------------
    # basic check on inputs
    # ---------------------

    (
        key,
        key_model,
        key_data,
        key_sigma,
        key_lamb,
        key_bs_vect,
        key_bs,
        absolute_sigma,
        # derived
        ref,
        ref0,
        shape,
        shape0,
        axis_lamb,
        axis_bs,
    ) = _check_keys(**locals())

    # ---------------------
    # domain
    # ---------------------

    # prepare ddata
    ddata = {
        key_lamb: {
            'data': coll.ddata[key_lamb]['data'],
            'ref': coll.ddata[key_lamb]['ref'][0],
        }
    }
    if key_bs is not None:
        ddata.update({
            key_bs_vect: {
                'data': coll.ddata[key_bs_vect]['data'],
                'ref': coll.ddata[key_bs_vect]['ref'][0],
            },
        })

    # ---------------------
    # mask & domain
    # ---------------------

    dvalid = _valid.mask_domain(
        # resources
        coll=coll,
        key_data=key_data,
        key_lamb=key_lamb,
        key_bs_vect=key_bs_vect,
        # options
        dvalid=dvalid,
        ref=ref,
        ref0=ref0,
        shape0=shape0,
    )

    # ---------------------
    # validity
    # ---------------------

    dvalid = _valid.valid(
        coll=coll,
        key=key,
        key_data=key_data,
        key_lamb=key_lamb,
        key_bs=key_bs,
        dvalid=dvalid,
        ref=ref,
        ref0=ref0,
    )

    # ---------------------
    # dparams
    # ---------------------

    # if dparams is None:
        # dparams = _dparams.main()

    # # -------- BACKUP ------------
    # # Add dscales, dx0 and dbounds

    # dinput['dscales'] = fit12d_dscales(dscales=dscales, dinput=dinput)
    # dinput['dbounds'] = fit12d_dbounds(dbounds=dbounds, dinput=dinput)
    # dinput['dx0'] = fit12d_dx0(dx0=dx0, dinput=dinput)
    # dinput['dconstants'] = fit12d_dconstants(
        # dconstants=dconstants,
        # dinput=dinput,
    # )

    # ---------------------
    # store
    # ---------------------

    wsf = coll._which_fit
    dobj = {
        wsf: {
            key: {
                'key_model': key_model,
                'key_data': key_data,
                'key_sigma': key_sigma,
                'key_lamb': key_lamb,
                'key_bs': key_bs,
                'key_bs_vect': key_bs_vect,
                'key_sol': None,
                'key_cov': None,
                'absolute_sigma': absolute_sigma,
                'dparams': dparams,
                'dvalid': dvalid,
            },
        },
    }

    coll.update(dobj=dobj)

    return


#############################################
#############################################
#        check keys
#############################################


def _check_keys(
    coll=None,
    # keys
    key=None,
    key_model=None,
    key_data=None,
    key_sigma=None,
    key_lamb=None,
    key_bs_vect=None,
    key_bs=None,
    absolute_sigma=None,
    # unused
    **kwdargs,
):

    # -------------
    # key
    # -------------

    wsf = coll._which_fit
    key = ds._generic_check._obj_key(
        d0=coll.dobj.get(wsf, {}),
        short='sf',
        key=key,
        ndigits=2,
    )

    # -------------
    # key_model
    # -------------

    wsm = coll._which_model
    lok = list(coll.dobj.get(wsm, {}).keys())
    key_model = ds._generic_check._check_var(
        key_model, 'key_model',
        types=str,
        allowed=lok,
    )

    # -------------
    # key_data
    # -------------

    # key_data
    lok = list(coll.ddata.keys())
    key_data = ds._generic_check._check_var(
        key_data, 'key_data',
        types=str,
        allowed=lok,
    )

    # derive refs
    ref = coll.ddata[key_data]['ref']
    shape = coll.ddata[key_data]['shape']

    # -------------
    # key_lamb
    # -------------

    # key_lamb
    lok = [
        k0 for k0, v0 in coll.ddata.items()
        if v0['monot'] == (True,)
        and v0['ref'][0] in ref
    ]
    key_lamb = ds._generic_check._check_var(
        key_lamb, 'key_lamb',
        types=str,
        allowed=lok,
        extra_msg="Should be a 1d vector, strictly monotonous",
    )

    # axis_lamb
    ref_lamb = coll.ddata[key_lamb]['ref'][0]
    axis_lamb = ref.index(ref_lamb)

    # -------------
    # key_sigma
    # -------------

    if key_sigma is None:
        key_sigma = 'poisson'

    # key_sigma
    if isinstance(key_sigma, str):

        # percentage
        c0 = (
            key_sigma[-1] == '%'
            and all([ss.isnumeric() or ss == '.' for ss in key_sigma[:-1]])
        )
        if c0:
            asig_def = True

        else:

            lok_data = [
                k0 for k0, v0 in coll.ddata.items()
                if v0['units'] == coll.ddata[key_data]['units']
                and (
                    v0['ref'] == ref
                    or v0['ref'] == ref_lamb
                )
                and np.all(v0['data'] > 0)
            ]

            lok = list(coll.ddata.keys())
            key_sigma = ds._generic_check._check_var(
                key_sigma, 'key_sigma',
                types=str,
                allowed=lok_data + ['poisson'],
                default='poisson',
                extra_msg=_err_key_sigma(key_sigma, lok=lok, returnas=True),
            )

            asig_def = True

    else:
        key_sigma = float(ds._generic_check._check_var(
            key_sigma, 'key_sigma',
            types=(int, float),
            sign='>0',
            extra_msg=_err_key_sigma(key_sigma, returnas=True),
        ))
        asig_def = True

    # -------------
    # absolute_sigma
    # -------------

    absolute_sigma = ds._generic_check._check_var(
        absolute_sigma, 'absolute_sigma',
        types=bool,
        default=asig_def,
        extra_msg=(
            "Determines whether the error 'key_sigma' should be "
            "understood as a relative or absolute error bar"
        ),
    )

    # -------------
    # key_bs
    # -------------

    c0 = (
        len(ref) >= 2
        and key_bs_vect is not None
    )
    if c0:

        # key_bs_vect
        lok = [
            k0 for k0, v0 in coll.ddata.items()
            if v0['monot'] == (True,)
            and v0['ref'][0] in ref
            and v0['ref'][0] != coll.ddata[key_lamb]['ref'][0]
        ]
        key_bs_vect = ds._generic_check._check_var(
            key_bs_vect, 'key_bs_vect',
            types=str,
            allowed=lok,
        )

        axis_bs = ref.index(coll.ddata[key_bs_vect]['ref'][0])

        # units, dim
        units = coll.ddata[key_bs_vect]['units']
        quant = coll.ddata[key_bs_vect]['quant']
        dim = coll.ddata[key_bs_vect]['dim']

        # key_bs
        wbs = coll._which_bsplines
        lok = [
            k0 for k0, v0 in coll.dobj.get(wbs, {}).items()
            if len(v0['shape']) == 1
            and (
                coll.ddata[v0['apex'][0]]['units'] == units
                or coll.ddata[v0['apex'][0]]['quant'] == quant
                or coll.ddata[v0['apex'][0]]['dim'] == dim
            )
        ]
        key_bs = ds._generic_check._check_var(
            key_bs, 'key_bs',
            types=str,
            allowed=lok,
        )

        # ref0
        ref0 = tuple([
            rr for ii, rr in enumerate(ref)
            if ii in [axis_lamb, axis_bs]
        ])

        # shape0
        shape0 = tuple([
            ss for ii, ss in enumerate(shape)
            if ii in [axis_lamb, axis_bs]
        ])

    else:
        key_bs_vect = None
        key_bs = None
        axis_bs = None
        shape0 = (shape[axis_lamb],)
        ref0 = (ref_lamb,)

    return (
        key,
        key_model,
        key_data,
        key_sigma,
        key_lamb,
        key_bs_vect,
        key_bs,
        absolute_sigma,
        # derived
        ref,
        ref0,
        shape,
        shape0,
        axis_lamb,
        axis_bs,
    )


def _err_key_sigma(key_sigma=None, lok=None, returnas=False):

    msg = (
        "Arg 'key_sigma' must either be:\n"
        "\t- str: a key to a array with:\n"
            "\t\t- same units as key_data\n"
            "\t\t- same ref as key_data or key_lamb\n"
            "\t\t- only strictly positive values\n"
    )
    if lok is not None:
        msg += f"\t\tAvailable:\n\t{lok}\n"

    msg += (
        "\t- 'poisson': poisson statictics (sqrt(data))\n"
        "\t- float or int : constant unique sigma for all data points\n"
        "\t- str: a float with '%' (e.g.: '5.0%'), constant percentage error\n"
        f"\nProvided:\n\t{key_sigma}"
    )

    if returnas is True:
        return msg
    else:
        raise Exception(msg)


# ###########################################
# ###########################################
#        check dinitial
# ###########################################


# def _check_dscales(
    # coll=None,
    # key_model=None,
    # key_data=None,
    # key_lamb=None,
    # dscales=None,
# ):