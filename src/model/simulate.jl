#!/usr/bin/env julia

using ArgParse
using DelimitedFiles


include("utilities/ArgParseUtils.jl")
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
function SEIR(o=stdout; duration, S, E=0, I=1, R=0, beta, gamma=1/14, sigma=1/2, dtmax=nothing)
	u₀ = hcat([S, E, I, R]...)
	solution = ODEs.simulate_SEIR(u₀, duration, beta, gamma, sigma; dtmax=dtmax)
	if solution === nothing return end
    writedlm(o, hcat(solution.t, vcat(solution.u...)))
end



function argument_parser()
	s = ArgParseSettings(description="Simulate pandemic ODE.", autofix_names=true)
	@add_arg_table! s begin
		"o"
			default = stdout
			help = "Output filename."
		"-t", "--duration"
			arg_type = Int
			range_tester = x -> x > 0
			help = "Simulation duration [days]."
			required = true
		"-S"
			arg_type = Int
			range_tester = x -> x > 0
			help = "Initial number of suscebtible people."
			required = true
		"-E"
			arg_type = Int
			range_tester = x -> x >= 0
			default = 0
			help = ""
		"-I"
			arg_type = Int
			range_tester = x -> x > 0
			default = 1
			help = ""
		"-R"
			arg_type = Int
			range_tester = x -> x >= 0
			default = 0
			help = ""
		"-b", "--beta"
			arg_type = Real
			range_tester = x -> x > 0
			required = true
			help = "rate of I->S"
		"-g", "--gamma"
			arg_type = Real
			range_tester = x -> x > 0
			default = 1/14
			help = "rate of I->R"
		"-s", "--sigma"
			arg_type = Real
			range_tester = x -> x > 0
			default = 1/2
			help = "rate of E->I"
		"--dtmax"
			arg_type = Int
			range_tester = x -> x > 0
			default = 100
			help = "Max dt (time step)."
		
	end
	s
end

ArgParseUtils.main(argument_parser(), SEIR)
