---
source: inbox-files/drm-sealing-chapter.md
fetched-at: 2026-11-01
converter: markitdown
---

# 9. Sealing (The Dylan Reference Manual)

Assembled on 2026-11-01 from the chapter's subpages, fetched through Jina Reader and concatenated in chapter order. The fifth subpage, Define Sealed Domain, was ingested separately.

- Chapter: https://opendylan.org/books/drm/Sealing
- https://opendylan.org/books/drm/Sealing_Overview
- https://opendylan.org/books/drm/Explicitly_Known_Objects
- https://opendylan.org/books/drm/Declaring_Characteristics_of_Classes
- https://opendylan.org/books/drm/Declaring_Characteristics_of_Generic_Functions

## Overview

Source: https://opendylan.org/books/drm/Sealing_Overview

[](https://opendylan.org/books/drm/Sealing_Overview)This chapter describes techniques for sealing portions of a Dylan program by declaring that classes or functions will never be used in particular ways, or will never be extended in particular ways. These sealing directives enable a range of compiler optimizations, and also clarify the programmer's intent.

[The sealing directives include:](https://opendylan.org/books/drm/Sealing_Overview)

*    Declaring a class to be `sealed` or `open`. This controls whether a class can be directly subclassed outside the library in which it is defined.
*   Declaring a class to be `abstract` or `concrete`. This controls whether a class can have direct instances.
*   Declaring a class to be `primary` or `free`. This controls how a class can be used for multiple inheritance.
*   Declaring a generic function to be `sealed` or `open`. This controls whether methods can be added to the generic function from outside the library in which the generic function is defined.
*   Using `define sealed domain`, or using the abbreviations
```
define sealed
	    method
```
 and `sealed slot`. These disallow the addition of some methods from outside the library in which the generic function is defined.

With the exception of `define sealed domain`, these directives are expressed as [adjectives](https://opendylan.org/books/drm/Sealing_Overview) on the generic function definition, class definition, method definition, or slot specification.[](https://opendylan.org/books/drm/Sealing_Overview)

## Explicitly Known Objects

Source: https://opendylan.org/books/drm/Explicitly_Known_Objects

A class, generic function, or method may or may not be explicitly known to a given library. A sealing restriction may limit the set of classes, generic functions, and methods to those that are explicitly known; others cannot be added.

*   A [class](https://opendylan.org/books/drm/Explicitly_Known_Objects)C is explicitly known in a library L if it is defined by `define class` in L or in a library used by L.
*   A [generic function](https://opendylan.org/books/drm/Explicitly_Known_Objects)G is explicitly known in a library L if G is defined by `define generic` in the library or in one of the libraries L uses, or if G is implicitly defined by the definition of a method explicitly known in L or if G is implicitly defined by a slot specification for a class explicitly known in L.
*   A [method](https://opendylan.org/books/drm/Explicitly_Known_Objects)M is explicitly known in a library L if M is defined by `define method` in L or in one of the libraries L uses, or if M is defined by a slot specification for a class explicitly known in L.[](https://opendylan.org/books/drm/Explicitly_Known_Objects)

## Declaring Characteristics of Classes

Source: https://opendylan.org/books/drm/Declaring_Characteristics_of_Classes

A class definition may include the adjectives `sealed`, `open`, `primary`, `free`, `abstract`, or `concrete`. These [adjectives](https://opendylan.org/books/drm/Declaring_Characteristics_of_Classes) declare characteristics of the class.

Additional restrictions on the ability to subclass classes may be imposed by
```
define
	  sealed domain
```
.

*   An explicitly defined class can be declared to be either [sealed or open](https://opendylan.org/books/drm/Declaring_Characteristics_of_Classes). If a class is sealed then no additional direct subclasses other than those explicitly known in the same library may be created. Thus, it is an error to define a direct subclass of a sealed class in some library other than the one that defined the sealed class, or to use `make` of `<class>` with a sealed class included in the direct superclasses specified by the `superclasses:` initialization argument. An open class does not prohibit such operations.
When explicitly defining a class, the default is for the class to be sealed. This may be overriden by explicitly specifying that it is open. A class created using `make` of `<class>` is open. There is no specified way to create a sealed class using `make`.
*   An explicitly defined class may be declared to be either [primary or free](https://opendylan.org/books/drm/Declaring_Characteristics_of_Classes). The default is free. Each primary superclass of a class must be either a subclass or a superclass of all the other primary superclasses of the class. (This essentially restricts primary classes to forming a [single inheritance](https://opendylan.org/books/drm/Declaring_Characteristics_of_Classes) chain.) [Slots](https://opendylan.org/books/drm/Declaring_Characteristics_of_Classes) defined in a primary class may be accessed more efficiently than slots defined in a free class.
*   An explicitly defined class may be defined to be either [abstract or concrete](https://opendylan.org/books/drm/Declaring_Characteristics_of_Classes). The default is concrete. The superclasses of an abstract class must be abstract. The default method on `make` will signal an error if passed an abstract class. For an abstract class to be instantiable, it must define a method on `make` that delegates to a concrete subclass.[](https://opendylan.org/books/drm/Declaring_Characteristics_of_Classes)

## Declaring Characteristics of Generic Functions

Source: https://opendylan.org/books/drm/Declaring_Characteristics_of_Generic_Functions

A generic function definition may include either the adjective [`sealed` or the adjective `open`](https://opendylan.org/books/drm/Declaring_Characteristics_of_Generic_Functions). These adjectives declare whether the generic function is sealed.

If a generic function is sealed then no additional methods other than those explicitly known in the same library may be added to the generic function and no methods may be removed from it. Thus, it is an error to define a method for a sealed generic function in some library other than the one which defined the sealed generic function, or to apply `add-method` or `remove-method` to a sealed generic function. An open generic function does not prohibit these operations.

When explicitly defining a generic function, the default is for the generic function to be sealed. It can be declared to be open by using the `open` adjective in the generic function definition. A generic function that has no explicit definition but has an implicit definition provided by explicit definitions of generic function methods or slot accessors is also sealed. A generic function created using `make` of `<generic-function>` is open. There is no specified way to create a sealed generic function using `make.`

Additional restrictions on the ability to add methods to a generic function may be imposed by `define sealed domain`.[](https://opendylan.org/books/drm/Declaring_Characteristics_of_Generic_Functions)
