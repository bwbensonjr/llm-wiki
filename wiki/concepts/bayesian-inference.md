---
type: concept
title: Bayesian Inference
created: 2026-06-23
tags: [bayesian-statistics]
---

# Bayesian Inference

Reasoning about unknown quantities by placing prior distributions over them and
updating to posterior distributions in light of observed data.

## Notes

The appeal is flexibility: with appropriate priors you can modify nearly any part
of a model to encode your assumptions — for example, treating measured data
coordinates as noisy observations of latent true coordinates — and then use Monte
Carlo methods (MCMC, e.g. the NUTS sampler) to recover parameter estimates.
[[gaussian-process|Gaussian processes]] are a common model component, and tools
like [[pymc|PyMC]] implement the inference machinery.

## Sources

- [[bayesian-modeling-for-unknown-coordinates|Bayesian modeling for unknown coordinates]]
