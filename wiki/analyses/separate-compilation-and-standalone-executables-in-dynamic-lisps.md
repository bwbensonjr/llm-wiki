---
type: analysis
status: reviewed
title: Separate Compilation and Standalone Executables in Dynamic Lisps
created: 2026-11-01
question: "Re-do the analysis of why separate compilation and producing small standalone executables is challenging in dynamic, Lisp-family languages and approaches that have been taken to address the issues. I want to use that analysis to do a later write-up of how my Emit Scheme system addresses these issues using LLVM and a decisions that address things like macro-compilation and cross-module naming."
tags: [language-implementation, lisp, scheme, macros, programming-languages]
sources: ["[[separate-compilation]]", "[[composable-and-compilable-macros]]", "[[implicit-phasing-for-r6rs-libraries]]", "[[extending-the-scope-of-syntactic-abstraction]]", "[[another-module-system-for-scheme]]", "[[clhs-semantic-constraints]]", "[[world-age-in-julia]]", "[[dylan]]", "[[sealing-dylan-reference-manual]]", "[[define-sealed-domain]]", "[[chez-scheme-system-operations]]", "[[porting-racket-to-chez-scheme]]", "[[flow-directed-lightweight-closure-conversion]]", "[[raco-exe-creating-stand-alone-executables]]", "[[standalone-rhombus-programs]]", "[[common-lisp-cookbook-scripting-and-executables]]", "[[sbcl-a-sanely-bootstrappable-common-lisp]]", "[[why-janet]]", "[[clasp]]", "[[lessons-learned-implementing-common-lisp-with-llvm]]"]
---

# Separate Compilation and Standalone Executables in Dynamic Lisps

## Answer

Dynamic Lisps prize three things that each work against compiling a library once and shipping a small, closed binary:

- macros, which run code inside the compiler;
- an open world, where anything can be redefined or `eval`ed at run time;
- the live image as the natural unit of a program.

[[separate-compilation]] is where these collide.

### The problems

