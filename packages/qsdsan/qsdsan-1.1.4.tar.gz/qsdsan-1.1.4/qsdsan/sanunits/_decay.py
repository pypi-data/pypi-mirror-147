#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems

This module is developed by:
    Yalin Li <zoe.yalin.li@gmail.com>

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/main/LICENSE.txt
for license details.
'''


# %%

from math import exp

__all__ = ('Decay',)


class Decay:
    '''For non-steady state degradation.'''

    # Put these as default class attributes
    _t0 = 0
    _COD_max_decay = None
    _decay_k_COD = None
    _MCF_decay = None
    _max_CH4_emission = None
    _N_max_decay = None
    _decay_k_N = None
    _N2O_EF_decay = None

    @staticmethod
    def allocate_N_removal(tot_red, preferred_N):
        '''
        Allocate the total amount of N removal to NH3 and non-NH3 components.

        Parameters
        ----------
        tot_red : float
            Total amount of N to be removed.
        preferred_N : float
            Current content of the N that will be removed first.

        Returns
        -------
        N removal: tuple
            Amount of preferred N to be removed, amount of other N to be removed.
        '''
        if not preferred_N > 0:
            return 0, tot_red
        elif preferred_N > tot_red:
            return tot_red, 0
        else:
            return preferred_N, tot_red-preferred_N


    def first_order_decay(self, k, t, max_decay, t0=None, tot=1):
        r'''
        Calculate first-order degradation loss based on
        `Trimmer et al. <https://doi.org/10.1021/acs.est.0c03296>`_.

        .. math:: C_{deg} = tot * max_{decay}
        .. math:: t_f = t_0 + t
        .. math:: C_{avg} = \frac{C_deg}{k*t} * (e^{-k*t_0}-e^{-k*t_f})
        .. math:: loss = C_{deg} - C_{avg}

        Parameters
        ----------
        k : float
            Degradation rate constant.
        t0 : float
            Degradation time prior to current process.
        t : float
            Degradation time in current process (i.e., tf-t0).
        max_decay : float
            Maximum removal ratio.
        tot : float, optional
            Total degradable amount.
            If set to 1 (default), the return is the relative ratio (i.e., loss/tot).

        Returns
        -------
        loss : float
            Amount lost due to degradation.

        References
        ----------
        [1] Trimmer et al., Navigating Multidimensional Social–Ecological System
        Trade-Offs across Sanitation Alternatives in an Urban Informal Settlement.
        Environ. Sci. Technol. 2020, 54 (19), 12641–12653.
        https://doi.org/10.1021/acs.est.0c03296.
        '''
        t0 = self.t0 if not t0 else t0
        tf = t0 + t
        Cdeg = tot * max_decay
        Cavg = Cdeg/(k*t) * (exp(-k*t0)-exp(-k*tf))
        loss = Cdeg - Cavg
        return loss


    @property
    def t0(self):
        '''[float] Degradation time prior to current process.'''
        return self._t0
    @t0.setter
    def t0(self, i):
        self._t0 = i

    @property
    def COD_max_decay(self):
        '''[float] Maximum fraction of COD removed during storage given sufficient time.'''
        return self._COD_max_decay
    @COD_max_decay.setter
    def COD_max_decay(self, i):
        self._COD_max_decay = i

    @property
    def decay_k_COD(self):
        '''[float] Rate constant for COD decay.'''
        return self._decay_k_COD
    @decay_k_COD.setter
    def decay_k_COD(self, i):
        self._decay_k_COD = i

    @property
    def MCF_decay(self):
        '''[float] Methane correction factor for COD decay.'''
        return self._MCF_decay
    @MCF_decay.setter
    def MCF_decay(self, i):
        self._MCF_decay = i

    @property
    def max_CH4_emission(self):
        '''[float] Maximum methane emssion as a fraction of degraded COD, [g CH4/g COD].'''
        return self._max_CH4_emission
    @max_CH4_emission.setter
    def max_CH4_emission(self, i):
        self._max_CH4_emission = i

    @property
    def N_max_decay(self):
        '''[float] Maximum fraction of N degraded through denitrification during storage given sufficient time.'''
        return self._N_max_decay
    @N_max_decay.setter
    def N_max_decay(self, i):
        self._N_max_decay = i

    @property
    def decay_k_N(self):
        '''[float] Rate constant for N decay.'''
        return self._decay_k_N
    @decay_k_N.setter
    def decay_k_N(self, i):
        self._decay_k_N = i

    @property
    def N2O_EF_decay(self):
        '''[float] Fraction of N emitted as N2O during decay.'''
        return self._N2O_EF_decay
    @N2O_EF_decay.setter
    def N2O_EF_decay(self, i):
        self._N2O_EF_decay = i