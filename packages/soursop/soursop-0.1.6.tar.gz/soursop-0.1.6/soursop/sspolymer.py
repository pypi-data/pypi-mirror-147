import numpy as np


def get_overlap_concentration(rg):
    """
    Function that takes the radius of gyration (Rg) in angstroms and returns 
    overlap concentration in molar units.

    The overlap concentration reflects the concentration at which a flexible
    polymer begins to 'collide' in trans with other polymers - i.e. the 
    concentration at which the chains begin to overlap.

    Parameters
    ----------

    rg : float
       Radius of gyration in Angstroms

    Return
    ------
    
    float 
        The overlap concentration in molar units

    """
    
    # Avogadro's number!
    Na = 6.023e23

    # get rg in meters (convert from Angstroms to meters)
    rg = rg*1e-10
        
    # get volume in m3
    v_m3=((4/3)*np.pi*np.power(rg, 3))
    
    # get volume in liters
    v_l = v_m3*1000
    
    # get concentration
    c = (1/(v_l))/Na

    return c
