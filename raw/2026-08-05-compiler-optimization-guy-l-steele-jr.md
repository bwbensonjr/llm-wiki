---
source: https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html
fetched-at: 2026-08-05
converter: jina
---

Title: Compiler Optimization – Guy L Steele Jr

URL Source: https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html

Markdown Content:
_RABBIT: A Compiler for SCHEME_ [[Steele 1978](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#steele-1978 "RABBIT: A Compiler for SCHEME (A Dialect of LISP) A Study in Compiler Optimization Based on Viewing LAMBDA as RENAME and PROCEDURE CALL as GOTO using the techniques of Macro Definition of Control and Environment Structures Source-to-Source Transformation Procedure Integration and Tail-Recursion")] contains the note:

> Revised version of a dissertation submitted (under the title _“Compiler Optimization Based on Viewing LAMBDA as RENAME plus GOTO”_) to the Department of Electrical Engineering and Computer Science on May 12, 1977

This is an abridged transcription ([CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/ "Creative Commons license deed: creativecommons.org/licenses/by-nc/4.0/") adaptation) of [[Steele 1978](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#steele-1978 "RABBIT: A Compiler for SCHEME (A Dialect of LISP) A Study in Compiler Optimization Based on Viewing LAMBDA as RENAME and PROCEDURE CALL as GOTO using the techniques of Macro Definition of Control and Environment Structures Source-to-Source Transformation Procedure Integration and Tail-Recursion")], omitting text not in the chapter _Compiler Optimization Based on Viewing LAMBDA as RENAME plus GOTO_ (in _Artificial Intelligence, an MIT Perspective, Volume 2_ (MIT Press 1979) pp401-431) [[Steele 1979](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#steele-1979 "'Compiler Optimization Based on Viewing LAMBDA as RENAME plus GOTO' in Artificial Intelligence, an MIT Perspective, Volume 2 (MIT Press 1979) pp401-431")]

This title page, Contents, links, {{transcriber notes}}, and bridging text added.

## Compiler Optimization

Based on Viewing

LAMBDA as RENAME plus GOTO

Guy Lewis Steele Jr.

Massachusetts Institute of Technology

{{[RABBIT: A Compiler for SCHEME](https://dspace.mit.edu/handle/1721.1/6913/AITR-474.pdf "Original pdf at MIT: dspace.mit.edu/bitstream/handle/1721.1/6913/AITR-474.pdf") © 1978 by Guy Lewis Steele Jr, and this abridged transcription,

 licensed [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/ "Creative Commons license deed: creativecommons.org/licenses/by-nc/4.0/") (Attribution-NonCommercial 4.0 International).

 Transcription by Roger Turner: links, Contents page, {{transcriber notes}}, and bridging text added.

* * *

## Contents

* * *

## [1. Lexically-scoped LISP](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

We have developed a compiler for the lexically-scoped dialect of LISP known as SCHEME. The compiler knows relatively little about specific data manipulation primitives such as arithmetic operators, but concentrates on general issues of environment and control. Rather than having specialized knowledge about a large variety of control and environment constructs, the compiler handles only a small basis set which reflects the semantics of lambda-calculus. All of the traditional imperative constructs, such as sequencing, assignment, looping, `GOTO`, as well as many standard LISP constructs such as `AND`, `OR`, and `COND`, are expressed as macros in terms of the applicative basis set. A small number of optimization techniques, coupled with the treatment of function calls as `GOTO` statements, serve to produce code as good as that produced by more traditional compilers. The macro approach enables speedy implementation of new constructs as desired without sacrificing efficiency in the generated code.

A subset of SCHEME serves as the representation intermediate between the optimized SCHEME code and the final output code; code is expressed in this subset in the so-called _continuation-passing style_. As a subset of SCHEME, it enjoys the same theoretical properties; one could even apply the same optimizer used on the input code to the intermediate code. However, the subset is so chosen that all temporary quantities are made manifest as variables, and no control stack is needed to evaluate it. As a result, this apparently applicative representation admits an imperative interpretation which permits easy transcription to final imperative machine code.

### [A. Background](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

In [[SCHEME](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#scheme-1-2-3-4-5 "[1] Sussman and Steele 1975, SCHEME: An Interpreter for Extended Lambda Calculus")] we (Gerald Jay Sussman and the author) described the implementation of a dialect of LISP named SCHEME with the properties of lexical scoping and tail-recursion; this implementation is embedded within MacLISP [[Moon](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#moon-1-2 "[1] Moon 1974, MACLISP Reference Manual, Revision 0")], a version of LISP which does not have these properties. The property of lexical scoping (that a variable can be referenced only from points textually within the expression which binds it) is a consequence of the fact that all functions are closed in the “binding environment.” [[Moses](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#moses-1-2 "[1] Moses 1970, The Function of FUNCTION in LISP")] That is, SCHEME is a “full-funarg” LISP dialect. {Note [Full-Funarg Example](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#note-full-funarg-example "As an example of the difference between lexical and dynamic scoping, consider the classic case of the 'funarg problem'. We have defined a function MAPCAR which, given a function and a list, produces a new list of the results of the function applied to each element of the given list ...")} The property of tail-recursion implies that loops written in an apparently recursive form will actually be executed in an iterative fashion. Intuitively, function calls do not “push control stack”; instead, it is argument evaluation which pushes control stack. The two properties of lexical scoping and tail-recursion are not independent. In most LISP systems [[LISP1.5M](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#lisp1.5m "McCarthy etal 1962, LISP 1.5 Programmer's Manual")] [[Moon](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#moon-1-2 "[2] Moon 1974, MACLISP Reference Manual, Revision 0")] [[Teitelman](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#teitelman "Teitelman 1975, InterLISP Reference Manual. Revised edition")], which use dynamic scoping rather than lexical, tail-recursion is impossible because function calls must push control stack in order to be able to undo the dynamic bindings after the return of the function. On the other hand, it is possible to have a lexically scoped LISP which does not tail-recurse, but it is easily seen that such an implementation only wastes storage space needlessly compared to a tail-recursing implementation. [[Steele](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#steele-1-2-3-4-5 "[1] Steele 1977, Debunking the 'Expensive Procedure Call' Myth")] Together, these two properties cause SCHEME to reflect lambda-calculus semantics much more closely than dynamically scoped LISP systems. SCHEME also permits the treatment of functions as full-fledged data objects; they may be passed as arguments, returned as values, made part of composite data structures, and notated as independent, unnamed (“anonymous”) entities. (Contrast this with most ALGOL-like languages, in which a function can be written only by declaring it and giving it a name; imagine being able to use an integer value only by giving it a name in a declaration!) The property of lexical scoping allows this to be done in a consistent manner without the possibility of identifier conflicts (that is, SCHEME “solves the `FUNARG` problem” [[Moses](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#moses-1-2 "[2] Moses 1970, The Function of FUNCTION in LISP")]). In [[SCHEME](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#scheme-1-2-3-4-5 "[2] Sussman and Steele 1975, SCHEME: An Interpreter for Extended Lambda Calculus")] we also discussed the technique of “continuation-passing style”, a way of writing programs in SCHEME such that no function ever returns a value.

In [[Imperative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#imperative-1-2-3 "[1] Steele and Sussman 1976, LAMBDA: The Ultimate Imperative")] we explored ways of exploiting these properties to implement most traditional programming constructs, such as assignment, looping, and call-by-name, in terms of function application. Such applicative (lambda-calculus) models of programming language constructs are well-known to theoreticians (see [[Stoy](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#stoy "Stoy 1974, the Scott-Strachey Approach to the Mathematical Semantics of Programming Languages")], for example), but have not been used in a practical programming system. All of these constructs are actually made available in SCHEME by macros which expand into these applicative definitions. This technique has permitted the speedy implementation of a rich user-level language in terms of a very small, easy-to-implement basis set of primitive constructs. The escape operator `CATCH` is easily modelled by transforming a program into continuation-passing style. Transforming a program into this style enforces a particular order of argument evaluation, and makes all intermediate computational quantities manifest as variables.

In [[Declarative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#declarative-1-2-3-4-5-6-7 "[1] Steele 1976, LAMBDA: The Ultimate Declarative")] we examined more closely the issue of tail-recursion, and demonstrated that the usual view of function calls as pushing a return address must lead to an either inefficient or inconsistent implementation, while the tail-recursive approach of SCHEME leads to a uniform discipline in which function calls are treated as `GOTO` statements which also pass arguments. We also noted that a consequence of lexical scoping is that the only code which can reference the value of a variable in a given environment is code which is closed in that environment or which receives the value as an argument; this in turn implies that a compiler can structure a run-time environment in any arbitrary fashion, because it will compile all the code which can reference that environment, and so can arrange for that code to reference it in the appropriate manner. Such references do not require any kind of search (as is commonly and incorrectly believed in the LISP community because of early experience with LISP interpreters which search a-lists) because the compiler can determine the precise location of each variable in an environment at compile time. It is not necessary to use a standard format, because neither interpreted code nor other compiled code can refer to that environment.

In [[Declarative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#declarative-1-2-3-4-5-6-7 "[2] Steele 1976, LAMBDA: The Ultimate Declarative")] we also carried on the analysis of continuation-passing style, and noted that transforming a program into this style elucidates traditional compilation issues such as register allocation because user variables and intermediate quantities alike are made manifest as variables on an equal footing. Appendix A of [[Declarative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#declarative-1-2-3-4-5-6-7 "[3] Steele 1976B, LAMBDA: The Ultimate Declarative")] contained an algorithm for converting any SCHEME program (not containing `ASET`) to continuation-passing style.

We have implemented two compilers for the language SCHEME. The purpose was to explore compilation techniques for a language modelled on lambda-calculus, using lambda-calculus-style models of imperative programming constructs. Both compilers use the strategy of converting the source program to continuation-passing style.

The first compiler (known as CHEAPY) was written as a throw-away implementation to test the concept of conversion to continuation-passing style. The first half of CHEAPY is essentially the algorithm which appears in Appendix A of [[Declarative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#declarative-1-2-3-4-5-6-7 "[4] Steele 1976, LAMBDA: The Ultimate Declarative")], and the second is a simple code generator with almost no optimization. In conjunction with the writing of CHEAPY, the SCHEME interpreter was modified to interface to compiled functions.

The second compiler, with which we are primarily concerned here, is known as RABBIT. It, like CHEAPY, is written almost entirely in SCHEME (with minor exceptions due only to problems in interfacing with certain MacLISP I/O facilities). Unlike CHEAPY, it is fairly clever. It is intended to demonstrate a number of optimization techniques relevant to lexical environments and tail-recursive control structures.

### [B. The Thesis](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

1.   Function calls are not expensive when compiled correctly; they should be thought of as `GOTO` statements that happen to pass arguments.
2.   The combination of cheap function calls, lexical scoping, tail-recursion, and “anonymous” notation of functions (which are not independent properties of a language, but aspects of a single unified approach) permits the definition of a wide variety of “imperative” constructs in applicative terms. Because these properties result from adhering to the principles of the well-known lambda-calculus [[Church](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#church-1-2 "[1] Church 1941, The Calculi of Lambda Conversion")], such definitions can be lifted intact from existing literature and used directly.
3.   A macro facility (the ability to specify syntactic transformations) makes it practical to use these as the only definitions of imperative constructs in a programming system. Such a facility makes it extremely easy to define new constructs.
4.   A few well-chosen optimization strategies enable the compilation of these applicative definitions into the imperative low-level code which one would expect from a traditional compiler.
5.   The macro facility and the optimization techniques used by the compiler can be conceptually unified. The same properties which make it easy to write the macros make it easy to define optimizations correctly. In the same way that many programming constructs are defined in terms of a small, well- chosen basis set, so a large number of traditional optimization techniques fall out as special cases of the few used in RABBIT. This is no accident. The separate treatment of a large and diverse set of constructs necessitates separate optimization techniques for each. As the basis set of constructs is reduced, so is the set of interesting transformations. If the basis set is properly chosen, their combined effect is “multiplicative” rather than “additive”.
6.   The technique of compiling by converting to continuation-passing style elucidates some important compilation issues in a natural way. Intermediate quantities are made manifest; so is the precise order of evaluation. Moreover, this is all expressed in a language isomorphic to a subset of the source language SCHEME; as a result the continuation-passing style version of a program inherits many of the philosophical and practical advantages. For example, the same optimization techniques can be applied at this level as at the original source level. While the use of continuation-passing style may not make the decisions any easier, it provides an effective and natural way to express the results of those decisions.
7.   Continuation-passing style, while apparently applicative in nature, admits a peculiarly imperative interpretation as a consequence of the facts that it requires no control stack to be evaluated and that no functions ever return values. As a result, it is easily converted to an imperative machine language.
8.   A SCHEME compiler should ideally be a designer of good data structures, since it may choose any representation whatsoever for environments. RABBIT has a rudimentary design knowledge, involving primarily the preferral of registers to heap-allocated storage. However, there is room for knowledge of “bit-diddling” representations.
9.   We suggest that those who have tried to design useful UNCOL s (UNiversal Computer-Oriented Languages) [[Sammet](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#sammet "Sammet 1969, Programming Languages: History and Fundamentals")] [[Coleman](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#coleman "Coleman 1974, JANUS: A Universal Intermediate Language")] have perhaps been thinking too imperatively, and worrying more about data manipulation primitives than about environment and control issues. As a result, proposed UNCOL s have been little more than generalizations of contemporary machine languages. We suggest that SCHEME makes an ideal UNCOL at two levels. The first level is the fully applicative level, to which most source-language constructs are easily reduced; the second is the continuation-passing style level, which is easily reduced to machine language. We envision building a compiler in three stages: (a) reduction of a user language to basic SCHEME, whether by macros, a parser of algebraic syntax, or some other means; (b) optimization by means of SCHEME-level source-to-source transformations, and conversion to continuation-passing style; and (c) generation of code for a particular machine. RABBIT addresses itself to the second stage. Data manipulation primitives are completely ignored at this stage, and are just passed along from input to output. These primitives, whether integer arithmetic, string concatenation and parsing, or list structure manipulators, are chosen as a function of a particular source language and a particular target machine. RABBIT deals only with fundamental environment and control issues common to most modes of algorithmic expression.
10.   While syntactic issues tend to be rather superficial, we point out that algebraic syntax tends to obscure the fundamental nature of function calling and tail-recursion by arbitrarily dividing functions into syntactic classes such as “operators” and “functions”. ([[Standish](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#standish-1-2 "[1] Standish etal 1976, The Irvine Program Transformation Catalogue")], for example, uses much space to exhibit each conceptually singular transformation in a multiplicity of syntactic manifestations.) The lack of an “anonymous” notation for functions in most algebraic languages, and the inability to treat functions as data objects, is a distinct disadvantage. The uniformity of LISP syntax makes these issues easier to deal with.

To the LISP community in particular we address these additional points:

1.   Lexical scoping need not be as expensive as is commonly thought. Experience with lexically-scoped _interpreters_ is misleading; lexical scoping is not inherently slower than dynamic scoping. While some implementations may entail access through multiple levels of structure, this occurs only under circumstances (accessing of variables through multiple levels of closure) which could not even be expressed in a dynamically scoped language. Unlike deep-bound dynamic variables, compiled lexical access requires no search; unlike shallow-bound dynamic variables, lexical binding does not require that values be put in a canonical value cell. The compiler has complete discretion over the manipulation of environments and variable values. The “display” technique used in Algol implementations can be generalized to provide an efficient solution to the FUNARG problem.
2.   Lexical scoping does not necessarily make LISP programming unduly difficult. The very existence of RABBIT, a working compiler some fifty pages in length written in SCHEME, first implemented in about a month, part-time, substantiates this claim (which is, however, admitted to be mostly a matter of taste and experience). SCHEME has also been used to implement several AI problem-solving languages, including AMORD [[Doyle](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#doyle-1-2 "[1] Doyle etal 1977, Explicit Control of Reasoning")].

* * *

## [2. The Source Language - SCHEME](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

The basic language processed by RABBIT is a subset of the SCHEME language as described in [[SCHEME](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#scheme-1-2-3-4-5 "[3] Sussman and Steele 1975, SCHEME: An Interpreter for Extended Lambda Calculus")] the primary restrictions being that the first argument to `ASET` must be quoted and that the multiprocessing primitives are not accommodated. This subset is summarized here. SCHEME is essentially a lexically scoped (“full funarg”) dialect of LISP. Interpreted programs are represented by S-expressions in the usual manner. Numbers represent themselves. Atomic symbols are used as identifiers (with the conventional exception of `T` and `NIL`, which are conceptually treated as constants). All other constructs are represented as lists.

In order to distinguish the various other constructs, SCHEME follows the usual convention that a list whose car is one of a set of distinguished atomic symbols is treated as directed by a rule associated with that symbol. All other lists (those with non-atomic cars, or with undistinguished atoms in their cars) are _combinations_, or function calls. All subforms of the list are uniformly evaluated in an unspecified order, and then the value of the first (the function) is applied to the values of all the others (the arguments). Notice that the function position is evaluated in the same way as the argument positions (unlike most other LISP systems). (In order to be able to refer to MacLISP functions, global identifiers evaluate to a special kind of functional object if they have definitions as MacLISP functions of the `EXPR`, `SUBR`, or `LSUBR` varieties. Thus “`(PLUS 1 2)`” evaluates to `3` because the values of the subforms are <functional object for `PLUS`>, `1`, and `2`; and applying the first to the other two causes invocation of the MacLISP primitive `PLUS`.)

The atomic symbols which distinguish special constructs are as follows:

**`LAMBDA`** This denotes a function. A form `(LAMBDA (var1 var2 ... varn) body)` will evaluate to a function of n arguments. The **parameters**`vari` are identifiers (atomic symbols) which may be used in the body to refer to the respective **arguments** when the function is invoked. Note that a `LAMBDA`-expression is not a function, but _evaluates_ to one, a crucial distinction. **`IF`** This denotes a conditional form. `(IF a b c)` evaluates the **predicate**`a`, producing a value `x`; if `x` is non-`NIL`, then the **consequent**`b` is evaluated, and otherwise the **alternative**`c`. If `c` is omitted, `NIL` is assumed. **`QUOTE`** As in all LISP systems, this provides a way to specify any S-expression as a constant. `(QUOTE x)` evaluates to the S-expression `x`. This may be abbreviated to `'x`, thanks to the MacLISP read-macro-character feature. **`LABELS`** This primitive permits the local definition of one or more mutually recursive functions. The format is:

`(LABELS ((name1 (LAMBDA ...))`

`(name2 (LAMBDA ...))`

`...`

`(namen (LAMBDA ...)))`

`body)`

 This evaluates the `body` in an environment in which the names refer to the respective functions, which are themselves closed in that same environment. Thus references to these names in the bodies of the `LAMBDA`-expressions will refer to the labelled functions. **`ASET'`** This is the primitive side-effect on variables. `(ASET' var body)` evaluates the `body`, assigns the resulting value to the variable `var`, and returns that value. {Note [Non-quoted `ASET`](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#note-non-quoted-aset "The SCHEME interpreter permits one to compute the name of the variable, but for technical and philosophical reasons RABBIT forbids this. ...")} For implementation-dependent reasons, it is forbidden by RABBIT to use `ASET'` on a global variable which is the name of a primitive MacLISP function, or on a variable bound by `LABELS`. (`ASET'` is actually used very seldom in practice anyway, and all these restrictions are “good programming practice”. RABBIT could be altered to lift these restrictions, at some expense and labor.) **`CATCH`** This provides an escape operator facility. [[Landin](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#landin "Landin 1965, A Correspondence between ALGOL 60 and Church's Lambda-Notation")] [[Reynolds](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#reynolds "Reynolds 1972, Definitional Interpreters for Higher Order Programming Languages")] `(CATCH var body)` evaluates the `body`, which may refer to the variable `var`, which will denote an “escape function” of one argument which, when called, will return from the `CATCH`-form with the given argument as the value of the `CATCH`-form. Note that it is entirely possible to return from the `CATCH`-form several times. This raises a difficulty with optimization which will be discussed later. **Macros** Any atomic symbol which has been defined in one of various ways to be a macro distinguishes a special construct whose meaning is determined by a macro function. This function has the responsibility of rewriting the form and returning a new form to be evaluated in place of the old one. In this way complex syntactic constructs can be expressed in terms of simpler ones. 

* * *

## [3. The Target Language](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

The “target language” is a highly restricted subset of MacLISP, rather than any particular machine language for an actual hardware machine such as the PDP-10. RABBIT produces MacLISP function definitions which are then compiled by the standard MacLISP compiler. In this way we do not need to deal with the uninteresting vagaries of a particular piece of hardware, nor with the peculiarities of the many and various data-manipulation primitives (`CAR`, `RPLACA`, `+`, etc.). We allow the MacLISP compiler to deal with them, and concentrate on the issues of environment and control which are unique to SCHEME. While for production use this is mildly inconvenient (since the code must be passed through two compilers before use), for research purposes it has saved the wasteful re-implementation of much knowledge already contained in the MacLISP compiler.

On the other hand, the use of MacLISP as a target language does not by any means trivialize the task of RABBIT. The MacLISP function-calling mechanism cannot be used as a target construct for the SCHEME function call, because MacLISP’s function calls are not guaranteed to behave tail-recursively. Since tail-recursion is a most crucial characteristic distinguishing SCHEME from most LISP systems, we must implement SCHEME function calls by more primitive methods. Similarly, since SCHEME is a full-funarg dialect of LISP while MacLISP is not, we cannot in general use MacLISP’s variable-binding mechanisms to implement those of SCHEME. On the other hand, it is a perfectly legitimate optimization to use MacLISP mechanisms in those limited situations where they are applicable.

## [4. Language Design Considerations](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

We divide the definition of the SCHEME language into two parts: the environment and control constructs, and the data manipulation primitives. Examples of the former are `LAMBDA`-expressions, combinations, and `IF`; examples of the latter are `CONS`, `CAR`, `EQ`, and `PLUS`. Note that we can conceive of a version of SCHEME which did not have `CONS`, for example, and more generally did not have S-expressions in its data domain. Such a version would still have the same environment and control constructs, and so would hold the same theoretical interest for our purposes here. (Such a version, however, would be less convenient for purposes of writing a meta-circular description of the language, however!)

SCHEME is a lexically scoped (“full-funarg”) dialect of LISP, and so is an applicative language which conforms to the spirit of the lambda-calculus. [[Church](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#church-1-2 "[2] Church 1941, The Calculi of Lambda Conversion")] By the “spirit of lambda-calculus” we mean the essential properties of the axioms obeyed by lambda-calculus expressions. Among these are the rules of _alpha-conversion_ and _beta-conversion_. The first intuitively implies that we can uniformly rename a function parameter and all references to it without altering the meaning of the function. An important corollary to this is that we can in fact effectively locate all the references. The second implies that in a situation where a known function is being called with known argument expressions, we may substitute an argument expression for a parameter reference within the body of the function (provided no naming conflicts result, and that certain restrictions involving side effects are met). Both of these operations are of importance to an optimizing compiler. Another property which follows indirectly is that of _tail-recursion_. This property is exploited in expressing iteration in terms of applicative constructs, and is discussed in some detail in [[Declarative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#declarative-1-2-3-4-5-6-7 "[5] Steele 1976, LAMBDA: The Ultimate Declarative")].

There are those to whom lexical scoping is nothing new, for example the ALGOL community. For this audience, however, we should draw attention to another important feature of SCHEME, which is that functions are first-class data objects. They may be assigned or bound to variables, returned as values of other functions, placed in arrays, and in general treated as any other data object. Just as numbers have certain operations defined on them, such as addition, so functions have an important operation defined on them, namely invocation.

The ability to treat functions as objects is not at all the same as the ability to treat _representations_ of functions as objects. It is the latter ability that is traditionally associated with LISP; functions can be represented as S-expressions. In a version of SCHEME which had no S-expression primitives, however, one could still deal with functions (i.e.closures) as such, for that ability is part of the fundamental environment and control facilities. Conversely, in a SCHEME which does have `CONS`, `CAR`, and `CDR`, there is no defined way to use `CONS` by itself to construct a function (although a primitive `ENCLOSE` is now provided which converts an S-expression representation of a function into a function), and the `CAR` or `CDR` of a function is in general undefined. The only defined operation on a function is invocation. {Note [Operations on Functions](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#note-operations-on-functions "It would certainly be possible to define other operations on functions, such as determining the number of arguments required, or the types of the arguments and returned value, etc. ...")}

We draw this sharp distinction between environment and control constructs on the one hand and data manipulation primitives on the other because only the former are treated in any depth by RABBIT, whereas much of the knowledge of a “real” compiler deals with the latter. A PL/I compiler must have much specific knowledge about numbers, arrays, strings, and so on. We have no new ideas to present here on such issues, and so have avoided this entire area. RABBIT itself knows almost nothing about data manipulation primitives beyond being able to recognize them and pass them along to the output code, which is a small subset of MacLISP. In this way RABBIT can concentrate on the interesting issues of environment and control, and exploit the expert knowledge of data manipulation primitives already built into the MacLISP compiler.

* * *

## [5. The Use of Macros](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

An important characteristic of the SCHEME language is that its set of primitive constructs is quite small. This set is not always convenient for expressing programs, however, and so a macro facility is provided for extending the expressive power of the language. A macro is best thought of as a _syntax rewrite rule_. As a simple example, suppose we have a primitive `GCD` which takes only two arguments, and we wish to be able to write an invocation of a `GCD` function with any number of arguments. We might then define (in a “production-rule” style) the conditional rule:

```
(XGCD)          => 0
    (XGCD x)        => x
    (XGCD x . rest) => (GCD x (XGCD . rest))
```

(Notice the use of LISP dots to refer to the rest of a list.) This is not considered to be a definition of a function `XGCD`, but a purely syntactic transformation. In principle all such transformations could be performed before executing the program. In fact, RABBIT does exactly this, although the SCHEME interpreter naturally does it incrementally, as each macro call is encountered.

Rather than use a separate production-rule/pattern-matching language, in practice SCHEME macros are defined as transformation functions from macro-call expressions to resulting S-expressions, just as they are in MacLISP. (Here, however, we shall continue to use production rules for purposes of exposition.) It is important to note that macros need not be written in the language for which they express rewrite rules; rather, they should be considered an adjunct to the interpreter, and written in the same language as the interpreter (or the compiler). To see this more clearly, consider a version of SCHEME which does not have S-expressions in its data domain. If programs in this language are represented as S-expressions, then the interpreter for that language cannot be written in that language, but in another meta-language which does deal with S-expressions. Macros, which transform one S-expression (representing a macro call) to another (the replacement form, or the interpretation of the call), clearly should be expressed in this meta-language also. The fact that in most LISP systems the language and the meta-language appear to coincide is a source of both power and confusion.

We shall give some examples here. The `BLOCK` macro is similar to the MacLISP`PROGN`; it evaluates all its arguments and returns the value of the last one. One critical characteristic is that the last argument is evaluated “tail-recursively” (I use horror quotes because normally we speak of invocation, not evaluation, as being tail-recursive). An expansion rule is given for this in [[Imperative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#imperative-1-2-3 "[2] Steele and Sussman 1976, LAMBDA: The Ultimate Imperative")] equivalent to:

```
(BLOCK x)         =>  x
    (BLOCK x . rest)  =>  ((LAMBDA (DUMMY) (BLOCK . rest)) x)
```

This definition exploits the fact that SCHEME is evaluated in applicative order, and so will evaluate all arguments before applying a function to them. Thus, in the second subrule, `x` must be evaluated, and then the block of all the `rest` is. It is then clear from the first subrule that the last argument is evaluated “tail-recursively”.

One problem with this definition is the occurrence of the variable `DUMMY`, which must be chosen so as not to conflict with any variable used by the user. This we refer to as the “`GENSYM` problem”, in honor of the traditional LISP function which creates a “fresh” symbol. It would be nicer to write the macro in such a way that no conflict could arise no matter what names were used by the user. There is indeed a way, which ALGOL programmers will recognize as equivalent to the use of “thunks”, or call-by-name parameters:

```
(BLOCK x)         =>  x
    (BLOCK x . rest)  =>  ((LAMBDA (A B) (B))
                           x
                           (LAMBDA () (BLOCK . rest)))
```

This is a technique which should be understood quite thoroughly, since it is the key to writing correct macro rules without any possibility of conflicts between names used by the user and those needed by the macro. As another example, let us consider the `AND` and `OR` constructs as used by most LISP systems. `OR` evaluates its arguments one by one, in order, returning the first non-`NIL` value obtained (without evaluating any of the following arguments), or `NIL` if all arguments produce `NIL`. `AND` is the dual to this; it returns `NIL` if any argument does, and otherwise the value of the last argument. A simple-minded approach to `OR` would be:

```
(OR)           =>  'NIL
    (OR x . rest)  =>  (IF x x (OR . rest))
```

There is an objection to this, which is that the code for `x` is duplicated. Not only does this consume extra space, but it can execute erroneously if `x` has any side-effects. We must arrange to evaluate x only once, and then test its value:

```
(OR)           =>  'NIL
    (OR x . rest)  =>  ((LAMBDA (V) (IF V V (OR . rest))) x)
```

This certainly evaluates `x` only once, but admits a possible naming conflict between the variable `V` and any variables used by rest. This is avoided by the same technique used for `BLOCK`:

```
(OR)          =>  'NIL
    (OR x . rest)  =>  ((LAMBDA (V R) (IF V V (R)))
                      x
                      (LAMBDA () (OR . rest)))
```

Let us now consider a rule for the more complicated `COND` construct:

```
(COND)                 =>  'NIL
    (COND (x) . rest)      =>  (OR x (COND . rest))
    (COND (x . r) . rest)  =>  (IF x (BLOCK . r) (COND . rest))
```

This defines the “extended” `COND` of modern LISP systems, which produces `NIL` if no clauses succeed, which returns the value of the predicate in the case of a singleton clause, and which allows more than one consequent in a clause. An important point here is that one can write these rules in terms of other macro constructs such as `OR` and `BLOCK`.

SCHEME also provides macros for such constructs as `DO` and `PROG`, all of which expand into similar kinds of code using `LAMBDA`, `IF`, and `LABELS` (see below). In particular, `PROG` permits the use of `GO` and `RETURN` in the usual manner. In this manner all the traditional imperative constructs are expressed in an applicative manner. {Note [`ASET'` Is Imperative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#note-aset-is-imperative-1-2 "It is true that ASET' is an actual imperative which produces a side effect, and is not expressed applicatively. ASET' is used only for two purposes in practice: to initialize global variables (often relating to MacLISP primitives), and to implement objects with state ...")}

None of this is particularly new; theoreticians have modelled imperative constructs in these terms for years. What is new, we think, is the serious proposal that a practical interpreter and compiler can be designed for a language in which such models serve as the _sole definitions_ of these imperative constructs. {Note [Dijkstra’s Opinion](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#note-dijkstras-opinion "In [Dijkstra] a remark is made to the effect that defining the while-do construct in terms of function calls seems unusually clumsy. In [Steele] we reply that this is due partly to Dijkstra’s choice of ALGOL for expressing the definition. ...")} This approach has both advantages and disadvantages.

One advantage is that the base language is small. A simple-minded interpreter or compiler can be written in a few hours. (We have re-implemented the SCHEME interpreter from scratch a dozen times or more to test various representation strategies; this was practical only because of the small size of the language. Similarly, the CHEAPY compiler is fewer than ten pages of code, and could be rewritten in a day or less.) Once the basic interpreter is written, the macro definitions for all the complex constructs can be used without revision. Moreover, the same macro definitions can be used by both interpreter and compiler (or by several versions of interpreter and compiler!). Excepting the very few primitives such as `LAMBDA` and `IF`, it is not necessary to “implement a construct twice”, once each in interpreter and compiler.

Another advantage is that new macros are very easy to write (using facilities provided in SCHEME). One can easily invent a new kind of `DO` loop, for example, and implement it in SCHEME for both interpreter and all compilers in less than five minutes.

A third advantage is that the attention of the compiler can be focused on the basic constructs. Rather than having specialized code for two dozen different constructs, the compiler can have much deeper knowledge about each of a few basic constructs. One might object that this “deeper knowledge” consists of recognizing the two dozen special cases represented by the separate constructs of the former case. This is true to some extent. It is also true, however, that in the latter case such deep knowledge will carry over to any new constructs which are invented and represented as macros.

Among the disadvantages of the macro approach are lack of speed and the discarding of information. Many people have objected that macros are of necessity slower than, say, the `FSUBR` implementation used by most LISP systems. This is true in many current interpretive implementations, but need not be true of compilers or more cleverly designed interpreters. Moreover, the `FSUBR` implementation is not general; it is very hard for a user to write a meaningful `FSUBR` and then describe to the compiler the best way to compile it. The macro approach handles this difficulty automatically. We do not object to the use of the `FSUBR` mechanism as a special-case “speed hack” to improve the performance of an interpreter, but we insist on recognizing the fact that it is not as generally useful as the macro approach.

Another objection relating to speed is that the macros produce convoluted code involving the temporary creation and subsequent invocation of many closures. We feel, first of all, that the macro writer should concern himself more with producing correct code than fast code. Furthermore, convolutedness can be eliminated by a few simple optimization techniques in the compiler, to be discussed below. Finally, function calls need not be as expensive as is popularly supposed. [[Steele](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#steele-1-2-3-4-5 "[2] Steele 1977, Debunking the 'Expensive Procedure Call' Myth")]

Information is discarded by macros in the situation, for example, where a `DO` macro expands into a large mess that is not obviously a simple loop; later compiler analysis must recover this information. This is indeed a problem. We feel that the compiler is probably better off having to recover the information anyway, since a deep analysis allows it to catch other loops which the user did not use `DO` to express for one reason or another. Another is the possibility that `DO` could leave clues around in the form of declarations if desired.

* * *

## [6. The Imperative Treatment of Applicative Constructs](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

Given the characteristics of lexical scoping and tail-recursive invocations, it is possible to assign a peculiarly imperative interpretation to the applicative constructs of SCHEME, which consists primarily of treating a function call as a `GOTO`. More generally, a function call is a `GOTO` that can pass one or more items to its target; the special case of passing no arguments is precisely a `GOTO`. It is never necessary for a function call to save a return address of any kind. It is true that return addresses are generated, but we adopt one of two other points of view, depending on context. One is that the return address, plus any other data needed to carry on the computation after the called function has returned (such as previously computed intermediate values and other return addresses) are considered to be packaged up into an additional argument (the **continuation**) which is passed to the target. This lends itself to a non-functional interpretation of `LAMBDA`, and a method of expressing programs called the continuation-passing style (similar to the message-passing actors paradigm), to be discussed further below. The other view, more intuitive in terms of the traditional stack implementation, is that the return address should be pushed before evaluating arguments rather than before calling a function. This view leads to a more uniform function-calling discipline, and is discussed in [[Declarative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#declarative-1-2-3-4-5-6-7 "[6] Steele 1976, LAMBDA: The Ultimate Declarative")] and [[Steele](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#steele-1-2-3-4-5 "[3] Steele 1977, Debunking the 'Expensive Procedure Call' Myth")].

We are led by this point of view to consider a compilation strategy in which function calling is to be considered very cheap (unlike the situation with PL/I and ALGOL, where programmers avoid procedure calls like the plague — see [[Steele](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#steele-1-2-3-4-5 "[4] Steele 1977, Debunking the 'Expensive Procedure Call' Myth")] for a discussion of this). In this light the code produced by the sample macros above does not seem inefficient, or even particularly convoluted. Consider the expansion of `(OR a b c)`:

```
((LAMBDA (V R) (IF V V (R)))
     a
     (LAMBDA () ((LAMBDA (V R) (IF V V (R)))
                 b
                 (LAMBDA () ((LAMBDA (V R) (IF V V (R)))
                             c (LAMBDA () 'NIL))))))
```

Then we might imagine the following (slightly contrived) compilation scenario. First, for expository purposes, we shall rename the variables in order to be able to distinguish them.

```
((LAMBDA (V1 R1) (IF V1 V1 (R1)))
     a
     (LAMBDA () ((LAMBDA (V2 R2) (IF V2 V2 (R2)))
                 b
                 (LAMBDA () ((LAMBDA (V3 R3) (IF V3 V3 (R3)))
                             c
                             (LAMBDA () 'NIL))))))
```

We shall assign a generated name to each `LAMBDA`-expression, which we shall notate by writing the name after the word `LAMBDA`. These names will be used as tags in the output code.

```
((LAMBDA name1 (V1 R1) (IF V1 V1 (R1)))
     a
     (LAMBDA name2 () ((LAMBDA name3 (V2 R2) (IF V2 V2 (R2)))
                       b
                       (LAMBDA name4 () ((LAMBDA name5 (V3 R3) (IF V3 V3 (R3)))
                                         c
                                         (LAMBDA name6 () 'NIL))))))
```

Next, a simple analysis shows that the variables `R1`, `R2`, and `R3` always denote the `LAMBDA`-expressions named `name2`, `name4`, and `name6`, respectively. Now an optimizer might simply have substituted these values into the bodies of `name1`, `name3`, and `name5` using the rule of beta-conversion, but we shall not apply that technique here. Instead we shall compile the six functions in a straightforward manner. We make use of the additional fact that all six functions are closed in identical environments (we count two environments as identical if they involve the same variable bindings, regardless of the number of “frames” involved; that is, the environment is the same inside and outside a `(LAMBDA () ...))`. Assume a simple target machine with argument registers called `reg1`, `reg2`, etc.

```
main:   <code for a>            ;result in reg1
            LOAD reg2,[name2]       ;[name2] is the closure for name2
            CALL-FUNCTION 2,[namel] ;call name1 with 2 arguments

    name1:  JUMP-IF-NIL reg1,name1a
            RETURN                  ;return the value in reg1
    name1a: CALL-FUNCTION 0,reg2    ;call function in reg2, 0 arguments

    name2:  <code for b>            ;result in reg1
            LOAD reg2,[name4]       ;[name4] is the closure for name4
            CALL-FUNCTION 2,[name3] ;call name3 with 2 arguments

    name3:  JUMP-IF-NIL reg1,name3a
            RETURN                  ;return the value in reg1
    name3a: CALL-FUNCTION 0,reg2    ;call function in reg2, 0 arguments

    name4:  <code for c>            ;result in reg1
            LOAD reg2,[name6]       ;[name6] is the closure for name6
            CALL-FUNCTION 2,[name5] ;call name5 with 2 arguments

    name5:  JUMP-IF-NIL reg1,name5a
            RETURN                  ;return the value in reg1
    name5a: CALL-FUNCTION 0,reg2    ;call function in reg2, 0 arguments

    name6:  LOAD reg1,'NIL          ;constant NIL in reg1
            RETURN
```

Now we make use of our knowledge that certain variables always denote certain functions, and convert `CALL-FUNCTION` of a known function to a simple `GOTO`. (We have actually done things backwards here; in practice this knowledge is used _before_ generating any code. We have fudged over this issue here, but will return to it later. Our purpose here is merely to demonstrate the treatment of function calls as `GOTO`s.)

```
main:   <code for a>            ;result in reg1
            LOAD reg2,[name2]       ;[name2] is the closure for name2
            GOTO name1

    name1:  JUMP-IF-NIL reg1,name1a
            RETURN                  ;return the value in reg1
    name1a: GOTO name2

    name2:  <code for b>            ;result in reg1
            LOAD reg2,[name4]       ;[name4] is the closure for name4
            GOTO name3

    name3:  JUMP-IF-NIL reg1,name3a
            RETURN                  ;return the value in reg1
    name3a: GOTO name4

    name4:  <code for c>            ;result in reg1
            LOAD reg2,[name6]       ;[name6] is the closure for name6
            GOTO name5

    name5:  JUMP-IF-NIL reg1,name5a
            RETURN                  ;return the value in reg1
    name5a: GOTO name6

    name6:  LOAD reg1,'NIL          ;constant NIL in reg1
            RETURN
```

The construction `[foo]` indicates the creation of a closure for `foo` in the current environment. This will actually require additional instructions, but we shall ignore the mechanics of this for now since analysis will remove the need for the construction in this case. The fact that the _only_ references to the variables `R1`, `R2`, and `R3` are function calls can be detected and the unnecessary `LOAD` instructions eliminated. (Once again, this would actually be determined ahead of time, and no `LOAD` instructions would be generated in the first place. All of this is determined by a general pre-analysis, rather than a peephole post-pass.) Moreover, a `GOTO` to a tag which immediately follows the `GOTO` can be eliminated.

```
main:   <code for a>            ;result in reg1
    name1:  JUMP-IF-NIL reg1,name1a
            RETURN                  ;return the value in reg1

    name1a:
    name2:  <code for b>            ;result in reg1
    name3:  JUMP-IF-NIL reg1,name3a
            RETURN                  ;return the value in reg1

    name3a:
    name4:  <code for c>            ;result in reg1
    name5:  JUMP-IF-NIL reg1,name5a
            RETURN                  ;return the value in reg1

    name5a:
    name6:  LOAD reg1,'NIL          ;constant NIL in reg1
            RETURN
```

This code is in fact about what one would expect out of an ordinary LISP compiler. (There is admittedly room for a little more improvement.) RABBIT indeed produces code of essentially this form, by the method of analysis outlined here.

Similar considerations hold for the `BLOCK` macro. Consider the expression `(BLOCK a b c)`; conceptually this should perform `a`, `b`, and `c` sequentially. Let us examine the code produced:

```
main:   <code for a>
    name1:
    name2:  <code for b>
    name3:
    name4:  <code for c>
            RETURN
```

What more could one ask for?

Notice that this has fallen out of a general strategy involving only an approach to compiling _function calls_, and has involved no special knowledge of `OR` or `BLOCK` not encoded in the macro rules. The cases shown so far are actually special cases of a more general approach, special in that all the conceptual closures involved are closed in the same environment, and called from places that have not disturbed that environment, but only used “registers.” In the more general case, the environments of caller and called function will be different. This divides into two subcases, corresponding to whether the closure was created by a simple `LAMBDA` or by a `LABELS` construction. The latter involves circular references, and so is somewhat more complicated; but it is easy to show that in the former case the environment of the caller must be that of the (known) called function, possibly with additional values added on. This is a consequence of lexical scoping. As a result, the function call can be compiled as a `GOTO` preceded by an environment adjustment which consists merely of lopping off some leading portion of the current one (intuitively, one simply “pops the unnecessary crud off the stack”). `LABELS`-closed functions also can be treated in this way, if one closes all the functions in the same way (which RABBIT presently does, but this is not always desirable). If one does, then it is easy to see the effect of expanding a `PROG` into a giant `LABELS` as outlined in [[Imperative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#imperative-1-2-3 "[3] Steele and Sussman 1976, LAMBDA: The Ultimate Imperative")] and elsewhere: normally, a `GOTO` to a tag at the same level of PROG will involve no adjustment of environment, and so compile into a simple `GOTO` instruction, whereas a `GOTO` to a tag at an outer level of PROG probably will involve adjusting the environment from that of the inner `PROG` to that of the outer. All of this falls out of the proper imperative treatment of function calls.

### [A. Optimization](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

Once the preliminary analysis is done, the optimization phase performs certain transformations on the code. The result is an equivalent program which will (probably) compile into more efficient code. This new program is itself structurally a valid SCHEME program; that is, all transformations are contained within the language. The transformations are thus similar to those performed on macro calls, consisting of a syntactic rewriting of an expression, except that the situations where such transformations are applicable are more easily recognized in the case of macro calls. It should be clear that the optimizer and the macro-functions are conceptually at the same level in that they may be written in the same meta-language that operates on representations of SCHEME programs. {Note [Non-deterministic Optimization](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#note-non-deterministic-optimization "To simplify the implementation, RABBIT uses only a deterministic (and very conservative) optimizer. Ideally, an optimizer would be non-deterministic in structure ...")}

The simplest transformation is that a combination whose function position contains a `LAMBDA`-expression and which has no arguments can be replaced by the body of the `LAMBDA`-expression:

`((LAMBDA () body))  =>  body`
There are two transformations on `IF` expressions. One is simply that an `IF` expression with a constant predicate is simplified to its consequent or alternative (resulting in elimination of dead code). The other was adapted from [[Standish](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#standish-1-2 "[2] Standish etal 1976, The Irvine Program Transformation Catalogue")], which does not have this precise transformation listed, but gives a more general rule. In its original form this transformation is:

`(IF (IF a b c) d e)  =>  (IF a (IF b d e) (IF c d e))`
One problem with this is that the code for d and e is duplicated. This can be avoided by the use of `LAMBDA`-expressions:

```
((LAMBDA (Q1 Q2)
             (IF a
                 (IF b (Q1) (Q2))
                 (IF c (Q1) (Q2))))
     (LAMBDA () d)
     (LAMBDA () e))
```

As before, there is no problem of name conflicts with Q1 and Q2. While this code may appear unnecessarily complex, the calls to the functions `Q1` and `Q2` will, typically, as shown above, be compiled as simple `GOTO`s. As an example, consider the expression:

`(IF (AND PRED1 PRED2) (PRINT 'WIN) (ERROR 'LOSE))`
Expansion of the `AND` macro will result in:

```
(IF ((LAMBDA (V R) (IF V (R) 'NIL))
         PRED1
         (LAMBDA () PRED2))
        (PRINT 'WIN)
        (ERROR 'LOSE))
```

(For expository clarity we will not bother to rename all the variables, inasmuch as they are already distinct.) Because `V` and `R` have only one reference apiece (and there are no possible interfering side-effects), the corresponding arguments can be substituted for them.

```
(IF ((LAMBDA (V R) (IF PRED1 ((LAMBDA () PRED2)) 'NIL))
         PRED1
         (LAMBDA () PRED2))
        (PRINT 'WIN)
        (ERROR 'LOSE) )
```

Now, since `V` and `R` have no referents at all, they and the corresponding arguments can be eliminated, since the arguments have no side-effects.

```
(IF ((LAMBDA () (IF PRED1 ((LAMBDA () PRED2)) 'NIL)))
        (PRINT 'WIN)
        (ERROR 'LOSE))
```

Next, the combination `((LAMBDA () ...))` is eliminated in two places:

```
(IF (IF PRED1 PRED2 'NIL)
        (PRINT 'WIN)
        (ERROR 'LOSE))
```

Now, the transformation on the nested `IF`’s:

```
((LAMBDA (Q1 Q2)
             (IF PRED1
                 (IF PRED2 (Q1) (Q2))
                 (IF 'NIL (Q1) (Q2))))
     (LAMBDA () (PRINT 'WIN))
     (LAMBDA () (ERROR 'LOSE)))
```

Now one `IF` has a constant predicate and can be simplified:

```
((LAMBDA (Q1 Q2)
             (IF PRED1
                 (IF PRED2 (Q1) (Q2))
                 (Q2)))
     (LAMBDA () (PRINT 'WIN))
     (LAMBDA () (ERROR 'LOSE)))
```

The variable `Q1` has only one referent, and so we substitute in, eliminate the variable and argument, and collapse a `((LAMBDA () ...))`:

```
((LAMBDA (Q2)
             (IF PRED1
                 (IF PRED2 (PRINT 'WIN) (Q2))
                 (Q2)))
     (LAMBDA () (ERROR 'LOSE)))
```

Recalling that `(Q2)` is, in effect, a `GOTO` branching to the common piece of code, and that by virtue of later analysis no actual closure will be created for either `LAMBDA`-expression, this result is quite reasonable. {Note [Evaluation for Control](#note-evaluation-for-control “It is usual in a compiler to distinguish at least three ‘evaluation contexts’: value, control, and effect. (See [[Wulf](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#wulf-1-2 "[1] Wulf 1975, The Design of an Optimizing Compiler")], for example.) Evaluation for control occurs in the predicate of an IF, where the point is not so much to produce a data object as simply to decide whether it is true or false. …”){#xevaluation}}

* * *

### [B. Environment and Closure Analysis](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

Following CPS conversion (see [Appendix](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#appendix)), RABBIT determines for each `LAMBDA`-expression whether a closure will be needed for it at run time. The idea is that in many situations (particularly those generated as expansions of macros) one can determine at compile time precisely which function will be invoked by a combination, and perhaps also what its expected environment will be. There are three possibilities:

1.   If the function denoted by the `LAMBDA`-expression is bound to some variable, and that variable is referenced other than in function position, then the closure is being treated as data, and must be a full (standard `CBETA` format) closure. If the function itself occurs in non-function position other than in a `LAMBDA`-combination, it must be fully closed.
2.   If the closure is bound to some variable, and that variable is referenced only in function position, but some of these references occur within other partially or fully closed functions, then this function must be partially closed. By this we mean that the environment for the closure must be “consed up”, but no pointer to the code need be added on as for a full closure. This function will always be called from places that know the name of the function and so can just perform a `GO` to the code, but those such places which are within closures must have a complete copy of the necessary environment.
3.   In other cases (functions bound to variables referenced only in function position and never within a closed function, or functions occurring in function position of `LAMBDA`-combinations), the function need not be closed. This is because the environment can always be fully recovered from the environment at the point of call.

In order to determine this information, it is necessary to determine, for each node, the set of variables referred to from within closed functions at or below that node. Thus this process and the process of determining functions to close are highly interdependent, and so must be accomplished in a single pass.

* * *

## [7. Conclusions](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

Lexical scoping, tail-recursion, the conceptual treatment of functions (as opposed to representations thereof) as data objects, and the ability to notate “anonymous” functions make SCHEME an excellent language in which to express program transformations and optimizations. Imperative constructs are easily modelled by applicative definitions. Anonymous functions make it easy to avoid needless duplication of code and conflict of variable names. A language with these properties is useful not only at the preliminary optimization level, but for expressing the results of decisions about order of evaluation and storage of temporary quantities. These properties make SCHEME as good a candidate as any for an UNCOL. The proper treatment of functions and function calls leads to generation of excellent imperative low-level code.

We have emphasized the ability to treat functions as data objects. We should point out that one might want to have a very simple run-time environment which did not support complex environment structures, or even stacks. Such an end environment does not preclude the use of the techniques described here. Many optimizations result in the elimination of `LAMBDA`-expressions; post CPS-conversion analysis eliminates the need to close many of the remaining `LAMBDA`-expressions. One could use the macros and internal representations of RABBIT to describe intermediate code transformations, and require that the final code not actually create any closures. As a concrete example, imagine writing an operating system in SCHEME, with machine words as the data domain (and functions excluded from the run-time data domain). We could still meaningfully write, for example:

```
(IF (OR (STOPPED (PROCESS I))
            (AWAITING-INPUT (PROCESS I)))
        (SCHEDULE-LOOP (+ I 1))
        (SCHEDULE-PROCESS I))
```

While the intermediate expansion of this code would conceptually involve the use of functions as data objects, optimizations would reduce the final code to a form which did not require closures at run time.

* * *

## [Notes](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

#### {Note `ASET'` Is Imperative} [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xaset-is-imperative1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xaset-is-imperative2)

It is true that `ASET'` is an actual imperative which produces a side effect, and is not expressed applicatively. `ASET'` is used only for two purposes in practice: to initialize global variables (often relating to MacLISP primitives), and to implement objects with state (cells, in the PLASMA sense [[Smith and Hewitt](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#smith-and-hewitt "Smith and Hewitt 1975, A PLASMA Primer (draft)")] [[Hewitt and Smith](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#hewitt-and-smith "Hewitt and Smith 1975, Towards a Programming Apprentice")]). If we were to redesign SCHEME from scratch, I imagine that we would introduce cells as our primitive side-effect rather than `ASET'`. The decision to use `ASET'` was motivated primarily by the desire to interface easily to the MacLISP environment (and, as a corollary, to be able to implement SCHEME in three days instead of three years!).

We note that in approximately one hundred pages of SCHEME code written by three people, the non-quoted `ASET` has never been used, and `ASET'` has been used only a dozen times or so, always for one of the two purposes mentioned above. In most situations where one would like to write an assignment of some kind, macros which expand into applicative constructions suffice.

#### {Note Dijkstra’s Opinion} [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdijkstras-opinion)

In [[Dijkstra](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#dijkstra "Dijkstra 1976, A Discipline of Programming")] a remark is made to the effect that defining the **while**-**do** construct in terms of function calls seems unusually clumsy. In [[Steele](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#steele-1-2-3-4-5 "[5] Steele 1977, Debunking the 'Expensive Procedure Call' Myth")] we reply that this is due partly to Dijkstra’s choice of ALGOL for expressing the definition. Here we would add that, while such a definition is completely workable and is useful for compilation purposes, we need never tell the user that we defined **while**-**do** in this manner! Only the writer of the macros needs to know the complexity involved; the user need not, and should not, care as long as the construction works when he uses it.

#### {Note Evaluation for Control} [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xevaluation)

It is usual in a compiler to distinguish at least three “evaluation contexts”: value, control, and effect. (See [[Wulf](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#wulf-1-2 "[2] Wulf 1975, The Design of an Optimizing Compiler")], for example.) Evaluation for control occurs in the predicate of an `IF`, where the point is not so much to produce a data object as simply to decide whether it is true or false. The results of `AND`, `OR`, and `NOT` operations in predicates are “encoded in the program counter”. When compiling an `AND`, `OR`, or `NOT`, a flag is passed down indicating whether it is for value or for control; in the latter case, two tags are also passed down, indicating the branch targets for success or failure. (This is called “anchor pointing” in [[Allen](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#allen "Allen and Cocke 1972, A Catalogue of Optimizing Transformations")].)

In RABBIT this notion falls out automatically without any special handling, thanks to the definition of `AND` and `OR` as macros expanding into `IF` statements. If we were also to define `NOT` as a macro

`(NOT x)  =>  (IF x 'NIL 'T)`
then nearly all such special “evaluation for control” cases would be handled by virtue of the nested-`IF` transformation in the optimizer.

One transformation which ought to be in the optimizer is

```
(IF ((LAMBDA (X Y ...) <body>) A B ...) <con> <alt>)
       =>  ((LAMBDA (X Y ...) (IF <body> <con> <alt>)) A B ...)
```

which could be important if the `<body>` is itself an `IF`. (This transformation would occur at a point (in the optimizer) where no conflicts between `X`, `Y`, and variables used in `<con>` and `<alt>` could occur.)

#### {Note Full-Funarg Example} [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xfull-funarg-example)

As an example of the difference between lexical and dynamic scoping, consider the classic case of the “funarg problem”. We have defined a function `MAPCAR` which, given a function and a list, produces a new list of the results of the function applied to each element of the given list:

```
(DEFINE MAPCAR
            (LAMBDA (FN L)
                    (IF (NULL L) NIL
                        (CONS (FN (CAR L)) (MAPCAR FN (CDR L))))))
```

Now suppose in another program we have a list `X` and a number `L`, and want to add `L` to every element of `X`:

`(MAPCAR (LAMBDA (Z) (+ Z L)) X)`
This works correctly in a lexically scoped language such as SCHEME, because the `L` in the function `(LAMBDA (Z) (+ Z L))` refers to the value of `L` at the point the `LAMBDA`-expression is evaluated. In a dynamically scoped language, such as standard LISP, the `L` refers to the most recent run-time binding of `L`, which is the binding in the definition of `MAPCAR` (which occurs between the time the `LAMBDA`-expression is passed to `MAPCAR` and the time the `LAMBDA`-expression is invoked).

#### {Note Non-deterministic Optimization} [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xnon-deterministic-optimization)

To simplify the implementation, RABBIT uses only a deterministic (and very conservative) optimizer. Ideally, an optimizer would be non-deterministic in structure; it could try an optimization, see how the result interacted with other optimizations, and back out if the end result is not as good as desired. We have experimented briefly with the use of the AMORD language [[Doyle](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#doyle-1-2 "[2] Doyle etal 1977, Explicit Control of Reasoning")] to build a non-deterministic compiler, but have no significant results yet.

We can see more clearly the fundamental unity of macros and other optimizations in the light of this hypothetical non-deterministic implementation. Rather than trying to guess ahead of time whether a macro expansion or optimization is desirable, it goes ahead and tries, and then measures the utility of the result. The only difference between a macro and other optimizations is that a macro call is an all-or-nothing situation: if it cannot be expanded for some reason, it is of infinite disutility, while if it can its disutility is finite. This leads to the idea of non-deterministic macro expansions, which we have not pursued.

#### {Note Non-quoted `ASET`} [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xnon-quoted-aset)

The SCHEME interpreter permits one to compute the name of the variable, but for technical and philosophical reasons RABBIT forbids this. We shall treat “`ASET'`” as a single syntactic object (think “`ASETQ`”).

(See also {Note [`ASET'` Is Imperative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#note-aset-is-imperative-1-2 "It is true that ASET' is an actual imperative which produces a side effect, and is not expressed applicatively. ASET' is used only for two purposes in practice: to initialize global variables (often relating to MacLISP primitives), and to implement objects with state ...")}.)

#### {Note Operations on Functions} [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xoperations-on-functions)

It would certainly be possible to define other operations on functions, such as determining the number of arguments required, or the types of the arguments and returned value, etc.

* * *

## [References](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

(Entries marked with a “*” are not referenced in the text.)

#### [Allen] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xallen)

Allen, Frances E., and Cocke, John. [_A Catalogue of Optimizing Transformations_](https://www.clear.rice.edu/comp512/Lectures/Papers/1971-allen-catalog.pdf "www.clear.rice.edu/comp512/Lectures/Papers/1971-allen-catalog.pdf"). In Rustin, Randall (ed.), Design and Optimization of Compilers. Proc. Courant Comp. Sci. Symp. 5. Prentice-Hall (Englewood Cliffs, N.J., 1972).

#### [Bobrow] *

Bobrow, Daniel G. and Wegbreit, Ben. [_A Model and Stack Implementation of Multiple Environments_](https://dl.acm.org/doi/10.1145/362375.362379 "dl.acm.org/doi/10.1145/362375.362379"). CACM 16, 10 (October 1973) pp.591-603.

#### [Church] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xchurch1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xchurch2)

Church, Alonzo. [_The Calculi of Lambda Conversion_](https://archive.org/details/AnnalsOfMathematicalStudies6ChurchAlonzoTheCalculiOfLambdaConversionPrincetonUniversityPress1941 "archive.org/details/AnnalsOfMathematicalStudies6ChurchAlonzoTheCalculiOfLambdaConversionPrincetonUniversityPress1941"). Annals of Mathematics Studies Number 6. Princeton University Press (Princeton, 1941). Reprinted by Klaus Reprint Corp.(New York, 1965).

#### [Coleman] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xcoleman)

Coleman, Samuel S. [_JANUS: A Universal Intermediate Language_](https://.invalid/_no_online_copy_found_ "No online copy found"), PhD thesis, University of Colorado, 1974.

#### [Declarative] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdeclarative1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdeclarative2), [3](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdeclarative3), [4](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdeclarative4), [5](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdeclarative5), [6](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdeclarative6), [7](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdeclarative7)

Steele, Guy Lewis Jr.[_LAMBDA: The Ultimate Declarative_](https://dspace.mit.edu/handle/1721.1/6091 "dspace.mit.edu/handle/1721.1/6091"). AI Memo 379. MIT AI Lab (Cambridge, November 1976).

 {{HTML transcription: [research.scheme.org/lambda-papers/](https://research.scheme.org/lambda-papers/ "research.scheme.org/lambda-papers/"). }}

#### [Dijkstra] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdijkstra)

Dijkstra, Edsger W. [_A Discipline of Programming_](https://archive.org/details/disciplineofprog0000dijk "archive.org/details/disciplineofprog0000dijk"). Prentice-Hall (Englewood Cliffs, N.J., 1976)

#### [Doyle] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdoyle1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xdoyle2)

Jon Doyle, Johan de Kleer, Gerald Jay Sussman, and Guy L. Steele Jr. [_Explicit Control of Reasoning_](https://dspace.mit.edu/handle/1721.1/5750). AI Memo 427. MIT AI Lab (Cambridge, June 1977).

#### [Geschke] *

Geschke, Charles M. [_Global program optimizations._](https://www.proquest.com/openview/257cdb472f7f80955f5e5be70cb1f2f6/1.pdf "www.proquest.com/openview/257cdb472f7f80955f5e5be70cb1f2f6/1.pdf"), PhD thesis, Carnegie-Mellon University, 1972.

#### [Gries] *

Gries, David [_Compiler Construction for Digital Computers_](https://archive.org/details/compilerconstruc0000grie "archive.org/details/compilerconstruc0000grie (Table of Contents only)"), John Wiley and Sons, 1971.

#### [Hewitt and Smith] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xhewitt-and-smith)

Hewitt, Carl, and Smith, Brian. [_Towards a Programming Apprentice_](https://dl.acm.org/doi/abs/10.1109/TSE.1975.6312818 "dl.acm.org/doi/abs/10.1109/TSE.1975.6312818"). IEEE Transactions on Software Engineering SE-1, 1 (March 1975), 26-45.

#### [Imperative] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#ximperative1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#ximperative2), [3](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#ximperative3)

Steele, Guy Lewis Jr., and Sussman, Gerald Jay. [_LAMBDA: The Ultimate Imperative_](https://dspace.mit.edu/handle/1721.1/5790 "dspace.mit.edu/handle/1721.1/5790"). AI Lab Memo 353. MIT (Cambridge, March 1976).

 {{HTML transcription: [research.scheme.org/lambda-papers/](https://research.scheme.org/lambda-papers/ "research.scheme.org/lambda-papers/"). }}

#### [Landin] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xlandin)

Landin, Peter J. [_A Correspondence between ALGOL 60 and Church’s Lambda-Notation_](https://dl.acm.org/doi/10.1145/363744.363749 "dl.acm.org/doi/10.1145/363744.363749"). CACM Vol. 8, No.2-3, 1965. ([February](https://dl.acm.org/doi/10.1145/363744.363749 "dl.acm.org/doi/10.1145/363744.363749") and [March](https://dl.acm.org/doi/10.1145/363791.363804 "dl.acm.org/doi/10.1145/363791.363804")).

#### [LISP1.5M] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xlisp1.5m)

McCarthy, John, et al.[_LISP 1.5 Programmer’s Manual_](https://apps.dtic.mil/sti/tr/pdf/AD0406138.pdf "apps.dtic.mil/sti/tr/pdf/AD0406138.pdf"). The MIT Press (Cambridge, 1962).

#### [Moon] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xmoon1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xmoon2)

Moon, David A. [_MACLISP Reference Manual, Revision 0_](https://www.softwarepreservation.org/projects/LISP/MIT/Moon-MACLISP_Reference_Manual-Apr_08_1974.pdf "www.softwarepreservation.org/projects/LISP/MIT/Moon-MACLISP_Reference_Manual-Apr_08_1974.pdf"). Project MAC, MIT (Cambridge, April 1974).

#### [Moses] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xmoses1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xmoses2)

Moses, Joel. [_The Function of FUNCTION in LISP_](https://dspace.mit.edu/handle/1721.1/5854 "dspace.mit.edu/handle/1721.1/5854"). AI Memo 199, MIT AI Lab (Cambridge, June 1970).

#### [Reynolds] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xreynolds)

Reynolds, John C. [_Definitional Interpreters for Higher Order Programming Languages_](https://dl.acm.org/doi/10.1145/800194.805852 "dl.acm.org/doi/10.1145/800194.805852"). ACM Conference Proceedings 1972.

#### [Sammet] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xsammet)

Sammet, Jean E. [_Programming Languages: History and Fundamentals_](https://archive.org/details/programminglangu00unse "archive.org/details/programminglangu00unse"), Prentice-Hall (Englewood Cliffs, N.J., 1969).

#### [Smith and Hewitt] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xsmith)

Smith, Brian C. and Hewitt, Carl. [_A PLASMA Primer (draft)_](https://www.scribd.com/document/185900689/A-Plasma-Primer "www.scribd.com/document/185900689/A-Plasma-Primer"). MIT AI Lab (Cambridge, October 1975).

#### [Standish] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xstandish1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xstandish2)

Standish, T. A. etal. [_The Irvine Program Transformation Catalogue_](https://escholarship.org/uc/item/79p8s9qv "escholarship.org/uc/item/79p8s9qv"), University of California TR#161, 1976.

#### [Steele] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xsteele1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xsteele2), [3](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xsteele3), [4](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xsteele4), [5](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xsteele5)

Steele, Guy Lewis Jr.[_Debunking the ‘Expensive Procedure Call’ Myth_](https://dl.acm.org/doi/abs/10.1145/800179.810196 "dl.acm.org/doi/abs/10.1145/800179.810196") submitted to the 77 ACM National Conference.

#### [Stoy] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xstoy-1974)

Stoy, Joseph [_The Scott-Strachey Approach to the Mathematical Semantics of Programming Languages_](https://.invalid/_no_online_copy_found_ "No online copy found"), MIT Laboratory for Computer Science, 1974. :::{.ti} {{See Stoy, Joseph E. [_Denotational Semantics: The Scott-Strachey Approach to Programming Language Theory_](https://archive.org/details/denotationalsema0000jose "archive.org/details/denotationalsema0000jose") MIT Press (Cambridge, 1977). }} :::

#### [SCHEME] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xscheme1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xscheme2), [3](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xscheme3), [4](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xscheme4), [5](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xscheme5)

Sussman, Gerald Jay, and Steele, Guy L. Jr. [_SCHEME: An Interpreter for Extended Lambda Calculus_](https://dspace.mit.edu/handle/1721.1/5794 "dspace.mit.edu/handle/1721.1/5794"). AI Lab Memo 349. MIT (Cambridge, December 1975).

#### [Teitelman] [^](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xteitelman)

Teitelman, Warren. [_InterLISP Reference Manual Revised edition_](https://.invalid/_no_online_copy_found_ "No online copy found"). Xerox Palo Alto Research Center (Palo Alto, 1975).

 {{see [_InterLISP Reference Manual_](https://www.bitsavers.org/pdf/xerox/interlisp/Interlisp_Reference_Manual_Oct_1974.pdf "www.bitsavers.org/pdf/xerox/interlisp/Interlisp_Reference_Manual_Oct_1974.pdf"), 1974 }}

#### [Wand] *

Wand, Mitchell and Friedman, Daniel P. [_Compiling Lambda Expressions Using Continuations_](https://legacy.cs.indiana.edu/ftp/techreports/TR55.pdf "legacy.cs.indiana.edu/ftp/techreports/TR55.pdf"), Technical Report 55, Indiana University, 1976.

#### [Wulf] [1](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xwulf1), [2](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#xwulf2)

Wulf, William A., et al.[_The Design of an Optimizing Compiler_](https://apps.dtic.mil/sti/citations/AD0773838 "apps.dtic.mil/sti/citations/AD0773838"). American Elsevier (New York, 1975).

* * *

## [Appendix](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#contents "Go to Contents")

We reproduce here Appendix A of [[Declarative](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#declarative-1-2-3-4-5-6-7 "[7] Steele 1976, LAMBDA: The Ultimate Declarative")]:

Here we present a set of functions, written in SCHEME, which convert a SCHEME expression from functional style to pure continuation-passing style.

```
(ASET' GENTEMPNUM O)

(DEFINE GENTEMP
        (LAMBDA (X)
                (IMPLODE (CONS X (EXPLODEN (ASET' GENTEMPNUM (+ GENTEMPNUM 1)))))))
```

`GENTEMP` creates a new unique symbol consisting of a given prefix and a unique number.

`(DEFINE CPS (LAMBDA (SEXPR) (SPRINTER (CPC SEXPR NIL '#CONT#))))`
`CPS` (Continuation-Passing Style) is the main function; its argument is the expression to be converted. It calls `CPC` (C-P Conversion) to do the real work, and then calls `SPRINTER` to pretty-print the result, for convenience. The symbol `#CONT#` is used to represent the implied continuation which is to receive the value of the expression.

```
(DEFINE CPC
        (LAMBDA (SEXPR ENV CONT)
                (COND ((ATOM SEXPR) (CPC-ATOM SEXPR ENV CONT))
                      ((EQ (CAR SEXPR) 'QUOTE)
                       (IF CONT "(,CONT ,SEXPR) SEXPR))
                      ((EQ (CAR SEXPR) 'LAMBDA)
                       (CPC-LAMBDA SEXPR ENV CONT))
                      ((EQ (CAR SEXPR) 'IF)
                       (CPC-IF SEXPR ENV CONT))
                      ((EQ (CAR SEXPR) 'CATCH)
                       (CPC-CATCH SEXPR ENV CONT))
                      ((EQ (CAR SEXPR) 'LABELS)
                       (CPC-LABELS SEXPR ENV CONT))
                      ((AND (ATOM (CAR SEXPR))
                            (GET (CAR SEXPR) 'AMACRO))
                       (CPC (FUNCALL (GET (CAR SEXPR) 'AMACRO)
                                     SEXPR) ENV CONT))
                      (T (CPC-FORM SEXPR ENV CONT)))))
```

`CPC` merely dispatches to one of a number of subsidiary routines based on the form of the expression `SEXPR`. `ENV` represents the environment in which `SEXPR` will be evaluated; it is a list of the variable names. When `CPS` initially calls `CPC`, `ENV` is `NIL`. `CONT` is the continuation which will receive the value of `SEXPR`. The double-quote (`"`) is like a single quote, except that within the quoted expression any subexpressions preceded by comma (`,`) are evaluated and substituted in (also, any subexpressions preceded by atsign (`@`) are substituted in a list segments). One special case handled directly by `CPC` is a quoted expression; `CPC` also expands any SCHEME macros encountered.

```
(DEFINE CPC-ATOM
        (LAMBDA (SEXPR ENV CONT)
                ((LAMBDA (AT) (IF CONT "(,CONT ,AT) AT))
                 (COND ((NUMBERP SEXPR) SEXPR)
                       ((MEMQ SEXPR ENV) SEXPR)
                       ((GET SEXPR 'CPS-NAME ))
                       (T (IMPLODE (CONS '% (EXPLODEN SEXPR))))))))
```

For convenience, `CPC-ATOM` will change the name of a global atom. Numbers and atoms in the environment are not changed; otherwise, a specified name on the property list of the given atom is used (properties defined below convert “`+`” into “`++`”, etc.); otherwise, the name is prefixed with “`%`”. Once the name has been converted, it is converted to a form which invokes the continuation on the atom. (If a null continuation is supplied, the atom itself is returned.)

```
(DEFINE CPC-LAMBDA
        (LAMBDA (SEXPR ENV CONT)
                ((LAMBDA (CN)
                         ((LAMBDA (LX) (IF CONT "(,COMT, LX) LX))
                          "(LAMBDA (@(CADR SEXPR) ,CN)
                                   ,(CPC (CADDR SEXPR)
                                         (APPEND (CADR SEXPR)
                                                 (CONS CN ENV))
                                         CN))))
                 (GENTEMP 'C))))
```

A `LAMBDA` expression must have an additional parameter, the continuation supplied to its body, added to its parameter list. `CN` holds the name of this generated parameter. A new `LAMBDA` expression is created, with `CN` added, and with its body converted in an environment containing the new variables. Then the same test for a null `CONT` is made as in `CPC-ATOM`.

```
(DEFINE CPC-IF
    (LAMBDA (SEXPR ENV CONT)
        ((LAMBDA (KN)
             "((LAMBDA (,KN)
                       ,(CPC (CADR SEXPR)
                             ENV
                             ((LAMBDA (PN)
                                  "(LAMBDA (,PN)
                                           (IF ,PN
                                               ,(CPC (CADDR SEXPR)
                                                     ENV
                                                     KN)
                                               ,(CPC (CADDDR SEXPR)
                                                     ENV
                                                     KN))))
                              (GENTEMP 'P))))
               ,CONT))
         (GENTEMP 'K))))
```

First, the continuation for an `IF` must be given a name `KN` (rather, the name held in `KN`; but for convenience, we will continue to use this ambiguity, for the form of the name is indeed `Kn` for some number `n`), for it will be referred to in two places and we wish to avoid duplicating the code. Then, the predicate is converted to continuation-passing style, using a continuation which will receive the result and call it `PN`. This continuation will then use an `IF` to decide which converted consequent to invoke. Each consequent is converted using continuation `KN`.

```
(DEFINE CPC-CATCH
        (LAMBDA (SEXPR ENV CONT)
                ((LAMBDA (EN)
                         "((LAMBDA (,EN)
                                   ((LAMBDA (,(CADR SEXPR))
                                            ,(CPC (CADDR SEXPR)
                                                  (CONS (CADR SEXPR) ENV)
                                                  EN))
                                    (LAMBDA (V C) (,EN V))))
                           ,CONT))
                 (GENTEMP 'E))))
```

This routine handles `CATCH` as defined in ~~[Sussman 75]~~ [[SCHEME](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#scheme-1-2-3-4-5 "[4] Sussman and Steele 1975, SCHEME: An Interpreter for Extended Lambda Calculus")], and in converting it to continuation-passing style eliminates all occurrences of `CATCH`. The idea is to give the continuation a name `EN`, and to bind the `CATCH` variable to a continuation `(LAMBDA (V C) ...)` which ignores its continuation and instead exits the catch by calling `EN` with its argument `V`. The body of the `CATCH` is converted using continuation `EN`.

```
(DEFINE CPC-LABELS
        (LAMBDA (SEXPR ENV CONT)
                (DO ((X (CADR SEXPR) (CDR X))
                     (Y ENV (CONS (CAAR X) Y)))
                    ((NULL X)
                     (DO ((W (CADR SEXPR) (CDR W))
                          (Z NIL (CONS (LIST (CAAR W)
                                             (CPC (CADAR W) Y NIL))
                                       Z)))
                         ((NULL W)
                          "(LABELS ,(REVERSE Z)
                                   ,(CPC (CADDR SEXPR) Y CONT))))))))
```

Here we have used `DO` loops as defined in MacLISP (`DO` is implemented as a macro in SCHEME). There are two passes, one performed by each `DO`. The first pass merely collects in `Y` the names of all the labelled `LAMBDA` expressions. The second pass converts all the `LAMBDA` expressions using a null continuation and an environment augmented by all the collected names in `Y`, collecting them in `Z`. At the end, a new `LABELS` is constructed using the results in `Z` and a converted `LABELS` body.

```
(DEFINE CPC-FORM
    (LAMBDA (SEXPR ENV CONT)
        (LABELS ((LOOP1
                    (LAMBDA (X Y Z)
                        (IF (NULL X)
                            (DO ((F (REVERSE (CONS CONT Y))
                                    (IF (NULL (CAR Z)) F
                                        (CPC (CAR Z)
                                             ENV
                                             "(LAMBDA (,(CAR Y) ,F)))))
                                 (Y Y (CDR Y))
                                 (Z Z (CDR Z)))
                                ((NULL Z) F))
                            (COND ((OR (NULL (CAR X))
                                       (ATOM (CAR X)))
                                   (LOOP1 (CDR X)
                                          (CONS (CPC (CAR X) ENV NIL) Y)
                                          (CONS NIL Z)))
                                  ((EQ (CAAR X) 'QUOTE)
                                   (LOOP1 (CDR X)
                                          (CONS (CAR X) Y)
                                          (CONS NIL Z)))
                                  ((EQ (CAAR X) 'LAMBDA)
                                   (LOOP1 (CDR X)
                                          (CONS (CPC (CAR X) ENV NIL) Y)
                                          (CONS NIL Z)))
                                  (T (LOOP1 (CDR X)
                                            (CONS (GENTEMP 'T) Y)
                                            (CONS (CAR X) Z))))))))
                (LOOP1 SEXPR NIL NIL))))
```

This, the most complicated routine, converts forms (function calls). This also operates in two passes. The first pass, using `LOOP1`, uses `X` to step down the expression, collecting data in `Y` and `Z`. At each step, if the next element of `X` can be evaluated trivially, then it is converted with a null continuation and added to `Y`, and `NIL` is added to `Z`. Otherwise, a temporary name `TN` for the result of the subexpression is created and put in `Y`, and the subexpression itself is put in `Z`. On the second pass (the `DO` loop), the final continuation-passing form is constructed in `F` from the inside out. At each step, if the element of `Z` is non-null, a new continuation must be created. (There is actually a bug in `CPC-FORM`, which has to do with variables affected by side-effects. This is easily fixed by changing `LOOP1` so that it generates temporaries for variables even though variables evaluate trivially. This would only obscure the examples presented below, however, and so this was omitted.)

```
(LABELS ((BAR
          (LAMBDA (DUMMY X Y)
                  (IF (NULL X) '|CPS ready to go!|
                      (BAR (PUTPROP (CAR X) (CAR Y) 'CPS-NAME)
                           (CDR X)
                           (CDR Y))))))
        (BAR NIL
             '(+  -  *  //   ^  T  NIL)
             '(++ -- ** //// ^^ 'T 'NIL)))
```

This loop sets up some properties so that “`+`” will translate into “`++`” instead of “`%+`”, etc.

Now let us examine some examples of the action of `CPS`. First, let us try our old friend `FACT`, the iterative factorial program.

```
(DEFINE FACT
        (LAMBDA (N)
                (LABELS ((FACT1 (LAMBDA (M A)
                                        (IF (= M 0) A
                                            (FACT1 (- M 1) (* M A))))))
                        (FACT1 N 1))))
```

Applying `CPS` to the `LAMBDA` expression for `FACT` yields:

```
(#CONT#
    (LAMBDA (N C7)
        (LABELS ((FACT1
            (LAMBDA (M A C10)
                ((LAMBDA (K11)
                    (%= M 0
                        (LAMBDA (P12)
                            (IF P12 (K11 A)
                                (-- M 1
                                    (LAMBDA (T13)
                                        (** M A
                                            (LAMBDA (T14)
                                                (FACT1 T13 T14 K11)
                                                ))))))))
                     C10))))
                 (FACT1 N 1 C7))))
```

As an example of `CATCH` elimination, here is a routine which is a paraphrase of the `SQRT` routine from ~~[Sussman 75]~~ [[SCHEME](https://research.scheme.org/lambda-papers/lambda-papers-compiler-optimization.html#scheme-1-2-3-4-5 "[5] Sussman and Steele 1975, SCHEME: An Interpreter for Extended Lambda Calculus")]:

```
(DEFINE SQRT
        (LAMBDA (X EPS)
                ((LAMBDA (ANS LOOPTAG)
                         (CATCH RETURNTAG
                                (BLOCK (ASET' LOOPTAG (CATCH M M))
                                       (IF ---
                                           (RETURNTAG ANS)
                                           NIL)
                                       (ASET' ANS ===)
                                       (LOOPTAG LOOPTAG))))
                 1.0
                 NIL)))
```

Here we have used “`---`” and “`===`” as ellipses for complicated (and relatively uninteresting) arithmetic expressions. Applying `CPS` to the `LAMBDA` expression for `SQRT` yields:

```
(#CONT#
 (LAMBDA (X EPS C33)
     ((LAMBDA (ANS LOOPTAG C34)
          ((LAMBDA (E35)
               ((LAMBDA (RETURNTAG)
                    ((LAMBDA (E52)
                         ((LAMBDA (M) (E52 M))
                          (LAMBDA (V C) (E52 V))))
                     (LAMBDA (T51)
                             (%ASET' LOOPTAG T51
                                (LAMBDA (T37)
                                  ((LAMBDA (A B C36) (B C36))
                                   T37
                                   (LAMBDA (C40)
                                       ((LAMBDA (K47)
                                          ((LAMBDA (P50)
                                               (IF P50
                                                   (RETURNTAG ANS K47)
                                                   (K47 'NIL)))
                                           %---))
                                        (LAMBDA (T42)
                                            ((LAMBDA (A B C41) (B C41))
                                             T42
                                             (LAMBDA (C43)
                                                 (%ASET' ANS %===
                                                    (LAMBDA (T45)
                                                       ((LAMBDA (A B C44)
                                                                (B C44))
                                                        T45
                                                        (LAMBDA (C46)
                                                           (LOOPTAG
                                                            LOOPTAG
                                                            C46))
                                                        C43))))
                                             C40))))
                                    E35))))))
                (LAMBDA (V C) (E35 V))))
           C34))
      1.0
      'NIL
      C33)))
```

Note that the `CATCH`es have both been eliminated. It is left as an exercise for the reader to verify that the continuation-passing version correctly reflects the semantics of the original.
