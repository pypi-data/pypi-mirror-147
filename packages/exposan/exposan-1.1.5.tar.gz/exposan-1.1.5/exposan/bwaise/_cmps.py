#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
EXPOsan: Exposition of sanitation and resource recovery systems

This module is developed by:
    Yalin Li <zoe.yalin.li@gmail.com>

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/EXPOsan/blob/main/LICENSE.txt
for license details.

Ref:
    [1] Trimmer et al., Navigating Multidimensional Social–Ecological System
        Trade-Offs across Sanitation Alternatives in an Urban Informal Settlement.
        Environ. Sci. Technol. 2020, 54 (19), 12641–12653.
        https://doi.org/10.1021/acs.est.0c03296.

'''


# %%

from thermosteam.functional import rho_to_V
from qsdsan import Chemical, Component, Components

__all__ = ('cmps', )

NH3 = Component('NH3', measured_as='N',
                phase='l', particle_size='Soluble',
                degradability='Undegradable', organic=False)

NonNH3 = Component('NonNH3', search_ID='N', measured_as='N',
                   phase='l', particle_size='Soluble',
                   degradability='Undegradable', organic=False,
                   description='Non-NH3 nitrogen')

P = Component('P', phase='l', particle_size='Soluble',
              degradability='Undegradable', organic=False)

K = Component('K', phase='l', particle_size='Soluble',
              degradability='Undegradable', organic=False)

Mg = Component('Mg', phase='l', particle_size='Soluble',
               degradability='Undegradable', organic=False)

Ca = Component('Ca', phase='l', particle_size='Soluble',
               degradability='Undegradable', organic=False)

H2O = Component('H2O', phase='l', particle_size='Soluble',
                degradability='Undegradable', organic=False)

OtherSS = Component('OtherSS', phase='l', particle_size='Soluble',
                    degradability='Undegradable', organic=False,
                    description='Unspecified soluble solids')

N2O = Component('N2O', phase='g', particle_size='Dissolved gas',
                degradability='Undegradable', organic=False)

CH4 = Component('CH4', phase='g', particle_size='Dissolved gas',
                degradability='Slowly', organic=True)

# Below three are for combustion reactions
O2 = Component('O2', phase='g', particle_size='Dissolved gas',
               degradability='Undegradable', organic=False)

N2 = Component('N2', phase='g', particle_size='Dissolved gas',
               degradability='Undegradable', organic=False)

CO2 = Component('CO2', phase='g', particle_size='Dissolved gas',
                degradability='Undegradable', organic=False)

P4O10 = Component.from_chemical('P4O10', Chemical('P4O10'),
                                phase='s', particle_size='Particulate',
                                degradability='Undegradable', organic=False)
# The following will lead to an error as it won't be able to copy the V model
# P4O10 = Component('P4O10', phase='s', particle_size='Particulate',
#                   degradability='Undegradable', organic=False)

def add_V_from_rho(cmp, rho):
    V_model = rho_to_V(rho, cmp.MW)
    try: cmp.V.add_model(V_model)
    except:
        handle = getattr(cmp.V, cmp.locked_state)
        handle.add_model(V_model)

Tissue = Component('Tissue', MW=1, phase='s', particle_size='Particulate',
                    degradability='Undegradable', organic=False,
                    description='Tissue for toilet paper')
# 375 kg/m3 is the average of 250-500 for tissue from
# https://paperonweb.com/density.htm (accessed 2020-11-12)
add_V_from_rho(Tissue, 375)

WoodAsh = Component('WoodAsh', MW=1, phase='s', i_Mg=0.0224, i_Ca=0.3034,
                    particle_size='Particulate', degradability='Undegradable',
                    organic=False, description='Wood ash for desiccant')
add_V_from_rho(WoodAsh, 760)

for i in (Tissue, WoodAsh):
    i.copy_models_from(Chemical('Glucose'), ('Cn', 'mu'))

Struvite = Component('Struvite', search_ID='MagnesiumAmmoniumPhosphate',
                     formula='NH4MgPO4·H12O6',
                     phase='s', particle_size='Particulate',
                     degradability='Undegradable', organic=False)
# http://www.chemspider.com/Chemical-Structure.8396003.html (accessed 2020-11-19)
add_V_from_rho(Struvite, 1711)

HAP = Component('HAP', search_ID='Hydroxyapatite',
                phase='s', particle_size='Particulate',
                degradability='Undegradable', organic=False)
# Taking the average of 3.1-3.2 g/cm3 from
# https://pubchem.ncbi.nlm.nih.gov/compound/Hydroxyapatite (accessed 2020-11-19)
add_V_from_rho(HAP, 3150)

for cmp in (NonNH3, P, K, Mg, Ca, OtherSS):
    cmp.default()
    cmp.copy_models_from(H2O, ('sigma', 'epsilon', 'kappa', 'Cn', 'mu'))
    add_V_from_rho(cmp, 1e3) # assume the same density as water

cmps = Components((NH3, NonNH3, P, K, Mg, Ca, H2O, OtherSS, N2O, CH4, O2, N2,
                   CO2, P4O10, Tissue, WoodAsh, Struvite, HAP))
for i in cmps:
    if i.HHV is None: i.HHV = 0
    if i.LHV is None: i.LHV = 0
    if i.Hf is None: i.Hf = 0
cmps.compile()

cmps.set_synonym('H2O', 'Water')