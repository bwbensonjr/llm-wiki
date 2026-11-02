---
type: summary
title: Extending the Scope of Syntactic Abstraction
created: 2026-10-31
source: inbox-files/292540.292559.pdf
raw: raw/2026-10-31-292540-292559.md
tags: [macros, scheme, chez-scheme, language-implementation, programming-languages]
---

# Extending the Scope of Syntactic Abstraction

## Summary

Oscar Waddell and [[r-kent-dybvig|R. Kent Dybvig]]'s POPL 1999 paper on the module system integrated with `syntax-case` in [[chez-scheme|Chez Scheme]]. The design keeps a small core language and treats modules as pure *scope*: a `module` form names a lexical contour and lists its exports, `import` makes those bindings visible where it appears, and both may occur at top level, in local bodies, or nested in other modules, and may be produced by macros. Modules change only visibility, never denotation, so a program with modules translates statically into core Scheme with consistently renamed identifiers. On that base the paper builds, as ordinary macros, qualified references, anonymous modules, selective import and renaming, multiple views of one module, mutually recursive modules, separate interfaces, and compound and incrementally satisfied interfaces. It shows that the more dynamic linking of Flatt and Felleisen's units can be written at the source level on top of it.

Implementation extends the `syntax-case` expander, which renames bound identifiers lazily through syntax objects carrying substitution "ribs" and marks ([[hygienic-macros]]). Module bodies get extensible ribs, a module's name maps to an interface of export syntax objects, and an exported macro keeps valid references to the module's private bindings because the syntax objects it inserts close over the module's rib. For **separate compilation**, generated names must be unique across compilation units, which the compiler ensures by mixing the host's network interface identifier, the process ID and the invocation time. A compiled module's object file holds its code, its interface and its compiled macro transformers; before compiling an importer, the module must be *visited* (installing interface and transformers) or *loaded* (also running its code).

The paper is direct about what exported macros cost static analysis. Unexported variables should be effectively local and so optimizable, but an exported macro may expand, inside someone else's separately compiled code, into a reference to or an assignment of a private variable. In the worked example a variable that appears only as quoted data inside a `syntax-rules` macro is nonetheless read and `set!` from outside the module. So "the compiler does not know how the macro will be used in separately compiled code" and must assume such variables are assigned and escape. With `datum->syntax-object`, even a conservative analysis fails, because any syntax object from the module can be used to forge access to any of its bindings. The authors rejected Dylan's approach of conservatively estimating a macro's implicit exports, since innocent edits could silently change performance, and instead improve the expansion of top-level modules so private bindings stay local where possible. An `import-only` form gives isolated scopes for verifying what a module uses.

## Why this matters

This is the Chez lineage behind both [[implicit-phasing-for-r6rs-libraries|the R6RS library work]] and [[chez-scheme-system-operations|Chez's compilation model]], and it pins down a specific way macros defeat [[separate-compilation]]: a module cannot treat its own unexported variables as private if its exported macros can be expanded in code it never sees. That costs optimization even with modules, and it is the same reason sealing or a closed world is needed before a compiler can treat library internals as fixed.
