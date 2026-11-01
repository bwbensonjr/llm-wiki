---
type: summary
status: provisional
title: Define Sealed Domain (Dylan Reference Manual)
created: 2026-10-31
source: https://opendylan.org/books/drm/Define_Sealed_Domain
raw: raw/2026-10-31-define-sealed-domain-9-sealing-the-drm.md
tags: [language-implementation, programming-languages, type-systems]
---

# Define Sealed Domain (Dylan Reference Manual)

## Summary

The Dylan Reference Manual section on `define sealed domain`, the most targeted of Dylan's sealing declarations. Dylan is a dynamic, object-oriented language with multiple dispatch and classes that can be extended at run time, and sealing is how it lets a compiler optimize despite that. `define sealed domain` takes a generic function and one type per required argument and makes that slice of the generic function and class hierarchy invariant "without disallowing all future changes". A declaration in library L for generic function G over types T1…Tn forbids three things outside L: adding a method whose specializers all overlap the Ts, removing such a method, and creating a new class (for example by multiple inheritance) that would make an existing method newly applicable inside the sealed domain. A worked example shows a class definition that is legal in the declaring library but illegal in any other.

The rationale is stated directly: the declaration "permits the compiler to assume certain properties of the program that can be computed based on explicitly known classes and methods, with a guarantee that an attempt to violate any of those assumptions will be detected." In practice it lets the compiler drop known methods from the set that could apply at a call site. If exactly one remains, the generic dispatch becomes a direct call or is inlined. The section spends most of its length justifying the class-creation rule, including a *pseudosubtype* relation needed so that limited collection types cannot slip a new applicable method into the domain. Two abbreviations cover the common cases: `define sealed method` seals the generic over that method's specializers, and a `sealed slot` seals its getter and setter over the class.

The last part addresses separately developed libraries directly. To avoid sealing violations, every method a library defines should either belong to a generic function the library defines or specialize on a class the library defines. The example has library L2 sealing `g` over its own class while an independent L3 adds a broader method to `g`; an application using both is in violation, L3 is at fault, but because L3 alone cannot be shown erroneous, the compiler should warn rather than refuse to compile it.

## Why this matters

Sealing is a language-level answer to the redefinition half of the [[separate-compilation]] problem: rather than forbidding change everywhere, as a closed-world compiler does, or allowing it everywhere, as most Lisps do, a library declares exactly which parts of its method and class graph other libraries may not extend, and the compiler optimizes across library boundaries on that basis. The section is also candid about the cost, that some violations surface only when independently compiled libraries are combined, which is the same composition hazard a separately compiled Lisp library faces.
