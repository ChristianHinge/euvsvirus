#!/usr/bin/env julia

using Fire


include("simulation/ODEs.jl")
include("simulation/Simulation.jl")

"""
Simulate SEIR. 
https://www.idmod.org/docs/hiv/model-seir.html
R₀ = β / γ
- duration [days]
- β = rate of I->S
- γ = rate of I->R
- σ = rate of E->I
"""
@main function SEIR(; duration, S, E=0, I=1, R=0, beta, gamma=1/14, sigma=1/2)
	u₀ = hcat([S, E, I, R]...)
	solution = Simulation.simulate(ODEs.SEIR!, u₀, duration)
	if solution === nothing return end
    print(solution)
end

