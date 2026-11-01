---
type: entity
status: reviewed
title: Christian Schafmeister
created: 2026-10-31
tags: [lisp, language-implementation]
---

# Christian Schafmeister

Professor of chemistry at Temple University whose lab builds large, rigid "molecular Lego" molecules (spiroligomers) as catalysts, sensors and therapeutics. To design them computationally he built [[clasp|Clasp]], a Common Lisp on [[llvm|LLVM]] that interoperates with C++, and CANDO, the molecular-design environment that runs on it. He writes as `drmeister`.

## Notes

He came to Lisp from the C++/[[python|Python]] interface problem: wrapping his chemistry library with Boost.Python consumed more effort than the chemistry. He learned compiler construction and LLVM largely from public documentation and the LLVM community, taking Clasp from an interpreter to a bootstrapped native compiler, and later adopted Robert Strandh's Cleavir as its optimizing compiler. His stated goal is consistent from 2015 to 2018: a fast, macro-capable language in which molecular designs can be generated and searched at scale.

## Sources

- [[clasp-common-lisp-using-llvm-and-c-for-molecular-metaprogramming|Clasp: Common Lisp Using LLVM and C++ for Molecular Metaprogramming]]
- [[improving-the-clasp-programming-experience|Improving the Clasp Programming Experience]]
- [[lessons-learned-implementing-common-lisp-with-llvm|Lessons Learned Implementing Common Lisp with LLVM]]
