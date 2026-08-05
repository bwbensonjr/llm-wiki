---
type: entity
status: provisional
title: Mitchell Wand
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp]
---

# Mitchell Wand

A programming-languages researcher at Northeastern University, co-author with
[[william-clinger|William Clinger]] of the HOPL IV history of
[[hygienic-macros|hygienic macro technology]].

## Notes

His name reaches this wiki from more than one direction. He co-wrote
[[hygienic-macro-technology|Hygienic Macro Technology]], and he is half of "Wand and
Steckler," whose [[lightweight-closure-conversion|Lightweight Closure Conversion]] uses
the term [[closure-conversion|closure conversion]] for a source-level transformation
replacing a procedure with a representation of it — a usage
[[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]] singles out
as adding to the terminological confusion around [[lambda-lifting|lambda lifting]]. The
paper itself shows the two are orthogonal in *purpose* rather than in mechanism: it
passes a captured variable as a call-site argument, which is lifting's move, but justifies
it with a soundness proof instead of a code-quality argument.

Earlier, he worked with Eugene Kohlbecker on macro-by-example — the pattern language
for specifying syntactic transformations. Notably, that paper does not mention
hygiene at all: the two regarded the pattern language and the capture problem as
orthogonal concerns, a separation that later designs would have to reconcile.

## Sources

- [[hygienic-macro-technology|Hygienic Macro Technology]]
- [[lightweight-closure-conversion|Lightweight Closure Conversion]]
