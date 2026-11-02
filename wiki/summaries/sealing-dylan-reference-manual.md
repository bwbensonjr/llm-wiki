---
type: summary
title: Sealing (Dylan Reference Manual)
created: 2026-11-01
source: inbox-files/drm-sealing-chapter.md
raw: raw/2026-11-01-9-sealing-the-dylan-reference-manual.md
tags: [language-implementation, programming-languages, type-systems]
---

# Sealing (Dylan Reference Manual)

## Summary

Chapter 9 of the [[dylan|Dylan]] Reference Manual (chapter page `https://opendylan.org/books/drm/Sealing`), covering its overview, explicitly known objects, and the sealing adjectives on classes and generic functions. Sealing directives declare that classes or functions "will never be used in particular ways, or will never be extended in particular ways". They enable compiler optimizations and also state the programmer's intent. The directives are `sealed`/`open` on classes and generic functions, `abstract`/`concrete` and `primary`/`free` on classes, and [[define-sealed-domain|`define sealed domain`]] with its abbreviations `define sealed method` and `sealed slot`. All but the last are adjectives on a definition.

The unit of sealing is the **library**, defined through **explicitly known** objects. A class is explicitly known in library L if `define class` defines it in L or in a library L uses. A method is explicitly known if `define method` or a slot specification of an explicitly known class defines it there. A generic function is explicitly known if `define generic` defines it, or if such a method or slot implies it. A sealing restriction limits the set of classes, generic functions or methods to the ones explicitly known, so nothing else can be added later.

- **Sealed class:** no direct subclasses beyond those explicitly known in the defining library. Subclassing it from another library, or passing it as a superclass to `make` of `<class>`, is an error.
- **Sealed generic function:** no methods beyond those explicitly known in its library, and no methods removed. Defining a method on it from another library, or calling `add-method` or `remove-method` on it, is an error.
- **Primary class:** a class's primary superclasses must form a single-inheritance chain, so slots defined in a primary class "may be accessed more efficiently" than slots in a free class.
- **Abstract class:** cannot be instantiated directly. It must have abstract superclasses, and `make` signals an error unless a method on `make` delegates to a concrete subclass.

The defaults lean closed. An explicitly defined class or generic function is **sealed unless declared `open`**, and so is a generic function implied only by method or slot definitions. Classes are free and concrete by default. Objects created at run time with `make` of `<class>` or `<generic-function>` are open, and the language specifies no way to create a sealed one that way.

## Why this matters

This chapter states the general rule behind [[define-sealed-domain|`define sealed domain`]]. A library is a boundary, and by default a class or generic function cannot be extended past it, so a compiler can treat a library's class graph and method sets as fixed when it compiles callers. A dynamic language usually makes a definition final only by explicit request. Dylan does the reverse: definitions are fixed unless declared `open`. That is a direct answer to the redefinition half of [[separate-compilation]]. Openness becomes something a library chooses rather than something every compilation unit must assume, and objects created at run time stay open so the dynamic language survives.
