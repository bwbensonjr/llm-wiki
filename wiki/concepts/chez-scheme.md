---
type: concept
status: reviewed
title: Chez Scheme
created: 2026-06-29
tags: [chez-scheme, scheme, lisp, programming-languages, language-implementation]
---

# Chez Scheme

A high-performance, optimizing-compiler implementation of [[scheme|Scheme]]
(R6RS), originally commercial and open-sourced in mid-2016. Its kernel is a
small amount of C, but it is mostly implemented in Scheme itself.

## Notes

Chez Scheme is well suited as a substrate for functional languages because it
provides the things mainstream VMs handle poorly: proper tail calls, first-class
continuations bounded only by the heap (with a long research lineage in
delimited control), the full numeric tower, and compilation to high-quality
machine code. This is why it was chosen as the new target for
[[racket|Racket]] — see
[[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]], which details
the roughly 30 changes and patches Racket CS needed from Chez and notes that
several were merged upstream.

It sits in this wiki's collection of [[scheme|Scheme]] implementations alongside
[[libscheme-scheme-as-a-c-library|libscheme]] (Scheme embedded as a C library)
and [[racket|Racket]] (which now runs on Chez Scheme).

## Sources

- [[porting-racket-to-chez-scheme|Porting Racket to Chez Scheme]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[the-development-of-chez-scheme|The Development of Chez Scheme]]