**1. Macros make the compiler run library code.** Importing a library that exports macros means executing that library at compile time. [[composable-and-compilable-macros|Flatt]] shows how a traditional Scheme gets this wrong. `(load "E.scm") (load "P.scm")` compiles to two compiled `load` calls, so the full compiler is needed at run time. The usual patch, `eval-when`, is fragile: adding a run-time helper to the macro file silently invalidates it, and it can appear to work because run-time code happens to supply what compile-time code needed. The same distinction is still there in Common Lisp practice. The [[common-lisp-cookbook-scripting-and-executables|Cookbook]] needs `eval-when` both to give a script an entry point and to load dependencies in mid-file. [[sbcl-a-sanely-bootstrappable-common-lisp|SBCL's build]] has to split `:compile-toplevel` from `:load-toplevel` carefully.

**2. Macros leak private names across module boundaries.** An exported macro expands inside someone else's code, so references to its home module's internals land in a unit that module never sees.

- [[extending-the-scope-of-syntactic-abstraction|Waddell and Dybvig]] show an exported `syntax-rules` macro that reads and `set!`s a variable its module never exports. That forces the compiler to treat unexported variables as possibly assigned and escaping. With `datum->syntax-object`, any syntax object from the module can be used to forge access to any of its bindings.
- [[another-module-system-for-scheme|Rees]] puts it from the linker's side. `delay` expands to `make-promise`, which is never exported, so the compiler must tell the linker to resolve that name in `delay`'s defining package, not in the client.

**3. Names must agree across separately built units.** Separate compilation turns macro-generated and module-private names into link-time names, and they have to be both unique and consistent.

- Waddell and Dybvig made generated names unique across compilation units by mixing the host's network interface ID, the process ID and the invocation time.
- [[implicit-phasing-for-r6rs-libraries|Ghuloum and Dybvig]] require each library to be expanded exactly once. Two expansions can export inconsistent bindings, for example a constant inlined under one configuration and a variable defined under another, and a program linked against both is "unlinkable". Each expansion therefore gets a globally unique ID.
- [[chez-scheme-system-operations|Chez's]] `verify-loadability` checks that object files come from mutually compatible compilation instances.
- [[raco-exe-creating-stand-alone-executables|`raco exe`]] renames embedded modules to deterministic `#%embedded:` names. That breaks features which record module names, such as serialization.

**4. Redefinition and `eval` defeat optimization and pruning.** [[clhs-semantic-constraints|CLHS 3.2.2.3]] lets a file compiler assume that a call to a function defined in the same file reaches that definition. Everywhere else, "the run-time definition prevails" unless the code is declared `inline` or given an `ftype` declaration. [[world-age-in-julia|Julia]] puts the cost plainly: fast code depends on resolving calls at compile time, and any newly `eval`ed method could invalidate them. `eval` also keeps the compiler alive. In Chez, `eval` *is* `compile`. `raco exe` can't see modules reached through `eval` or `dynamic-require`, and `raco demod` can prune only programs that give up `eval` ([[standalone-rhombus-programs|Rhombus Guide]]).

**5. Top-level effects have to happen in some order, at some time.**

- A Lisp file has no `main`; loading it runs every top-level form.
- Chez's whole-program mode orders library initialization by static dependencies only, so initialization that reaches other libraries through `eval` can break.
- SBCL can't run top-level forms while building its core image, so it defers them to a "cold init" phase that Rhodes calls the most fragile part of the build.

**6. Size: the runtime and compiler come along.** The Cookbook's open-source Common Lisp executables are large (SBCL about 48 MB) because they carry the compiler, debugger, symbol names and argument lists. Shrinking them takes compression or a tree shaker that has to prove what the program never reaches. `raco exe` gains no speed: it copies the whole runtime.

### The approaches taken

**Separating phases.** There are two opposite designs:

- **Explicit phases.** [[composable-and-compilable-macros|Flatt]] declares which phase each import is for, instantiates a module fresh for each phase and each compilation, and guarantees that compiling new code never affects previously compiled code. All compile-time code can be stripped from the finished program.
- **Implicit phases.** [[implicit-phasing-for-r6rs-libraries|Ghuloum and Dybvig]] infer each import's phase from how its identifiers are used, and share one instance per process.

Both split a compiled library into a part needed only to compile importers (macro transformers, called *visit code*) and a run-time part. Chez's `strip-fasl-file` removes the visit code before shipping.

**Drawing a boundary inside which nothing changes.** Each system picks a different unit:

- **The file.** Common Lisp's same-file call rule ([[clhs-semantic-constraints|CLHS]]).
- **The module.** Scheme 48 forbids assigning to imported variables, so a module compiled as a block can treat every variable it only defines as constant, even exported ones ([[another-module-system-for-scheme|Rees]]).
- **The library.** [[dylan|Dylan]] seals classes and generic functions by default ([[sealing-dylan-reference-manual|Sealing]]), and [[define-sealed-domain|`define sealed domain`]] seals narrower slices. The cost is that some violations show up only when independently compiled libraries are combined.
- **The top-level call.** [[world-age-in-julia|Julia's world age]] freezes the method table for a whole top-level call, with `invokelatest` as an explicit way out.

**Carrying information across separate compilation.** Chez embeds inlining information in library object files by default, so constants and procedures propagate into dependent libraries ([[chez-scheme-system-operations|CSUG 12.4]]). [[porting-racket-to-chez-scheme|Racket CS]] expands modules into *linklets*, whose imports and exports are explicit variables, and that makes cross-module optimization possible.

**Whole-program compilation.** Chez's `compile-whole-program` folds libraries into one object file, discards unused code, and optimizes across library boundaries. Incorporated libraries are hidden from `eval` unless requested. [[flow-directed-lightweight-closure-conversion|Stalin]] goes all the way: it has no `eval`, no REPL and no separate compilation, and in return whole-program flow analysis proves soundly what other compilers are only told by unsafe flags. `raco demod` is the optional version of the same move.

**Tracing from an entry point.** Scheme 48's static linker takes a named startup procedure and follows `open` and `access` links to decide what goes into a standalone heap image.

**Bundling the runtime.**

- [[raco-exe-creating-stand-alone-executables|`raco exe`]] and `raco dist` keep the language fully dynamic and ship it whole.
- [[why-janet|Janet]] embeds bytecode in a generated C file with the runtime and compiles it to a native executable under 1 MB.

**Dumping the image.**

- Common Lisp's default is `save-lisp-and-die`, which writes out the running heap ([[common-lisp-cookbook-scripting-and-executables|Cookbook]]). LispWorks' tree shaker and ECL's compile-to-C route give smaller results.
- Janet runs top-level code at compile time and snapshots the resulting program state to resume at run time.
- [[sbcl-a-sanely-bootstrappable-common-lisp|SBCL]] builds its own core by "pseudo-loading" its compiled files (writing them into a memory image without running them) and then running the deferred initialization on first boot.

**An LLVM-backed Lisp.** [[clasp|Clasp]] compiles Common Lisp through LLVM. It does both JIT and ahead-of-time compilation, runs link-time optimization across Lisp and C++ bitcode, and emits DWARF debug info for mixed Lisp and C++ stacks ([[lessons-learned-implementing-common-lisp-with-llvm|2018 talk]]).

### Decisions this leaves for an LLVM-backed Scheme

Each question comes from the problems above.

1. **Phase model.** Explicit phases or inferred ones? One instance per process or one per phase?
2. **Where compiled macros live.** Are transformers kept apart from run-time code (Chez's visit code, Flatt's strippable compile-time code), and are they left out of executables?
3. **Private names that exported macros reach.** Must they be link-visible symbols? How does the linker resolve them in the macro's home module (Rees)?
4. **Generated-name scheme.** Unique per compilation (Waddell and Dybvig), or deterministic like `raco exe`'s embedded names? Is there a build identity that catches mismatched builds (Ghuloum and Dybvig's unique IDs, Chez's loadability check)?
5. **Optimization boundary.** File, module or library? Can imported bindings be assigned? Is anything sealed?
6. **`eval` policy.** If `eval` is kept, the compiler is in the executable and pruning is unsound.
7. **Initialization order.** Static dependency order, as in Chez's whole-program mode, and what happens when initialization uses `eval`.
8. **Getting to a small binary.** Whole-program compilation, tracing from an entry point, or link-time dead stripping.

*Not corpus-backed:* how these map onto LLVM itself. Symbol linkage choices (`internal` vs `external`, `linkonce_odr` for macro-introduced helpers), symbol name mangling, and using LTO or `--gc-sections` for dead stripping come from general knowledge, not from a cited source.

## Why this matters

It's the problem map Emit Scheme's LLVM design answers.
