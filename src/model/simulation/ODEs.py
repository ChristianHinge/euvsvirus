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
    _interval_betas = []
    for interval, interval_beta in zip(intervals, interval_betas):
        if interval[0] <= t <= interval[1]: _interval_betas.append(interval_beta)
    if len(_interval_betas) > 0: beta = np.mean(_interval_betas)
    return SEIR(y, t, beta, gamma, sigma)


def simulate_SEIR(duration, S0, E0=0, I0=1, R0=0, beta=None, gamma=1/14, sigma=1/2):
    assert beta is not None
    y0 = [S0, E0, I0, R0]
    return _eradication(odeint(SEIR, y0, range(duration), args=(beta, gamma, sigma)))


def simulate_SEIR_betas(duration, S0, E0=0, I0=1, R0=0, beta=None, gamma=1/14, sigma=1/2, intervals=None, beta_factors=None):
    """
    :param beta_factors: factor on default beta within each intervals, e.g. higher and lower than 1 for a panic buying interval then a lockdown interval 
    """
    assert beta is not None
    if intervals is None: intervals = []
    if beta_factors is None: interval_betas = []
    else: interval_betas = beta * np.asarray(beta_factors)
    y0 = [S0, E0, I0, R0]
    return _eradication(odeint(SEIR_betas, y0, range(duration), args=(beta, gamma, sigma, intervals, interval_betas)))


def _eradication(solution):
    idx = np.where(solution[:, 2] < 0.9)[0]
    if len(idx) > 0:
        idx = idx[0]
        # move remaining E and I to R
        solution[idx, 3] += sum(solution[idx, 1:3])
        solution[idx, 1:3] = 0  # remove E and I
        solution[idx+1:,] = solution[idx,]  # everything is static
    return solution


