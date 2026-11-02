---
type: concept
title: Perceptron
created: 2026-06-23
tags: [machine-learning, neural-networks]
---

# Perceptron

The simplest neural unit (Frank Rosenblatt, 1958): it multiplies each input by a
weight, adds a bias, and outputs a binary decision based on whether the weighted
sum exceeds zero.

## Notes

The classifier is `output = 1 if (w·x + b) > 0 else 0`. It learns via the
perceptron rule — on a wrong prediction, nudge `weight` by
`learning_rate * error * value` and `bias` by `learning_rate * error`, repeated
over *epochs*. The bias shifts the decision boundary (`x = -bias/weight`) away
from the origin; without it the boundary is stuck at zero and cannot separate
classes whose split lies elsewhere. A single perceptron draws just one straight
line (a linear classifier); stacking such units is the basis of a
[[neural-network|neural network]].

## Sources

- [[the-smallest-brain-you-can-build|The Smallest Brain You Can Build]]
