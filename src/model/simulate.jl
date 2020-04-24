#!/usr/bin/env julia

using Fire
using DelimitedFiles


include("simulation/ODEs.jl")

"""
Simulate SEIR. 
https://www.idmod.org/docs/hiv/model-seir.html
R₀ = β / γ
- duration [days]
- β = rate of I->S
- γ = rate of I->R
- σ = rate of E->I
"""
# @main 
function SEIR(o=stdout; duration, S, E=0, I=1, R=0, beta, gamma=1/14, sigma=1/2, dtmax=nothing)
	u₀ = hcat([S, E, I, R]...)
	solution = ODEs.simulate_SEIR(u₀, duration, beta, gamma, sigma; dtmax=dtmax)
	if solution === nothing return end
    writedlm(o, hcat(solution.t, vcat(solution.u...)))
end

