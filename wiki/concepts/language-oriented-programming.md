---
type: concept
title: Language-Oriented Programming
created: 2026-06-24
tags: [language-oriented-programming, programming-languages]
---

# Language-Oriented Programming

A software-development paradigm (LOP) in which developers analyze each part of a
problem in the language of its domain, express the solution in a matching
[[domain-specific-language]], and then compose these multilingual components
into one system. It elevates "language" itself to a software building block with
the same status as objects, modules, and components.

## Notes

The case for LOP is framed by analogy to object-oriented programming (which made
creating and manipulating objects syntactically simple and cheap) and
concurrency-oriented programming (Erlang's inexpensive processes and message
passing) — each paradigm thrives when the base language supports it directly.

LOP's defining quality is **incrementality**: the ability to build languages in
small pieces, one construct at a time, deriving new languages from old and
making them as sound or secure as a project demands. Two subsidiary guidelines:
enable a language's creator to enforce its invariants (values flowing between
languages need protection), and turn extra-linguistic mechanisms into linguistic
constructs (resorting to external config/build/makefile languages signals the
host language lacks expressive power).

[[racket]] is the platform built to explore LOP directly; language workbenches
such as Spoofax are a parallel line of work, and the authors conjecture the two
approaches will converge.

## Sources

- [[a-programmable-programming-language|A Programmable Programming Language]]
