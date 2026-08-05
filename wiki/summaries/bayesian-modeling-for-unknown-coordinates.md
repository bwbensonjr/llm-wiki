---
type: summary
status: reviewed
title: Bayesian modeling for unknown coordinates
created: 2026-06-23
source: https://christopherkrapu.com/blog/2026/dont-know-where-your-data-is-from/
raw: raw/2026-06-23-don-t-know-where-your-data-is-from-bayesian-modeling-for-unknown-coordinates.md
tags: [bayesian-statistics, gaussian-processes, spatial-statistics]
---

# Bayesian modeling for unknown coordinates

## Summary

A technical walkthrough by [[christopher-krapu|Christopher Krapu]] of
[[bayesian-inference|Bayesian]] [[gaussian-process|Gaussian process]] (GP)
regression for the case where the *locations* of spatial data points are
themselves uncertain — observed only with substantial measurement noise. The
motivating setting is mineral exploration (geologic samples with strong spatial
correlation), illustrated with uranium concentration measurements from the
Walker Lake dataset (Isaaks & Srivastava; distributed with the R `gstat`
package).

Standard GP regression assumes known coordinates. Krapu modifies the model so
each recorded coordinate is a noisy observation of a latent true coordinate,
placing a Gaussian prior (with known scale σ_s representing the assumed level of
location error) on the displacement and evaluating the GP at the latent
coordinates. This is harder than a fixed-location GP because the covariance
matrix changes whenever the latent coordinates move; the implementation uses
[[pymc|PyMC]]'s `pm.gp.Marginal` with a Matérn-5/2 covariance to integrate out
the latent GP values, sampled with NUTS.

Run at increasing noise levels (σ_s = 12, 25, 40 m), the posterior recovers the
main features of the underlying uranium surface even under severe coordinate
perturbation, and each point's posterior location density grows gracefully with
the assumed error. A naive Nadaraya–Watson kernel smoother (bandwidth matched to
the GP length scale) serves as a baseline and yields only a rough average with
little spatial structure. The broader point is methodological: Bayesian modeling
with appropriate priors lets you modify nearly any part of a model to encode your
assumptions, then turn the Monte Carlo crank for reliable estimates.

## Why this matters

I am very interested in understanding the world through data, modeling, and
statistics, and am a big fan of Bayesian methods.
