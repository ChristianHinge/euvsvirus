#!/usr/bin/env python3
from scipy.integrate import odeint


def SEIR(y, t, beta, gamma, sigma):
    S, E, I, R = y
    N = S + E + I + R
    
    dSdt = - beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    
    return dSdt, dEdt, dIdt, dRdt


def simulate_SEIR(duration, S0, E0=0, I0=1, R0=0, beta=None, gamma=1/14, sigma=1/2):
    assert beta is not None
    y0 = [S0, E0, I0, R0]
    return odeint(SEIR, y0, range(duration), args=(beta, gamma, sigma))


# simulate_SEIR(100, S0=100, beta=1/7)

    









