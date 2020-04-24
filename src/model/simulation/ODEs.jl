#!/usr/bin/env julia

module ODEs
using DifferentialEquations: ODEProblem, solve, ODESolution

export SEIR!

function SEIR!(du, u::AbstractMatrix, t, β, γ, σ)
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
SEIR!(du, u::AbstractVector, t, β, γ, σ) = SEIR!(du, u', t, β, γ, σ)

dSdt(S, I, N, β) = - β .* S .* I ./ N
dEdt(S, E, I, N, β, σ) = β .* S .* I ./ N .- σ .* E
dIdt(E, I, γ, σ) = σ .* E .- γ .* I
dRdt(I, γ) = γ .* I



end;
