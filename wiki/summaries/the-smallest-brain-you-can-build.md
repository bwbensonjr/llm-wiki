---
type: summary
status: reviewed
title: The Smallest Brain You Can Build
created: 2026-06-23
source: https://ranpara.net/posts/perceptron-explained-from-scratch/
raw: raw/2026-06-23-the-smallest-brain-you-can-build.md
tags: [machine-learning, neural-networks, python]
---

# The Smallest Brain You Can Build

## Summary

A beginner-friendly, math-light walkthrough (from ranpara.net) that builds a
[[perceptron]] — "the smallest brain you can build" — from scratch in
[[python|Python]] and trains it live in the browser. Framed as the seed of every
modern [[neural-network|neural network]], the perceptron takes inputs,
multiplies each by a weight, adds a bias, and outputs a yes/no decision:
`output = 1 if (w·x + b) > 0 else 0` (Frank Rosenblatt, 1958), by analogy to a
neuron firing.

It develops the idea through concrete examples: a **human decision** (John Doe
weighing a job offer) motivates inputs, weights, and a threshold; **"is this
number positive?"** is the simplest one-input classifier, trained by the
perceptron learning rule (`weight += learning_rate * error * value`,
`bias += learning_rate * error`), where one full pass is an *epoch* and repeating
epochs is *training*. The **decision boundary** sits where `w·x + b = 0`, i.e.
`x = -bias/weight`.

**Why bias matters:** in a student-pass example (boundary should be at 50), a
bias-less model is glued to a boundary of 0 and stalls near 50% accuracy; adding
bias lets the boundary slide to 50 and reach 100% — "when your inputs sit far
from zero, you need a bias to move the line to them." The **learning rate** sets
correction size (0.1 here), and **normalization** (e.g. divide by the max, or
standardize) keeps training smooth and becomes essential when inputs live on
different scales. It closes with the full ~20-line Python program and the forward
pointer that *stacking* such neurons yields networks able to learn shapes a
single line cannot. Credits a Welch Labs video as inspiration.

## Why this matters

This is important because it explains the math behind how neural networks learn.
