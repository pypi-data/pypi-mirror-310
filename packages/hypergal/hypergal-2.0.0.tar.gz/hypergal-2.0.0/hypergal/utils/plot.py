import numpy as np
from shapely.geometry import Point
from ..spectroscopy import adr as spectroadr


Mg = 5177
Na = 5896
# https://classic.sdss.org/dr3/products/spectra/vacwavelength.html Vaccum to Air wavelength
Mg = Mg / (1.0 + 2.735182E-4 + 131.4182 / Mg**2 + 2.76249E8 / Mg**4)
Na = Na / (1.0 + 2.735182E-4 + 131.4182 / Na**2 + 2.76249E8 / Na**4)

Hbeta = 4861.333
Halpha = 6562.819
S2_2 = 6730.810
N1 = 7468.310

O3_a = 4932.603
O3_b = 4958.911
O3_c = 5006.843
O3_a = O3_a / (1.0 + 2.735182E-4 + 131.4182 / O3_a**2 + 2.76249E8 / O3_a**4)
O3_b = O3_b / (1.0 + 2.735182E-4 + 131.4182 / O3_b**2 + 2.76249E8 / O3_b**4)
O3_c = O3_c / (1.0 + 2.735182E-4 + 131.4182 / O3_c**2 + 2.76249E8 / O3_c**4)

all_em = np.array([Hbeta, Halpha, S2_2, N1])
all_em_names = [r'$H_{\beta}$', r'$H_{\alpha}$', r'$S[II]$', r'$N[I]$']

O3li = np.array([O3_a, O3_b, O3_c])

all_ab = np.array([Mg, Na])
all_ab_names = [r'$M_g$', r'$N_a$']


def em_lines(z):
    return(z*all_em + all_em)


def o3_lines(z):
    return(z*O3li + O3li)


def ab_lines(z):
    return(z*all_ab + all_ab)


