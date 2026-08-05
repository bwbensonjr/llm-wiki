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
[[hygienic-macro-technology|Hygienic Macro Technology]], and he appears in the
compiler pages as half of "Wand and Steckler," whose *selective and lightweight
closure conversion* uses the term [[closure-conversion|closure conversion]] for a
source-level transformation replacing a procedure with a representation of it —
a usage orthogonal to [[lambda-lifting|lambda lifting]], and one that
[[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]]
singles out as adding to the terminological confusion around that pass.

Earlier, he worked with Eugene Kohlbecker on macro-by-example — the pattern language
for specifying syntactic transformations. Notably, that paper does not mention
hygiene at all: the two regarded the pattern language and the capture problem as
orthogonal concerns, a separation that later designs would have to reconcile.

## Sources

- [[hygienic-macro-technology|Hygienic Macro Technology]]
