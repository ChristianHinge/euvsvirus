#!/usr/bin/env python3
import numpy as np
from scipy.integrate import odeint


def SEIR(y, t, beta, gamma, sigma):
    """
    :param y: [S, E, I, R]
    :param t: time
    :param beta: rate of S->E
    :param gamma: rate of I->R
    :param sigma: rate of E->I
    """
    S, E, I, R = y
    N = S + E + I + R
    
    dSdt = - beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    
    return dSdt, dEdt, dIdt, dRdt


def SEIR_betas(y, t, beta, gamma, sigma, intervals, interval_betas):
    """
    :param y: [S, E, I, R]
    :param t: time
    :param beta: default beta outside specified intervals
    :param gamma: rate of I->R
    :param sigma: rate of E->I
    :param intervals: inclusive intervals, e.g. [[start0,end0],[start1,end1],...]
    :param interval_betas: beta value for each of the intervals
    """
    for interval, interval_beta in zip(intervals, interval_betas):
        if interval[0] <= t <= interval[1]: return SEIR(y, t, interval_beta, gamma, sigma)
    return SEIR(y, t, beta, gamma, sigma)


def simulate_SEIR(duration, S0, E0=0, I0=1, R0=0, beta=None, gamma=1/14, sigma=1/2):
    assert beta is not None
    y0 = [S0, E0, I0, R0]
    return odeint(SEIR, y0, range(duration), args=(beta, gamma, sigma))


def simulate_SEIR_betas(duration, S0, E0=0, I0=1, R0=0, beta=None, gamma=1/14, sigma=1/2, intervals=None, beta_factors=None):
    """
    :param beta_factors: factor on default beta within each intervals, e.g. higher and lower than 1 for a panic buying interval then a lockdown interval 
    """
    assert beta is not None
    if intervals is None: intervals = []
    if beta_factors is None: interval_betas = []
    else: interval_betas = beta * np.asarray(beta_factors)
    y0 = [S0, E0, I0, R0]
    return odeint(SEIR_betas, y0, range(duration), args=(beta, gamma, sigma, intervals, interval_betas))


# simulate_SEIR(100, S0=100, beta=1/7)

    