def global_report(datacub, hostmod, snmod, bkgdmod, coutcube, df,
                  fullparam, metaparam, radec, redshift, cubefile,
                  lbda_range, nslices, saveplot=None):
    """ """
    
    from matplotlib.pyplot import cm
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    
    mainlbdarange = lbda_range
    fullmod = datacub.get_new(
        newdata=hostmod.data + snmod.data + bkgdmod.data)
    fullres = datacub.get_new(newdata=datacub.data - fullmod.data)
    hostiso = datacub.get_new(
        newdata=datacub.data - snmod.data - bkgdmod.data)
    sniso = datacub.get_new(
        newdata=datacub.data - hostmod.data - bkgdmod.data, newvariance=datacub.variance)

    mslices = sniso.to_metaslices(
        lbda_ranges=mainlbdarange, nslices=nslices, as_slice=True)
    mslicesmod = snmod.to_metaslices(
        lbda_ranges=mainlbdarange, nslices=nslices, as_slice=True)
    mslicesres = fullres.to_metaslices(
        lbda_ranges=mainlbdarange, nslices=nslices, as_slice=True)

    slid = (abs(metaparam.xs('lbda', level=1)['values']-6500)).idxmin()

    gmsn = psf.GaussMoffat2D()

    alpha = metaparam.loc[slid].xs('alpha_ps')['values']
    eta = metaparam.loc[slid].xs('eta_ps')['values']
    a_ell = metaparam.loc[slid].xs('a_ps')['values']
    b_ell = metaparam.loc[slid].xs('b_ps')['values']
    xoff = metaparam.loc[slid].xs('xoff')['values']
    yoff = metaparam.loc[slid].xs('yoff')['values']
    ampl_ps = metaparam.loc[slid].xs('ampl_ps')['values']
    norm_comp = metaparam.loc[slid].xs('norm_comp')['values']

    gmsn.update_parameters(alpha=alpha, eta=eta, a=a_ell, b=b_ell)

    p = Point(xoff, yoff)
    circle = p.buffer(8)
    idx = mslices[slid].get_spaxels_within_polygon(circle)
    idxmod = mslicesmod[slid].get_spaxels_within_polygon(circle)
    idxsn = idxmod.copy()

    mslice = mslices[slid].get_subslice(idx)
    mslicemod = mslicesmod[slid].get_subslice(idxmod)
    msliceres = mslicesres[slid].get_subslice(idx)

    xsn, ysn = np.transpose(mslice.index_to_xy(mslice.indexes))
    xcsn, ycsn = xoff, yoff
    dxsn = xsn-xcsn
    dysn = ysn-ycsn
    rsn = np.sqrt(dxsn**2 + gmsn.a_ell*dysn**2 + 2*gmsn.b_ell * (dxsn*dysn))

    sndat = mslice.data
    snerr = mslice.variance**0.5

    xgrid, ygrid = np.meshgrid(np.linspace(
        0.2, 10, 100), np.linspace(0.2, 10, 100))
    xc, yc = 0, 0
    dx = xgrid-xc
    dy = ygrid-yc
    rgrid = np.sqrt(dx**2 + gmsn.a_ell*dy**2 + 2*gmsn.b_ell * (dx*dy))

    radiusrav = rgrid.ravel()
    radiusrav.sort()
    radiusrav = radiusrav[::-1]
    profil = gmsn.get_radial_profile(radiusrav)

    x0 = metaparam.xs('xoff', level=1)['values'].values
    x0err = metaparam.xs('xoff', level=1)['errors'].values
    y0 = metaparam.xs('yoff', level=1)['values'].values
    y0err = metaparam.xs('yoff', level=1)['errors'].values
    lbda = metaparam.xs('lbda', level=1)['values'].values

    ADRFitter = spectroadr.ADRFitter(xpos=x0, ypos=y0, xpos_err=x0err, ypos_err=y0err,
                                     lbda=lbda, init_adr=spectroadr.ADR.from_header(datacub.header))

    ADRFitter.fit_adr()

    datacube = datacub.copy()
    modelcube = fullmod.copy()
    lbdamin, lbdamax = (3700, 9300)

    fig = plt.figure(figsize=(30, 20), dpi=75)
    gs = fig.add_gridspec(5, 2, height_ratios=[1, 0.01, 1, 0.25, 1])

    gs0 = gs[0, 0].subgridspec(1, 3)
    gs0bl = gs[1, 0].subgridspec(1, 1)
    gs1 = gs[2, 0].subgridspec(1, 2)
    gs1bl = gs[3, 0].subgridspec(1, 1)
    gs2 = gs[4, 0].subgridspec(1, 3, width_ratios=[1, 0.8, 0.8], wspace=0.5)
    gs3 = gs[0, 1].subgridspec(
        1, 4, width_ratios=[1, 0.6667, 0.6667, 0.6667])
    gs3bl = gs[1, 1].subgridspec(1, 1)
    gs4 = gs[2, 1].subgridspec(1, 1)
    gs4bl = gs[3, 1].subgridspec(1, 1)
    gs5 = gs[4, 1].subgridspec(1, 1)

    axdat = fig.add_subplot(gs0[0, 0])
    axmod = fig.add_subplot(gs0[0, 1])
    axpull = fig.add_subplot(gs0[0, 2])
    axadr = fig.add_subplot(gs1[0, :])

    axhostiso = fig.add_subplot(gs2[0, 0])
    axhostisospec = fig.add_subplot(gs2[0, 1:])

    axsniso = fig.add_subplot(gs3[0, 0])
    axsnisozoom = fig.add_subplot(gs3[0, 1])
    axsnmodzoom = fig.add_subplot(gs3[0, 2])
    axsnreszoom = fig.add_subplot(gs3[0, 3])
    axsnprof = fig.add_subplot(gs4[0, 0])
    axsnspec = fig.add_subplot(gs5[0, 0])

    cmap = cm.viridis
    cmapres = cm.coolwarm
    cmaprms = cm.cividis

    lbdacond = (datacube.lbda > lbdamin) & (datacube.lbda < lbdamax)
    lbdacondrms = (datacube.lbda > 4500) & (datacube.lbda < 8500)

    slicerms = pyifu.spectroscopy.Slice.from_data(data=np.sqrt(len(datacube.data[lbdacondrms])**-1 * np.nansum(((datacube.data[lbdacondrms]-modelcube.data[lbdacondrms])/modelcube.data[lbdacondrms])**2, axis=0)),
                                                  spaxel_mapping=datacube.spaxel_mapping, spaxel_vertices=datacube.spaxel_vertices)

    slicemodel = np.array([np.nanmean(np.delete(modelcube.data[lbdacond].T[i], np.isnan(datacube.data[lbdacond].T[i])))
                           for i in range(len(modelcube.data[lbdacond].T))])

    slicedat = np.array([np.nanmean(np.delete(datacube.data[lbdacond].T[i], np.isnan(datacube.data[lbdacond].T[i])))
                         for i in range(len(datacube.data[lbdacond].T))])

    slice_err = np.sqrt(
        np.nansum(datacube.variance[lbdacond].T, axis=1))/len(datacube.data[lbdacond])
    slicepull = pyifu.spectroscopy.Slice.from_data(data=(slicedat - slicemodel)/(np.sqrt(2)*(
        slice_err)), spaxel_mapping=datacube.spaxel_mapping, spaxel_vertices=datacube.spaxel_vertices, lbda=np.mean(datacube.lbda[lbdacond]))  # PULL
    # slicepull = slicerms##RMS

    vmin = np.nanpercentile(datacube.get_slice(
        lbda_min=mainlbdarange[0], lbda_max=mainlbdarange[1]), 0.5)
    vmax = np.nanpercentile(datacube.get_slice(
        lbda_min=mainlbdarange[0], lbda_max=mainlbdarange[1]), 99.5)

    datacube._display_im_(axim=axdat, vmin=vmin, vmax=vmax,
                          lbdalim=mainlbdarange, cmap=cmap, rasterized=False)
    axdat.scatter(*ADRFitter.refract(ADRFitter.fitted_xref, ADRFitter.fitted_yref,
                  6000), marker='x', color='r', s=32, zorder=10, label='Target')
    if len(df) > 0:
        for n_ in range(len(df)):
            if np.logical_and(*abs(hostiso.wcs.all_world2pix(coutcube.wcs.all_pix2world(np.array([df.x[n_], df.y[n_]])[:, None].T, 0), 0)[0]) < (22, 22)):
                axdat.scatter(*hostiso.wcs.all_world2pix(coutcube.wcs.all_pix2world(np.array([df.x[n_], df.y[n_]])[
                    :, None].T, 0), 0)[0], marker='x', color='k', s=32, zorder=10, label='Host')
    axdat.legend(
        *[*zip(*{l: h for h, l in zip(*axdat.get_legend_handles_labels())}.items())][::-1], loc='lower left')

    modelcube._display_im_(axim=axmod, vmin=vmin, vmax=vmax,
                           lbdalim=mainlbdarange, cmap=cmap, rasterized=False)
    axmod.scatter(*ADRFitter.refract(ADRFitter.fitted_xref,
                  ADRFitter.fitted_yref, 6000), marker='x', color='r', s=32, zorder=10)
    if len(df) > 0:
        for n_ in range(len(df)):
            if np.logical_and(*abs(hostiso.wcs.all_world2pix(coutcube.wcs.all_pix2world(np.array([df.x[n_], df.y[n_]])[:, None].T, 0), 0)[0]) < (22, 22)):
                axmod.scatter(*hostiso.wcs.all_world2pix(coutcube.wcs.all_pix2world(np.array(
                    [df.x[n_], df.y[n_]])[:, None].T, 0), 0)[0], marker='x', color='k', s=32, zorder=10)

    slicepull.show(ax=axpull, show_colorbar=False, vmin=-6,
                   vmax=6, cmap=cmapres, rasterized=False)  # PULL
    # slicepull.show(ax=axpull, show_colorbar=False,vmin=0,vmax=0.15, cmap=cmaprms,rasterized=False); ##RMS

    axdat.set_axis_off()
    axmod.set_axis_off()
    axpull.set_axis_off()

    fraction = 0.05
    norm = mpl.colors.Normalize(vmin=-6, vmax=6)  # PULL
    # norm = mpl.colors.Normalize(vmin=0, vmax=0.15)##RMS
    cbar = axpull.figure.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmapres),  # PULL
        # mpl.cm.ScalarMappable(norm=norm, cmap=cmaprms), ##RMS
        ax=axpull, pad=.05, extend='both', fraction=fraction)

    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cbar = axdat.figure.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
        ax=axdat, pad=.05, extend='both', fraction=fraction)

    cbar = axmod.figure.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
        ax=axmod, pad=.05, extend='both', fraction=fraction)

    cbar.set_label(r'Flux (erg unit)', color="0.5",
                   fontsize="medium", labelpad=10)

    prop = dict(loc="center", color="0.5", fontsize="medium")
    axdat.set_title('SEDM Data', **prop)
    axmod.set_title('Scene Model', **prop)
    axmod.set_aspect('equal')
    axdat.set_aspect('equal')

    axpull.set_title(r'Pull of spectraly integrated spaxels', **prop)
    axpull.set_aspect('equal')

    ADRFitter.show(ax=axadr)
    axadr.set_title(fr'$x_{{ref}}= {np.round(ADRFitter._fit_xref,2)},y_{{ref}}= {np.round(ADRFitter._fit_yref,2)}, \lambda_{{ref}}= {ADRFitter.lbdaref}\AA  $' + '\n' +
                    fr'$Airmass= {np.round( ADRFitter._fit_airmass,2)},Parangle= {np.round( ADRFitter._fit_parangle,0)}  $'
                    + '\n' + f'Input Airmass = {datacub.header["AIRMASS"]}, Input Parangle = {datacub.header["TEL_PA"]}', **prop)

    mu = 0
    sigma = 1
    x = np.linspace(mu - 5*sigma, mu + 5*sigma, 100)

    if len(df) > 0:
        hostmodonly = hostmod.get_extsource_cube(
            df, wcsin=coutcube.wcs, wcsout=hostiso.wcs, sourcescale=5, )
        hostobsonly = hostiso.get_extsource_cube(
            df, wcsin=coutcube.wcs, wcsout=hostiso.wcs, sourcescale=5, )
        x, y = np.transpose(hostobsonly.index_to_xy(hostobsonly.indexes))

        flagin = (hostobsonly.lbda > 4000) & (hostobsonly.lbda < 9300)

        # axhostisospec.plot(hostmodonly.lbda[flagin], np.nanmean(
        #    hostmodonly.data[flagin].T, axis=0), c='r', label='Host Model')
        axhostisospec.plot(hostobsonly.lbda[flagin], np.nanmean(
            hostobsonly.data[flagin].T, axis=0), label='Host isolated')
        axhostisospec.fill_between(hostobsonly.lbda[flagin], np.nanmean(hostobsonly.data[flagin].T, axis=0) - (np.nanmean(hostobsonly.variance[flagin].T, axis=0)/len(hostobsonly.lbda[flagin]))**0.5,
                                   np.nanmean(hostobsonly.data[flagin].T, axis=0) + (np.nanmean(hostobsonly.variance[flagin].T, axis=0)/len(hostobsonly.lbda[flagin]))**0.5, alpha=0.5)

    vmin = np.nanpercentile(hostiso.get_slice(
        lbda_min=mainlbdarange[0], lbda_max=mainlbdarange[1]), 0.5)
    vmax = np.nanpercentile(hostiso.get_slice(
        lbda_min=mainlbdarange[0], lbda_max=mainlbdarange[1]), 99.5)

    hostiso._display_im_(
        axim=axhostiso, lbdalim=mainlbdarange, vmin=vmin, vmax=vmax)
    axhostiso.set_aspect('equal')
    if len(df) > 0:
        axhostiso.scatter(x, y, c='k', marker='D', s=4)
        prop = dict(loc="center", color="0.5", fontsize="medium")
        axhostiso.set_title(
            'Host isolated : Data - SNmodel - BKGmodel', **prop)
        axhostisospec.set_xlabel(r'Wavelength($\AA$)')
        axhostisospec.set_ylabel(r'Flux ($erg.s^{-1}.cm^{-2}.\AA^{-1}$)')

        xemlines_gal = em_lines(redshift)
        idx = [(np.abs(hostobsonly.lbda[flagin]-xl)).argmin()
               for xl in xemlines_gal]
        yemlines_gal = np.nanmean(hostobsonly.data[flagin].T, axis=0)[idx]

        xo3lines_gal = o3_lines(redshift)
        idx = [(np.abs(hostobsonly.lbda[flagin]-xl)).argmin()
               for xl in xo3lines_gal]
        yo3lines_gal = np.nanmean(hostobsonly.data[flagin].T, axis=0)[idx]
        xo3lines_gal = xo3lines_gal[yo3lines_gal.argmax()]
        yo3lines_gal = np.max(yo3lines_gal)

        xablines_gal = ab_lines(redshift)
        idx = [(np.abs(hostobsonly.lbda[flagin]-xl)).argmin()
               for xl in xablines_gal]
        yablines_gal = np.nanmean(hostobsonly.data[flagin].T, axis=0)[idx]

        axhostisospec.vlines(em_lines(redshift), ymin=yemlines_gal + 0.1*np.median(np.nanmean(hostmodonly.data[flagin].T, axis=0)), ymax=yemlines_gal + 0.15*np.median(
            np.nanmean(hostmodonly.data[flagin].T, axis=0)), color='k', alpha=0.5, ls='--', label='EM/AB lines' + '\n' + f'Input z={np.round(redshift,4)}')
        axhostisospec.vlines(ab_lines(redshift), ymin=yablines_gal - 0.1*np.median(np.nanmean(
            hostmodonly.data[flagin].T, axis=0)), ymax=yablines_gal - 0.15*np.median(np.nanmean(hostmodonly.data[flagin].T, axis=0)), color='k', alpha=0.5, ls='--')
        axhostisospec.vlines(xo3lines_gal, ymin=yo3lines_gal + 0.1*np.median(np.nanmean(hostmodonly.data[flagin].T, axis=0)), ymax=yo3lines_gal + 0.15*np.median(
            np.nanmean(hostmodonly.data[flagin].T, axis=0)), color='k', alpha=0.5, ls='--')
        for l in range(len(all_em_names)):
            axhostisospec.text(em_lines(redshift)[l], yemlines_gal[l] + 0.17*np.median(np.nanmean(
                hostmodonly.data[flagin].T, axis=0)), all_em_names[l], ha='center', va='center')

        axhostisospec.text(xo3lines_gal, yo3lines_gal + 0.17*np.median(np.nanmean(
            hostmodonly.data[flagin].T, axis=0)), r'$O[III]$', ha='center', va='center')

        for l in range(len(all_ab_names)):
            axhostisospec.text(ab_lines(redshift)[l], yablines_gal[l] - 0.17*np.median(np.nanmean(
                hostmodonly.data[flagin].T, axis=0)), all_ab_names[l], ha='center', va='center')
        axhostisospec.legend()
        axhostiso.set_axis_off()

    rms_cub = snmod.get_new(newdata=fullres.data / fullmod.data)
    rms_subcub = rms_cub.get_partial_cube(rms_cub.indexes, np.argwhere(
        (datacub.lbda > 5000) & (datacub.lbda < 8500)).squeeze())
    rms_slice = pyifu.spectroscopy.Slice.from_data(data=np.sqrt(len(rms_subcub.data)**-1 * np.nansum((rms_subcub.data)**2, axis=0)),
                                                   spaxel_mapping=rms_subcub.spaxel_mapping, spaxel_vertices=rms_subcub.spaxel_vertices, lbda=np.mean(datacub.lbda[(datacub.lbda > 5000) & (datacub.lbda < 8500)]))

    p = Point(xoff, yoff)
    circle = p.buffer(8)
    idx = rms_slice.get_spaxels_within_polygon(circle)
    rms_slice_sub = rms_slice.get_subslice(idx)

    sl_subpull = slicepull.get_subslice(idx)

    sniso._display_im_(axim=axsniso, lbdalim=mainlbdarange)
    axsniso.set_aspect('equal')
    axsniso.scatter(xsn, ysn, c='k', marker='D', s=4)
    axsniso.set_title('SN isolated : Data - Hostmodel - BKGmodel', **prop)
    axsniso.set_axis_off()

    sniso.get_partial_cube(idx, np.arange(len(sniso.lbda)))._display_im_(
        axim=axsnisozoom, vmax='95', vmin='10', lbdalim=mainlbdarange, rasterized=False)
    axsnisozoom.set_aspect('equal')
    axsnisozoom.set_title('SN isolated', **prop)
    axsnisozoom.set_axis_off()

    snmod.get_partial_cube(idx, np.arange(len(snmod.lbda)))._display_im_(
        axim=axsnmodzoom, vmax='95', vmin='10', lbdalim=mainlbdarange, rasterized=False)
    axsnmodzoom.set_aspect('equal')
    axsnmodzoom.set_title('Model', **prop)
    axsnmodzoom.set_axis_off()

    # rms_slice_sub.show(ax=axsnreszoom, cmap=cmaprms, vmin=0, vmax=0.15, show_colorbar=False); ##RMS
    sl_subpull.show(ax=axsnreszoom, cmap=cmapres,
                    vmin=-6, vmax=6, show_colorbar=False)
    axsnreszoom.set_axis_off()
    axsnreszoom.set_aspect('equal')
    axsnreszoom.set_title(r'Pull', **prop)

    # norm = mpl.colors.Normalize(vmin=0, vmax=0.15)##RMS
    norm = mpl.colors.Normalize(vmin=-6, vmax=6)  # PULL
    cbar = axsnreszoom.figure.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmapres),  # PULL
        # mpl.cm.ScalarMappable(norm=norm, cmap=cmaprms), ##RMS
        ax=axsnreszoom, pad=.05, extend='both', fraction=fraction)

    axsnprof.plot(radiusrav, profil*ampl_ps*norm_comp /
                  np.max(profil*ampl_ps*norm_comp), label="Gaussian + Moffat model", c='r')
    axsnprof.scatter(rsn, sndat/np.max(profil*ampl_ps *
                     norm_comp), c='k', label="Datas", s=16)
    axsnprof.errorbar(rsn, sndat/np.max(profil*ampl_ps*norm_comp), snerr /
                      np.max(profil*ampl_ps*norm_comp), fmt='none', c='k')

    axsnprof.set_xlim(np.min(rsn)-0.1, 8)
    axsnprof.set_ylim(-0.5, 1.5)
    axsnprof.set_xlabel('Elliptical Radius (spx)')
    axsnprof.set_ylabel(' Flux (normalized) ')
    axsnprof.set_title(
        fr'SN profile with Gaussian + Moffat model (from Metaslice at {np.round(mslice.lbda,0)} $\AA$)', **prop)
    axsnprof.vlines(radiusrav[np.where(abs(profil*ampl_ps*norm_comp/np.max(profil*ampl_ps*norm_comp) - 0.5) == np.min(abs(profil*ampl_ps*norm_comp/np.max(profil*ampl_ps*norm_comp) - 0.5)))[0]], -0.5, 1.5, ls='--', color='b', alpha=0.5,
                    label=fr'fitted FWHM={np.round(radiusrav[np.where(abs(profil*ampl_ps*norm_comp/np.max(sndat) -0.5) == np.min(abs(profil*ampl_ps*norm_comp/np.max(sndat) - 0.5)))[0]][0]*2*0.558,2)} " (1spx = 0.558")')
    axsnprof.legend()

    speccoef = fullparam.xs('norm_comp', level=1)['values'].values
    specval = fullparam.xs('ampl_ps', level=1)[
        'values'].values * speccoef/datacub.header['EXPTIME']
    specerr = fullparam.xs('ampl_ps', level=1)[
        'errors'].values*speccoef/datacub.header['EXPTIME']
    speclbda = fullparam.xs('lbda', level=1)['values'].values

    axsnspec.plot(speclbda, specval, label='Target model spectra ')
    axsnspec.fill_between(speclbda, specval+specerr,
                          specval-specerr, alpha=0.3)
    axsnspec.set_xlim(3800, 9300)
    axsnspec.set_ylim(
        0, np.max(specval[(speclbda > 3800) & (speclbda < 9300)]))
    axsnspec.set_xlabel(r'Wavelength($\AA$)')
    axsnspec.set_ylabel(r'Flux($ erg.s^{1}.cm^{-2}.\AA^{-1}$)')
    axsnspec.set_title('Target model spectra', **prop)

    l1t, l1b = gs1bl.get_grid_positions(
        fig)[0]+0.01, gs1bl.get_grid_positions(fig)[1]-0.01
    line = plt.Line2D((.1, .48), (l1b, l1b), color="k", linewidth=1.5)
    fig.add_artist(line)
    fig.text(0.29, (2*l1t+l1b)/3, 'Host Spectrum', fontsize=14, ha='center')
    line2 = plt.Line2D((.1, .48), (l1t, l1t), color="k", linewidth=1.5)
    fig.add_artist(line2)

    lgt, lgb = gs0.get_grid_positions(
        fig)[1]+0.05, gs0.get_grid_positions(fig)[1]+0.03
    lineg = plt.Line2D((.1, .48), (lgb, lgb), color="k", linewidth=1.5)
    fig.add_artist(lineg)
    fig.text(0.29, (lgt+2*lgb)/3, 'Global view', fontsize=14, ha='center')
    line2g = plt.Line2D((.1, .48), (lgt, lgt), color="k", linewidth=1.5)
    fig.add_artist(line2g)

    l3t, l3b = lgt, lgb
    line3 = plt.Line2D((.52, .9), (l3b, l3b), color="k", linewidth=1.5)
    fig.add_artist(line3)
    fig.text(0.71, (lgt+2*lgb)/3, 'SN Spectrum', fontsize=14, ha='center')
    line4 = plt.Line2D((.52, .9), (l3t, l3t), color="k", linewidth=1.5)
    fig.add_artist(line4)

    linesep = plt.Line2D((.5, .5), (lgb, gs2.get_grid_positions(fig)[
                         0]), color="k", linewidth=1.5)
    fig.add_artist(linesep)

    import datetime
    import hypergal
    fig.text(
        0.5, 0.01, f"hypergal version {hypergal.__version__} | made the {datetime.datetime.now().date().isoformat()} | J.Lezmy (lezmy@ipnl.in2p3.fr)", ha='center', color='grey', fontsize=10)
    fig.suptitle(
        datacube.header['NAME'] + fr' ({datacube.header["OBSDATE"]} , ID: {datacube.header["OBSTIME"].rsplit(".")[0].replace(":","-")})', fontsize=16, fontweight="bold", y=0.97)

    if saveplot is not None:
        fig.savefig(saveplot)
    else:
        return fig
