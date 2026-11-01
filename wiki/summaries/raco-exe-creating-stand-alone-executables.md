---
type: summary
status: provisional
title: "raco exe: Creating Stand-Alone Executables"
created: 2026-10-31
source: https://docs.racket-lang.org/raco/exe.html
raw: raw/2026-10-31-2-raco-exe-creating-stand-alone-executables.md
tags: [racket, language-implementation, programming-languages]
---

# raco exe: Creating Stand-Alone Executables

## Summary

The [[racket|Racket]] documentation chapter for `raco exe`, the tool that packages a Racket program as an executable, along with launchers and the related `raco distribute`. Its model is to bundle, not to link: `raco make` produces compiled code that relies on a Racket executable for run-time support, and `raco exe` embeds a module, from source or bytecode, into a copy of the `racket` (or, with `--gui`, `gracket`) executable, which invokes that module at startup. Modules reached through `require` come along automatically. The documentation is explicit that this buys no speed: an `raco exe` executable does not run faster than the same code under `raco make`, and for faster startup it recommends a smaller base language (`racket/base`), precompiled bytecode, and `raco demod`.

The limits all come from dynamism. Modules and files reached only *dynamically*, "through `eval`, `load`, or `dynamic-require`", are not embedded; the programmer must name them with `++lib`, or declare them with `define-runtime-path` so they are copied into a distribution. Language readers used only through `#lang` are likewise omitted unless supplied with `++lang`, for programs that load `#lang` modules at run time. Embedded modules lose their filesystem names and get symbolic `#%embedded:` names, generated in an unspecified but deterministic way, which can break features that depend on module names, such as serialization formats that record a module name to find a deserializer later; `++named-lib` and `++named-file` fix the names when that matters. The tool works only with module-based programs.

"Stand-alone" is qualified: the executable runs without starting `racket` or DrRacket but may still depend on Racket's shared libraries and on run-time files. How stand-alone it is depends on how Racket itself was built (`--enable-shared` on Unix makes executables less so), on flags such as `--embed-dlls` on Windows and `--orig-exe` on Unix, and finally on `raco distribute`, which packages the executable with its support libraries into a self-contained directory. The chapter also covers launchers, small installation-specific scripts or binaries that start an installed Racket on a program, as a lighter alternative.

## Why this matters

`raco exe` is the bundling answer to standalone executables in a dynamic Lisp: rather than compiling the program into a closed native binary, it ships the whole runtime with the program's modules inside it, which is why it gains no speed and why everything reached through `eval` or `dynamic-require` has to be declared by hand. Set against [[chez-scheme-system-operations|Chez's whole-program compilation]], on which Racket CS runs, it shows that Racket chose to keep its dynamism intact at delivery time and accept a larger, runtime-carrying executable, one of the design points on the [[separate-compilation]] spectrum.
