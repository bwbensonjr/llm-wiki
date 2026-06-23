---
type: summary
title: "Plotnine: a grammar of graphics for Python"
created: 2026-06-23
source: https://plotnine.org/
raw: raw/2026-06-23-plotnine.md
tags: [data-visualization, python, grammar-of-graphics]
---

# Plotnine: a grammar of graphics for Python

## Summary

[[plotnine|Plotnine]] is a [[python|Python]]
[[data-visualization|data visualization]] library built on the
[[grammar-of-graphics|grammar of graphics]] — a coherent system for *describing*
a plot as composable layers rather than drawing it imperatively. Its API
deliberately mirrors R's [[ggplot2|ggplot2]]: a plot starts with
`ggplot(data, aes(...))` and grows by adding geoms, facets, scales, and themes
with `+`.

The homepage walks through Anscombe's Quartet — four datasets with nearly
identical descriptive statistics but very different shapes — building from a
one-line scatter plot to a fully themed, faceted figure. Along the way it
illustrates the library's selling points: sensible automatic defaults (legends,
color palettes, breaks) that can each be overridden, declarative faceting
instead of `for` loops, and per-layer inheritance of data and column mappings.

## Why this matters

This matters because I am a big fan of ggplot2 and R tidyverse in general. I
haven't fixated on a single Python data visualization library, but I would like
to use plotnine when it makes sense.
