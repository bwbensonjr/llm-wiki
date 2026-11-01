---
type: concept
status: reviewed
title: Clasp
created: 2026-10-31
tags: [lisp, llvm, language-implementation, programming-languages]
---

# Clasp

A Common Lisp implementation by [[christian-schafmeister|Christian Schafmeister]] that compiles through [[llvm|LLVM]] and interoperates directly with C++, built as the language of the CANDO molecular-design system. Its compiler is written in Common Lisp against LLVM's C++ API, which Clasp exposes to itself.

## Notes

**C++ interoperation without an FFI.** Most Common Lisps reach C++ only through a C foreign function interface. Clasp instead uses clbind, a C++ template library adapted from Lua's Luabind (in the Boost.Python mold), which generates wrappers at compile time from a Lisp name and a C++ function or class. By 2016 even the registration calls were generated: a Common Lisp scraper reads preprocessor tags such as `CL_DEFUN` and `CL_LAMBDA` out of the C++ source, emits the startup code, and records source locations so the editor can jump to a definition in either language.

**Compiler lineage.** Its Lisp runtime code came from ECL (Embeddable Common Lisp). An interpreter bootstraps a simple compiler (bclasp) that goes straight from s-expressions to LLVM IR. That compiler then builds one based on Robert Strandh's Cleavir, from the SICL project, which lowers through an AST and a flow-graph IR with inlining, type inference and [[escape-analysis|escape analysis]] before reaching LLVM IR.

**Runtime.** The Memory Pool System compacting collector moves C++ objects, made possible by a static analyzer written in Lisp on Clang's AST matchers that finds every pointer in every managed class. Clasp has DWARF debug info for mixed Lisp/C++ stacks, C++-compatible exception unwinding, the ORC JIT, LTO across Lisp and C++ bitcode, and joint profiling. Performance moved from about 100x slower than SBCL (2015) to within about 4x of C++ on a Fibonacci microbenchmark, with about 97.8% of the ANSI test suite passing (2018).

Among LLVM-backed functional-language compilers it sits alongside the CPS-based work in [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]; it is a [[lisp|Lisp]] relative of [[scheme|Scheme]] systems such as [[chez-scheme|Chez Scheme]] and [[racket|Racket]].

## Sources

- [[clasp-common-lisp-using-llvm-and-c-for-molecular-metaprogramming|Clasp: Common Lisp Using LLVM and C++ for Molecular Metaprogramming]]
- [[improving-the-clasp-programming-experience|Improving the Clasp Programming Experience]]
- [[lessons-learned-implementing-common-lisp-with-llvm|Lessons Learned Implementing Common Lisp with LLVM]]
