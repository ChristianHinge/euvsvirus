#!/usr/bin/env julia

module ODEs
using DifferentialEquations: ODEProblem, solve, ODESolution


function SEIR!(du, u::Matrix, t, β, γ, σ)
    S = @view u[:,1]
    E = @view u[:,2]
    I = @view u[:,3]
    R = @view u[:,4]
    N = S .+ E .+ I .+ R
    du[:,1] .= dSdt(S, I, N, β)
    du[:,2] .= dEdt(S, E, I, N, β, σ)
    du[:,3] .= dIdt(E, I, γ, σ)
    du[:,4] .= dRdt(I, γ)
end

dSdt(S, I, N, β) = - β .* S .* I ./ N
dEdt(S, E, I, N, β, σ) = β .* S .* I ./ N .- σ .* E
dIdt(E, I, γ, σ) = σ .* E .- γ .* I
dRdt(I, γ) = γ .* I

function simulate_SEIR(u₀::Matrix, duration::Real, β, γ, σ)
    problem = ODEProblem(SEIR!, u₀, (0., duration), β, γ, σ)
    solve(problem, save_everystep=true)
end



end;
