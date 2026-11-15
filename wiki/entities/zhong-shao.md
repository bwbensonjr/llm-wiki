---
type: entity
title: Zhong Shao
created: 2026-11-15
tags: [programming-languages, language-implementation, standard-ml]
---

# Zhong Shao

A Yale computer scientist and leader of the FLINT compiler-infrastructure project, who
worked with [[andrew-appel|Andrew W. Appel]] on the [[standard-ml|Standard ML of New Jersey]]
compiler. With Appel he wrote
[[efficient-and-safe-for-space-closure-conversion|Efficient and Safe-for-Space Closure Conversion]],
whose **safely linked closures** group free variables by lifetime into shareable records
so that closures can share environment without breaking the [[safe-for-space|safe-for-space]]
rule, and whose stackless calling convention keeps continuation closures in callee-save
registers. The algorithm grew out of his Princeton dissertation and shipped in both SML/NJ
and FLINT/ML.

## Sources

- [[efficient-and-safe-for-space-closure-conversion|Efficient and Safe-for-Space Closure Conversion]]
