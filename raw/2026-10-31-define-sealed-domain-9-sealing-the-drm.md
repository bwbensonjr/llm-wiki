---
source: https://opendylan.org/books/drm/Define_Sealed_Domain
fetched-at: 2026-10-31
converter: jina
---

Title: Define Sealed Domain — 9. Sealing — The DRM

URL Source: https://opendylan.org/books/drm/Define_Sealed_Domain

Markdown Content:
`define sealed domain` is used to make specific portions of a generic function and of the class hierarchy invariant without disallowing all future changes. The arguments to `define sealed domain` are an explicitly known generic function and a series of types, one for each required argument of the generic function.

The complete syntax of `define``sealed domain` is given on [page 388](https://opendylan.org/books/drm/Definition_Macros#XREF-2024).

A `define sealed domain` definition in a library L for a generic function G with types T _1_…T _n_ imposes the following [constraints on programs](https://opendylan.org/books/drm/Define_Sealed_Domain):

1.   A method M that is congruent to G and that is not an explicitly known method in L may be added to G only if at least one of the specializers for M is disjoint from the corresponding T.
2.   A method M may be removed from G only if at least one of the specializers for M is disjoint from the corresponding T.
3.   A class C (with direct superclasses D _1_…D _m_) that is not explicitly known in L may be created only if no method in G actually blocks C. 
    *   A method M (with specializers S _1_…S _n_) in G potentially blocks C at argument position i if there exist j and k such that D _j_ is a pseudosubtype of S _i_, D _k_ is a pseudosubtype of T _i_, and D _k_ is not a pseudosubtype of S _i_.
    *   A method M actually blocks C if M potentially blocks C at some argument position, and for every argument position i where S _i_ and T _i_ are disjoint, M potentially blocks C at i.

The third constraint is illustrated by the following example:

define open generic m (x);
define open class <t> (<object>) end class <t>;
define open class <s> (<object>) end class <s>;
define method m (s :: <s>) end method m;
define sealed domain m (<t>);

define class <c> (<s>, <t>) end class <c>;

The definition of class `<c>` would be valid if it appeared in the same library as the preceding definitions or in a library used by them, but invalid if it appeared in a different library. The reason is that without the definition of `<c>`, the method defined on `m` is not within the domain declared by the `define sealed domain`, but with the definition of `<c>` the method is within that domain.

[**Errata:**](https://opendylan.org/books/drm/Errata#p136-1) In the published book, `open` is missing from the definitions of `generic m`, `class <t>`, and `class <s>`.

## Rationale

`define sealed domain` permits the compiler to assume certain properties of the program that can be computed based on explicitly known classes and methods, with a guarantee that an attempt to violate any of those assumptions will be detected.

The goal of rule 3 is that the creation of the class C must not make any method M applicable to a part of the sealed domain to which it was not previously applicable.

The potentially blocks concept describes the mechanism for testing whether the set of objects that are instances of both S _i_ and T _i_ (i.e., to which the method is applicable at the i th argument position and that are within the sealed domain at that argument position) would change as a result of creating C. By specifying what valid programs are allowed to do, rule 3 implicitly specifies the assumptions a compiler can make. A `define sealed domain` definition accomplishes this by permitting the compiler to eliminate some of the known methods on a generic function from the set of methods that might be applicable to a particular call at runtime. For example, if this leaves exactly one applicable method, the compiler can eliminate a run-time method dispatch and consider additional optimizations such as inlining.

Specifically, suppose the compiler is compiling a call to G and has determined that the argument at position i is an instance of some type U (where U is not necessarily a standard Dylan type, but could instead be a compiler-internal extension to the type system, such as a difference of two types). For the compiler to be able to rely on the `define sealed domain` definition, U must be a subtype of T _i_. For the compiler to determine that M is not applicable, U must be disjoint with S _i_. Creating C can't change whether U is a subtype of T _i_, but it can change whether U is disjoint with S _i_. If there could be an object that is simultaneously an instance of U, C, and S _i_, it would violate the compiler's assumption that M is not applicable in the call to G, and therefore creating C would be a sealing violation. If there can't be such an object, then creating C is allowed.

This maps onto rule 3 as follows (ignoring for the moment the added complication of limited types that lead to the use of the pseudosubtype relationship rather than subtype):

U is a subtype of D _k_ and therefore is a subtype of T _i_, because subtype is transitive.

D _k_ is not a subtype of S _i_, because if it were then U could not be disjoint from S _i_.

D _j_ is a subtype of S _i_.

If U and C would have a nonempty intersection, then the creation of C must be prevented, else U would no longer be disjoint from S _i_. One possible U is the set of all general instances of D _k_ that are not also general instances of any of the explicitly known direct subclasses of D _k_. That U would indeed have a non-empty intersection with C. The existence of this U makes the proposed rule 3 necessary.

Rule 3 does not need to address the possibility of multiple inheritance being used to combine classes involved in the element types of limited collection classes. Changes to the disjointness relationships between element types does not affect the relationships between collection types with those element types.[](https://opendylan.org/books/drm/Define_Sealed_Domain)

## [Pseudosubtype Examples](https://opendylan.org/books/drm/Define_Sealed_Domain)

Suppose A and B are disjoint subclasses of `<collection>`, S _i_ is `limited(A, of: T)`, and T _i_ is 
```
limited(B,
	of: T)
```
. Thus, S _i_ and T _i_ are disjoint and M is outside the sealed domain. If C inherits from A and B it should be potentially blocked by M, because an instance of 
```
limited(C,
	of: T)
```
 would be an instance of both S _i_ and T _i_. Since B is not a subtype of T _i_, there would be no blockage if the constraints in rule 3 were defined in terms of `subtype`. However, B is a pseudosubtype of T _i_, so specifying rule 3 using the pseudosubtype relationship correctly causes M to potentially block C.

Suppose S _i_ is 
```
limited(<stretchy-vector>, of:
	  <integer>)
```
 and T _i_ is `limited(<sequence>, of: <integer>)`. It should be possible to create `<stretchy-string>`, a direct subclass of `<stretchy-vector>` and `<string>`. The element-type of `<stretchy-string>` must be a subtype of `<character>`, therefore, assuming `<integer>` and `<character>` are disjoint, `<stretchy-string>` is disjoint from both S _i_ and T _i_, and so is not blocked. This example shows the need for the non-disjointness requirement in the definition of pseudosubtype.[](https://opendylan.org/books/drm/Define_Sealed_Domain)

## [](https://opendylan.org/books/drm/Define_Sealed_Domain)[Abbreviations for Define Sealed Domain](https://opendylan.org/books/drm/Define_Sealed_Domain)

`define sealed method` defines a method on a generic function and also seals the generic function for the types that are the specializers of the method.

The following two program fragments are equivalent:

define sealed method insert (source :: <list>, i :: <object>)
  => (result :: <list>)
  …
end method insert;
and

define method insert (source :: <list>, i :: <object>)
  => (result :: <list>)
  …
end method insert;
define sealed domain insert (<list>, <object>);

The `sealed slot` option to `define class` defines a slot and also makes the getter generic function sealed over the class, and the setter generic function, if there is one, sealed over the type of the slot and the class.

The following two program fragments are equivalent:

define class <polygon> (<shape>)
  sealed slot sides :: <integer>, required-init-keyword: sides:;
end class <polygon>;

and

define class <polygon> (<shape>)
  slot sides :: <integer>, required-init-keyword: sides:;
end class <polygon>;
define sealed domain sides (<polygon>);
define sealed domain sides-setter (<integer>, <polygon>);[](https://opendylan.org/books/drm/Define_Sealed_Domain)

## [Implied Restrictions on Method Definitions](https://opendylan.org/books/drm/Define_Sealed_Domain)

To avoid potential [sealing violations](https://opendylan.org/books/drm/Define_Sealed_Domain) among separately developed libraries, one of the following conditions should be true for every method M defined in a library L:

*   Either the generic function to which M is added should be defined in the library L, or
*   One of the specializers of M should be a subtype of a class defined in library L.

The following example illustrates why this condition is necessary.

Library L _1_ defines and exports the following:

define open generic g (x)
define open class <c1> (<object>) end class <c1>;

Library L _2_ uses L _1_ and defines the following

define open class <c2> (<c1>) end class <c2>;
define method g (x :: <c2>) end method;
define sealed domain g (<c2>)

Library L _3_ uses L _1_ and defines the following

define method g (x :: <c1>) end method;

Libraries L _2_ and L _3_ are developed independently, and have no knowledge of each other. An application that attempts to use both L _2_ and L _3_ contains a sealing violation. L _2_ is clearly valid. Therefore, L _3_ is at fault for the sealing violation. Because the compiler cannot prove that use of L _3_ will lead to an error (and indeed, it will only lead to an error in the presence of L _2_), it is appropriate to issue a warning but not disallow the compilation of L _3_.[](https://opendylan.org/books/drm/Define_Sealed_Domain)[](https://opendylan.org/books/drm/Define_Sealed_Domain)

[**Errata:**](https://opendylan.org/books/drm/Errata#p140-1) In the published book, `open` is missing from the definitions of `generic g`, `class <c1>`, and `class <c2>`.

[**Errata:**](https://opendylan.org/books/drm/Errata#p140-2) In the published book, `method g (x :: <c1>)` is incorrectly specialized on `<c>`.
