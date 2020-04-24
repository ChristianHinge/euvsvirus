#!/usr/bin/env julia

module ODEs
using DifferentialEquations: ODEProblem, solve, ODESolution

export SEIR!

function SEIR!(du, u::AbstractMatrix, βγσ, t)
    u .= max.(u, 0)
    S = @view u[:,1]
    E = @view u[:,2]
    I = @view u[:,3]
    R = @view u[:,4]
    N = S .+ E .+ I .+ R
    β, γ, σ = βγσ
    du[:,1] .= dSdt(S, I, N, β)
    du[:,2] .= dEdt(S, E, I, N, β, σ)
    du[:,3] .= dIdt(E, I, γ, σ)
    du[:,4] .= dRdt(I, γ)
end
SEIR!(du, u::AbstractVector, βγσ, t) = SEIR!(du, u', βγσ, t)

dSdt(S, I, N, β) = - β .* S .* I ./ N
dEdt(S, E, I, N, β, σ) = β .* S .* I ./ N .- σ .* E
dIdt(E, I, γ, σ) = σ .* E .- γ .* I
dRdt(I, γ) = γ .* I


function simulate_SEIR(u₀::AbstractArray, duration::Real, β, γ, σ; dtmax=nothing)
    problem = ODEProblem(SEIR!, float(u₀), (0., duration), [β, γ, σ])
    solve(problem, save_everystep=true, dtmax=dtmax)
end



end;
