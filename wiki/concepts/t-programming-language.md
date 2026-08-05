---
type: concept
status: reviewed
title: T (Programming Language)
created: 2026-08-05
tags: [scheme, lisp, programming-languages, language-implementation]
---

# T (Programming Language)

A dialect of [[scheme]] developed at Yale in the 1980s by the T project — Norman
Adams, [[richard-kelsey|Richard Kelsey]], [[david-kranz|David Kranz]], Jim Philbin,
and Jonathan Rees — notable for the ORBIT compiler that made it competitive with
Pascal.

## Notes

T was both the language ORBIT compiled and the language ORBIT was written in. Its
runtime shaped the compiler's constraints: the T3 system supports lightweight
processes and must be able to take an interrupt between any two instructions, so
registers are partitioned into rootable (tagged, scannable by the garbage
collector) and non-rootable classes that the compiler must keep separated.
Arguments are passed in registers under a standard calling sequence, with a
known memory block for the overflow beyond the register count.

Its predecessor compiler, TC, was a conventional compiler with closure handling
added on — the design ORBIT was written to replace by treating closures as
fundamental instead.

## Sources

- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
- [[a-tractable-native-code-scheme-system|A Tractable Native-Code Scheme System]]
