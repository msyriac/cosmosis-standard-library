from cosmosis.datablock import option_section, names
#from scipy.interpolate import interp1d
import numpy as np
import pdb

def get_nbins(block, section):
    if block.has_value(section, "nbin_a"):
        n_a=block[section,"nbin_a"]
        n_b=block[section,"nbin_b"]
    else:
        n_a=block[section,"nbin"]
        n_b=n_a
    return n_a, n_b


def apply_lcut(block, section, Lmin, Lmax):
    n_other, n_cmb = get_nbins(block, section)
    if (n_cmb != 1):
        raise ValueError("Found more than 1 CMB bin - there is definitely only 1 CMB.")

    ell = block[section, 'ell']
    w   = np.ones(ell.shape[0])
    w[ell<Lmin]=0
    w[np.where(ell>Lmax)[0][1:]]=0
    for bini in xrange(0,n_other):
        C_ell_orig = block[section, 'bin_' + str(bini+1) + '_' + str(1)]
        beamed_C_ell = C_ell_orig*w
        block[section, 'bin_' + str(bini+1) + '_' + str(1)] = beamed_C_ell

def setup(options):
    shearkappa_section = options.get_string(option_section, "shearkappa_section", default="shear_cmbkappa_cl")
    galkappa_section = options.get_string(option_section, "galkappa_section", default="galaxy_cmbkappa_cl")

    if options.has_value(option_section, 'beam_sigma_arcmin'):
        beam_sigma_arcmin = options[option_section, "beam_sigma_arcmin"]
        # radians
        beam_sigma = (1./60.0)*(np.pi/180.)*beam_sigma_arcmin
    
    elif options.has_value(option_section, 'beam_fwhm_arcmin'):
        beam_fwhm_arcmin = options[option_section, "beam_fwhm_arcmin"]
        beam_sigma = (1./np.sqrt(8.*np.log(2.)))*(1./60.0)*(np.pi/180.)*beam_fwhm_arcmin
    else:
        raise ValueError("No beam_sigma_arcmin or beam_fwhm_armcin supplied!")


    return {"shearkappa_section":shearkappa_section, "galkappa_section":galkappa_section, "beam_sigma":beam_sigma}

def execute(block, config):
    shearkappa_section = config['shearkappa_section']
    galkappa_section = config['galkappa_section']
    beam_sigma = config['beam_sigma']

    if block.has_section(galkappa_section):
        apply_lcut(block, galkappa_section, beam_sigma)


    if block.has_section(shearkappa_section):
        apply_lcut(block, shearkappa_section, beam_sigma)
        
    return 0

def cleanup(config):
    pass
