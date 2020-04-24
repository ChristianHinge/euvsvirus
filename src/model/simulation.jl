#!/usr/bin/env julia

module simulation
using DifferentialEquations: ODEProblem, solve, ODESolution


function simulate(ODEs, u₀::Matrix, duration::Real, args...)
    problem = ODEProblem(ODEs, u₀, (0., duration), args...)
    solve(problem, save_everystep=true)
end



end;
