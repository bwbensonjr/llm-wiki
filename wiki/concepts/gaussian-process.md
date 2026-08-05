---
type: concept
status: reviewed
title: Gaussian Process
created: 2026-06-23
tags: [gaussian-processes, bayesian-statistics]
---

# Gaussian Process

A distribution over functions used as a flexible prior in regression, where any
finite set of points is jointly Gaussian with covariance set by a kernel (GP).

## Notes

Widely used in spatial statistics, robotics, and neuroscience. The covariance
kernel (e.g. Matérn-5/2) encodes smoothness and a length scale. In
[[bayesian-inference|Bayesian]] GP regression the latent function values can be
integrated out (marginalized); [[christopher-krapu|Christopher Krapu]] extends the
standard fixed-location model to the case of uncertain input coordinates, where
the covariance matrix changes as the latent locations move. Implemented in that
example with [[pymc|PyMC]]'s `pm.gp.Marginal`.

## Sources

- [[bayesian-modeling-for-unknown-coordinates|Bayesian modeling for unknown coordinates]]
