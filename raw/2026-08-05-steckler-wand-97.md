---
source: https://www.ccs.neu.edu/home/wand/papers/steckler-wand-97.ps
fetched-at: 2026-08-05
converter: ghostscript+docling
---

Lightweight Closure Conversion PAUL A/. STECKLER University of Technology/, Sydney and MITCHELL WAND

Northeastern University

We consider the problem of lightweight closure conversion/, in which multiple procedure call pro/tocols may coexist in the same code/. A lightweight closure omits bindings for some of the free variables of the procedure that it represents/. Flow analysis is used to match the protocol expected by each procedure and the protocol used at its possible call sites/. We formulate the /ow analysis as a deductive system that generates a labeled transition system and a set of constraints/. We show

Meanings of Programs/]/: Semantics of Programming Languages/|operational semantics General Terms/: Algorithms/, Languages/, Theory Additional Key Words and Phrases/: Closure conversion/, compiler construction/, global optimiza/-

that any solution to the constraints justi/es the resulting transformation/. Some of the techniques used are similar to those of abstract interpretation/, but others appear to be novel/. Categories and Subject Descriptors/: D/./3/./3 /[Programming Languages/]/: Language Constructs and Features/|procedures/, functions/, and subroutines/; D/./3/./4 /[Programming Languages/]/: Pro/cessors/|compilers/; optimization/; F/./3/./1 /[Logics and Meanings of Programs/]/: Specifying and Verifying and Reasoning about Programs/|assertions/; pre/- and postconditions/; F/./3/./2 /[Logics and

tion///ow analysis/, program transformations

/1/. OPTIMIZING CODE TRANSFORMATIONS Modern compilers perform a variety of program analyses in order to produce good code/. The goal of such analyses is to annotate a program with certain propositions about the behavior of the program/. One can then apply optimizations to the

program that are justi/ed by those propositions/.

For /rst/-order languages/, the justi/cation of such optimizations or transforma/-

This work was supported by the National Science Foundation and DARPA under grants CCR//9/0/0/2/2/5/3 and CCR/-/9/0/1/4/6/0/3/. Preliminary presentations of this work appeared in Conference Record of the /2/1st ACM Symposium on Principles of Programming Languages and in the /rst/-named

College of Computer Science/, Cullinane Hall/, Northeastern University/, Boston/, MA /0/2/1/1/5/; email/: wand/@ccs/.neu/.edu/. Permission to make digital//hard copy of all or part of this material without fee is granted provided that the copies are not made or distributed for pro/t or commercial advantage/, the ACM copyright//server notice/, the title of the publication/, and its date appear/, and notice is given that copying is by permission of the Association for Computing Machinery/, Inc/. /(ACM/)/. To copy otherwise/, to republish/, to post on servers/, or to redistribute to lists requires prior speci/c

author/'s Ph/.D/. dissertation/. Both authors were a/liated with Northeastern University when this research was conducted/. Authors/' addresses/: P/.A/. Steckler/, School of Computing Sciences/, University of Technology/, Syd/ney/, P/.O/. Box /1/2/3/, Broadway /2/0/0/7 NSW/, Australia/; email/: steck/@socs/.uts/.edu/.au/; M/. Wand/,

permission and//or a fee/.

c

/ /1/9/9/6

ACM /0/1/6/4/-/0/9/2/5///9/9///0/1/0/0/-/0/1/1/1

/$/0/0/./7/5

ACM Transactions on Programming Languages/, pp/. /1/-/1/0/0/.

/2 / P/.A/. Steckler and M/. Wand tions has been investigated for many years and is reasonably well understood/. For higher/-order languages such as Scheme/, Standard ML/, or Haskell/, however/, it has

/1/9/8/9/]/.

proven remarkably di/cult to specify the semantics of these propositions in a way that justi/es the resulting transformations/. Here we study one such transformation/, called closure conversion/. In a lexically scoped higher/-order language/, a procedure is typically represented by a record con/sisting of a piece of pure code /(a closed //-abstraction/) and the values of the free variables of the original procedure /(an environment/)/. This data structure is called a closure/. In closure conversion/, these data structures are built at the source/-language level/. During compilation/, procedure creation is replaced by closure creation/, and during execution/, procedure application is replaced by invocation of the code part of the closure on an actual parameter and the environment part of the closure/. Alternatively/, another copy of the closure can be passed instead of just the envi/ronment/. This strategy is sometimes called closure/-passing style /[Appel and Jim

to

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

application/; we do not create closures for the implicit procedures/. Here f takes an argument and emits a procedure of one argument/; in the closure/converted version/, both f and the procedure it returns are represented by records/. g takes the closure record returned by f and applies it by taking the piece of code and applying it to the record of free variables and the actual parameter/. Both f

in app g /(app f /9/) where app is a combinator/, de/ned as /r/:/(/#/1 r/)/(/#/2 r/)/, which applies the code part of a closure to its environment part/. In this and subsequent examples/, procedures are curried/; the procedure in the code part of the closure for f should be read as /e/:/x/: / / //, for example/. In examples/, we use let as syntactic sugar for procedure

and g are closed/, so their closures have empty records of free variables/. Closure conversion is a crucial step in the compilation process for higher/-order languages/. Since the code parts of closures are closed/, they may be moved to the top level of the program if desired/. Furthermore/, this conversion is a source/-to/source transformation/, so the representation of closures can be optimized using all

convertible with the result of the original program/.

ACM Transactions on Programming Languages Let us closure/-convert

the tools available to the compiler/. In the last example/, the original program and its transform both evaluate to the same result/. Closure conversion may produce a transform whose result is not

Lightweight Closure Conversion

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

in app f /4

clearly be used in this way/.

In this case/, the original program evaluates to an ordinary procedure/, while the transform evaluates to a closure record/. In many cases/, a closure need not include all the free variables of a procedure/, because some of the free variables are available at all the places where the closure might be invoked/. We call such variables dynamic/, because they behave the same as they would if the language used dynamic scope/, and we call the incomplete closures lightweight closures/. If we took this approach to an extreme/, a procedure might be able to /nd all its free variables at the call site/, so no closure need be created/, as in lambda/-lifting /[Augustsson /1/9/8/4/]/. We do not go so far/, but our techniques could

- /|First/, we believe the analysis may be turn out to be a useful one for real languages/. /|Second/, it provides an example of the formal justi/cation of a fairly complex
- These results are signi/cant in several ways/:
- analysis/-based program transformation/. /|We believe the techniques and approach we have used will be useful for other

do not seem readily expressible in that framework/.

- analyses and transformations/. /|Last/, while some of our techniques are similar to those of abstract interpretation/, we believe that others represent a new approach/. Control/-/ow analysis/, one part of our analysis/, is a typical application of abstract interpretation/; our invariance sets/, which track variable bindings that do not change across subterm evaluation/,

/2/. EXAMPLES The data/ow analysis has two signi/cant responsibilities toward the closure con/version transformation/. First/, all procedures /owing to a given call site must agree on their application protocol/. By application protocol/, we mean which variables are designated as dynamic and in what order those variables appear as arguments/. Second/, the dynamic variables at a call site must be bound to the same values as they have at the de/nition sites for the procedures that /ow to that site/. As the following examples should suggest/, it is not obvious how to perform the data/ow

analysis/.

Consider the following/:

ACM Transactions on Programming Languages

/

/3

/4

in /(if /(zero/? / / //) then f else g/) c Variable x is free in the procedure f/, and y is free in the procedure g/. At the call site on the bottom line/, x and y are in scope and can be supplied as extra

```
/ P/.A/. Steckler and M/. Wand let x /= / / / y /= / / / in let f /= /(/v/: / / / x / / //) g /= /(/z/: / / / y / / //)
```

arguments/.

in app/(if /(zero/? / / //) then f else g/) x y c Other choices are possible/, subject to the condition that f and g obey the same application protocol/. For instance/, we could have reversed the order of the dynamic variables/, or we could have left the dynamic variables in the closures/. Our data/ow

```
After closure conversion/, we might have let x /= / / / y /= / / / in let f /= /[/(/e/; x/; y/; v/: / / / x / / //)/; /[ /]/] g /= /[/(/e/; x/; y/; z/: / / / y / / //)/; /[ /]/]
```

analysis will enforce protocol agreement/. Not all variables in scope at a call site are eligible to be made dynamic/. A free variable in a procedure may be in the scope of di/erent binders where the procedure is called and where the procedure is closed/. Also/, a procedure may escape the binding of a free variable and /ow back to a call site where the variable is in scope/. Even though the variable is visible at the call site/, it may be bound to

in g c /(g c /0 /(/v/:v/)/) The result of evaluating this program is c /0 /. Variable x is in scope at f/'s call site

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

a dynamic variable/. So instead we want

ACM Transactions on Programming Languages

in app/(app g c/) /(app /(app g c /0 /) /[/(/e /0/0 /; x/; v/:v/)/; /[ /]/]/) But there are two calls to g/, both of which invoke the scope for x/. For the left/-hand call/, x is bound to c/; for the right/-hand call/, x is bound to c /0 /. During the left/-hand call to g/, y is bound to a copy of f with its free x bound to c /0 /. That is/, f has escaped from the other invocation of x/'s scope/. This incorrect transform gives c as a result/. Therefore/, the data/ow analysis needs to assure that x is not considered

```
Lightweight Closure Conversion / let g /= /[/(/e/; x/:/[/(/e /0 /; y/: let x /= /(/#/1 e /0 /) right/! in let f /= /[/(/e /0/0 /; z/: let x /= /(/#/1 e /0/0 /) in x/)/; /[x/]/] in app y f/)/; /[x/]/]/)/; /[ /]/]
```

/5

in app/(app g c/) /(app /(app g c /0 /) /[/(/e /0/0 /; v/:v/)/; /[ /]/]/) Our analysis may be seen as a kind of lifetime analysis/, which compares the life/-

```
sites around loops/: /1 let x /= c in let g /= /(/y/: / / / x / / //) in letrec f /= /(/h/:/n/:if /(zero/? n/) then /(h c /0 /) else /(f h /(pred n/)/)/)
```

times of procedures and the bindings for their free variables/. This last example demonstrates that the binding lifetime of a variable is not determined by its scope/. Data/ow patterns may be complex/. For example/, procedures may /ow to call

in f g c /0/0 The variable x is free in the procedure g/, so ordinarily x would appear in g/'s closure/. Now consider the call site /(h c /0 /)/. At that site/, h is bound to g/, and x is in scope/. Certainly x has the same binding there as at g/'s de/nition site/, since x never gets rebound/. Before that call is made/, f may be called many times/, depending on the magnitude of c /0/0 /. Therefore/, the data/ow analysis should allow us to make x a dynamic variable/. Each recursive call to f rebinds h and n/. The analysis detects that at the call site/, h is bound to g and that x has not been rebound since its

in app/(app f g/) c /0/0

```
de/nition/. So what we want is let x /= c in let g /= /[/(/e/; x/; y/: / / / x / / //)/; /[ /]/] in letrec f /= /[/(/e /0 /; h/:/[/(/e /0/0 /; n/: let h /= /(/#/1 e /0/0 /) in if /(zero/? n/) then /(app h x c /0 /) else /(app /(app f h/) /(pred n/)/)/)/; /[h/]/]/)/; /[ /]/]
```

and our analysis can give results like this/. Certain programming idioms may make lightweight closure conversion useful in

in / / / /(g a /0 /) / / / /(h a /0/0 /) / / / /1 We can de/ne a procedure in our input language that returns the least /xed point of a functional/, so we can consider the letrec construct in this example as syntactic sugar/. Plotkin /[/1/9/7/5/] gives such a procedure Z as /f/:/(/x/:f/(/y/:/(xx/)y/)/) /(/x/:f /(/y/:/(xx/)y/)/)/. This /xed/-point operator works

```
practice/. Consider the following procedure/: /t/: let f /= /(/p/:/a/: / / / t / / / p / / / a / / //) in let g /= f P h /= f P /0
```

with call/-by/-value evaluation/, which we use for our input language/.

ACM Transactions on Programming Languages

/6 / P/.A/. Steckler and M/. Wand Suppose the argument t is a tree and f a procedure that performs action a on nodes of t for which predicate p holds/. Procedures g and h are versions of f specialized to predicates P and P /0 /, respectively/. Naive closure conversion would include t in

/[ /]/] The tree t is available at the call sites for f/, g/, and h and so is omitted from their

<!-- formula-not-decoded -->

- closures/. The rest of the article is organized as follows/: /|In Section /3/, we describe the input language/, / in /. We also describe a data structure called an occurrence closure that represents / in terms/, and we give an
- labeled transition system and data associated with such states/. /|In Section /5/, we show how program annotations may be derived as the solution
- evaluator for such data structures/. /|In Section /4/, we describe the syntax and semantics of the annotations given to programs by our analysis/. Program annotations are given as the states of a
- to a deductive system generated from an input program text/.
- rules is sound/. /|In Section /8/, we describe the language produced by the closure conversion trans/-
- /|In Section /6/, we show how the deductive system annotates an example program/. /|In Section /7/, we show that any program annotation derivable from the deduction
- formation/. /|In Section /9/, we present an equational reasoning system that will be used to
- /|In Section /1/1/, we give a correctness result for the transformation/. /|In Section /1/2/, we mention related work/.
- simplify the proof of the correctness of the closure conversion transformation/.
- /|In Section /1/0/, we give the closure conversion transformation/.

/|Finally/, in Section /1/3/, we present conclusions/.

evaluator that preserves occurrence source information/.

/3/. LANGUAGES The language framework given in this section consists of a source language/, some notation for describing occurrences of terms/, a grammar for environments/, and an

/3/./1 The Source Language We present the source language on which the transformation will operate/. The

language /in is an untyped //-calculus with integer constants/, boolean constants/,

ACM Transactions on Programming Languages Lightweight Closure Conversion

<!-- formula-not-decoded -->

if M then M else M

PrimOp /:/:/= succ j pred j zero/? The metavariable c ranges over an in/nite set of integer constants/. Let Var be the set of variables in / in /. Sometimes we will use the word /\constant/" to refer to an

where

integer constant and sometimes to a boolean constant/. Though records appear in our output language for creating closures/, we have de/liberately omitted them from the input language/. Adding records would be straight/-

their concrete syntax/. We assume that application associates to the left/, as usual/; otherwise/, we will use parentheses as necessary for disambiguation/. To emphasize that /in may be considered a programming language/, we will usually refer to //-abstractions in / in as /\procedures/./" Procedures are curried/, but we will sometimes write //~ x/:M as a notational convenience for /x/1 /: /: /: /: /:/x n /:M /. Similarly/, we may write /x/; y/:M for /x/:/y/:M/. We will usually refer to the formal

forward/, but would add some tedious cases to our proofs/; so we avoid records until we really need them/. The grammar above describes the abstract structure of /in terms/, rather than

parameter of a procedure as its /\binding variable/./" We write M /= N to indicate that M and N are //-congruent /| that is/, the terms are syntactically identical/, except for possibly di/erent names for their bound

variables/.

Val /:/:/= x j c j true j false j /x/:M where the metavariable M ranges over terms in /in /. A scalar value is a boolean

Values in / in

<!-- formula-not-decoded -->

## constant or integer constant/.

problem/, we build an occurrence evaluator that preserves source information about terms/. We identify each source program occurrence by a string called an occurrence

/3/./2 Occurrences of Terms For the purpose of showing the soundness of our analysis/, an ordinary term evalu/ator that uses substitution has a signi/cant limitation/. Given a term and its value/, we wish to compare the static annotations of the term and the value/. But a substi/tuting term evaluator discards source information about terms/: given a substituted term/, we cannot always know which parse tree node produced it/. To solve this

index/.

<!-- formula-not-decoded -->

of the parse tree to the occurrence of the term/. /2 The empty string is the index

/ /= frator/; rand/; bv/; body/; test/; then/; elseg/: An occurrence index for a source program term describes the path from the root

/2 Other approaches used to specify occurrences include generating a unique label for each occur/-

ACM Transactions on Programming Languages

/

/7

/8 / P/.A/. Steckler and M/. Wand for the root of the parse tree/. For a procedure with occurrence index i/, i/:bv is the index of its binding variable/, and i/:body the index of the procedure body/. For an application i/, the operator has index i/:rator/, and the operand has index i/:rand/. For a conditional with index i/, i/:test/, i/:then/, and i/:else are the indices for the test/, then/-part/, and else/-part/, respectively/. Any occurrence of a term may have subterms/, except for an occurrence of a binding variable/. We can more precisely specify the

```
set of possible program occurrences by the regular expression
```

of /[ /[i/] /] M /0 /. We can now de/ne the data structures manipulated by the occurrence evaluator/. De/nition /3/./2/./1/. We simultaneously de/ne occurrence environments and occur/-

/(rator /+ rand /+ body /+ test /+ then /+ else/) / /(bv /+ //)/: We write /[/[i/] /] M for the subterm of M with index i/. We usually assume we are working with an occurrence in the input term M/0 /; in this case we write /[/[i/]/] instead

```
rence closures by the grammar / /:/:/= /[ /] j / /[x /7/! oc/] /(occurrence environments/)
```

where i is an occurrence index/. We may write / /[v/1 /; /: /: /: /; v n /7/! oc /1 /; /: /: /: /; oc n /] as shorthand for the occurrence envi/ronment / /[v /1 /7/! oc /1 /] / / / /[v n /7/! oc n /]/. We shall often rely on the inductively/-de/ned

oc /:/:/= /(i/; / /)

/(occurrence closures/)

structure of occurrence environments in subsequent de/nitions and proofs/.

/[ /]/(x/) is unde/ned

<!-- formula-not-decoded -->

We write Dom/(/ /) for the domain of an occurrence environment / /. In certain cases/, we will want occurrence environments to be subject to restric/-

Dom/(/ /)/; / /(x/) /= /(j/; / /0 /) implies /[/[j/] /] is a scalar value/.

tions/: De/nition /3/./2/./2/. An occurrence environment /  is a scalar environment i/ /8x /2

In particular/, the empty occurrence environment /[ /] is a scalar environment/. When evaluating an occurrence closure /(i/; / /)/, the occurrence evaluator may ma/nipulate occurrences that originate in the environment / /, besides occurrences of subterms of the source program /[/[i/]/]/. Also/, use of the primitive operators may pro/duce constants found in neither a program nor an environment/. Therefore/, we need

result of each program subexpression to a fresh binder in a let/-expression/.

ACM Transactions on Programming Languages Lightweight Closure Conversion / /9 Let us de/ne a set of indices for occurrences that originate in environments/. Let K be an in/nite set of strings/, disjoint from / / /. We assume K is a regular set over a /nite alphabet/. An occurrence environment /  is an initial environment i/ /8x /2 Dom/(/ /)/, if / /(x/) /= /(//; / /0 /) then / /2 K/, and /  /0 is an initial environment/. This de/nition is well founded/, since it makes the empty environment initial/. An occurrence index that has a pre/x / /2 K is said to be an environment occurrence/.

to describe occurrence indices for terms other than source terms/. rence /[Sestoft /1/9/9/1/]/, //-converting a program so that each binding occurrence is unique/, and using the binding variable as a token /[Palsberg and Schwartzbach /1/9/9/5/]/. In both cited works/, only oc/currences of procedures are speci/ed/. Our approach allows us to refer to occurrences of arbitrary terms/. Also/, given the index of a term/, we can derive the indices of its subterms/. Flanagan and Felleisen /[/1/9/9/5/] use A/-normal forms to encode occurrences as variable names by assigning the

occurrences/, but observe that program and environment occurrences may also refer to constants/. Now we can give an expression that describes the entire set of occurrence indices/.

We assume that subterms of values in an initial environment are assigned occurrence indices as for program subterms/. Scalar values are their own occurrence indices/. /3 That is/, for any integer constant or boolean constant c/, /[/[c/] /] /= c/. Let C be the set of all such constant occurrences/. We assume that C/, like K/, is coded as a regular set of strings over some /nite alphabet/, e/.g/./, the set f/0/; /1g/. C is disjoint from the sets of program and environment

<!-- formula-not-decoded -->

## OM /[ O/  /.

C /+ /(/(K /+ //) /(rator /+ rand /+ body /+ test /+ then /+ else/) / /(bv /+ //)/)/: For a / in term M/, OM indicates the set of occurrence indices in M/; for an occur/rence environment / /, O / is the set of occurrence indices in / /; and O M/;/ is the set

/3/./3 The Occurrence Evaluator The occurrence evaluator is an abstract machine that uses environment extension to simulate the substitutions that would be used by a call/-by/-value term evaluator/. The evaluation relation /= /) oc de/nes a relation between occurrence closures repre/senting arbitrary terms and occurrence closures representing values/. The rules for

the occurrence evaluator are given in Figure /1/.

Const/, Var/, Proc/, PrimApp/, App/, Cond to test whether an occurrence refers to a constant/, variable/, procedure/, primitive ap/plication/, application/, or conditional/. The predicate Const is true for an occurrence of a scalar value/. As for /[/[/BnZr/] /]/, we can think of these predicates as parameterized by a particular term/. However/, we will be informal in our use of such predicates/,

We use the predicates

omitting mention of the term in which an occurrence appears/.

/3/./4 Unwinding Occurrence Closures An occurrence closure represents a term/. The meaning of occurrence closures is

U/[ /[/(i/; / /)/] /] /= /[ /[i/] /]fU /[ /[/BnZr/] /] / / g /3 Here we are confounding pointers and integers in the same way for which pre/-ANSI C language hackers were once notorious/. Our goal in doing so is to make the occurrence evaluator rules

given by the map U/[/[/BnZr/] /] de/ned by

involving constants a little simpler/.

ACM Transactions on Programming Languages

/1/0

/

<!-- image -->

P/.A/. Steckler and M/. Wand

oc

Fig/. /1/. Rules for the occurrence evaluator/. where the curly braces indicate substitution/. This de/nition is well founded/, since occurrence closures have /nite depth by De/nition /3/./2/./1/; termination occurs when

/  is empty/.

For example/, suppose

Then We call U/[/[/BnZr/] /] the unwinding function/.

/(i/; / /) /= /) oc /(k/; / /0/0 /)

<!-- formula-not-decoded -->

U/[ /[/(i/; / /)/] /] /=

/[ /[i/] /]fU /[ /[/BnZr/] /] / / g

ACM Transactions on Programming Languages

```
Lightweight Closure Conversion /= xfU/[/[/BnZr/] /] / /[ /]/[x /7/! /(j/; / /0 /)/]g /= U/[ /[/(j/; / /0 /)/] /] /= /[ /[j /] /]fU /[ /[/BnZr/] /] / / /0 g /= /(/z/:zy/)fU/[ /[/BnZr/] /] / / /0 g /= /(/z/:z U/[ /[/(/ /0 /(y/)/)/] /]/) /= /(/z/:z U/[ /[/(c/; /[ /]/)/] /]/) /= /(/z/:z /[ /[c/] /]fU /[ /[/BnZr/] /] / /[ /]g/)
```

/

/1/1

/4/. ANNOTATIONS In preparation for the closure conversion transformation/, we construct for any pro/gram a particular kind of labeled transition system with some additional baggage/.

/=

/(/z/:zc/)

Recall that O is the set of all occurrence indices/, and Var is the set of all variables/.

- is a set of value states /|a set of transition labels T /= O /[ Var/,
- De/nition /4/./1/. An abstract execution consists of /|a set of states S /= S env /[ S val /, where S env is a set of environment states and S val
- /|a T/-indexed family of transition relations on S/,
- /|a map /-/: S val /! /2 Var /, called the invariance set map/, and

/|a map /	/: S val

/! Var /

/, called the protocol tag map

- /|Senv and Sval are disjoint
- such that

/|if s /1 t /BnZr /! s /2 and s/1 t /BnZr /! s /3 for some t /2 T /, then s /2 /= s /3 /. We use A as a metavariable ranging over abstract executions/. We use E /(some/times F and G/) to range over elements of Senv /, and V to range over elements of Sval /. /4 For an abstract execution A/, we may write /-A for its invariance set map

- /|if s /1 i /BnZr /! s /2 for some i /2 O/, then s /1 /2 S val and s/2 /2 S env /|if s /1 x /BnZr /! s /2 for some x /2 Var/, then s /1 /2 S env and s/2 /2 S val

and /	A for its protocol tag map/. Because transitions are deterministic/, we may think of states as functions/. For

an environment state E in an abstract execution A/, de/ne Dom/(E/) to be

<!-- formula-not-decoded -->

fx j /9V such that E x /BnZr /! V in Ag

fi j /9E such that V /BnZr /! E in Ag /4 The use of labeled transition systems to describe abstract executions is a change from Wand and Steckler /[/1/9/9/4/] and Steckler /[/1/9/9/4/]/. There we wrote E/(x/) /= V for E x /BnZr /! V and /(i/; E/) /2 / for V i /BnZr /! E/. We believe the the use of labeled transition systems gives a clearer account of

annotations that contain cycles and of the constraint generation process /(see Section /5/)/.

ACM Transactions on Programming Languages

/1/2 / P/.A/. Steckler and M/. Wand As indicated/, an abstract execution has two kinds of transitions/. The transition

labels are variables and occurrence indices/.

transition of the form

E x /BnZr /! V describes the lookup of a variable x in an environment described by E/, while a

substitution is described by E/.

Intuitively/, a transition of the form

V i /BnZr /! E describes a call from a site described by V to the procedure with occurrence index i/. More precisely/, the call is to a substitution instance of that procedure where the

For example/, the sequence of transitions

free in /[ /[i/] /]/. /, which we have not shown/, would indicate the procedures to which x might evaluate/. The /-A and /	A maps of an abstract execution A associate with each value state V in A an invariance set / V and a protocol tag / V /. An invariance set is a /nite set of variables/. These are intended to be variables whose bindings do not change across an occurrence closure evaluation/, in case the result of the evaluation is a procedure/. A protocol tag is a /nite sequence of variables/, which describes a procedure application protocol/. We may write hv/1/; /: /: /: /; v n i to indicate such a sequence of variables/. For any sequence of variables hv/1 /; /: /: /: /; v n i/, dhv /1 /; /: /: /: /; v n ie is the corresponding set/, fv /1 /; /: /: /: /; v n g/, and khv /1 /; /: /: /: /; v n ik is the length of the sequence/,

V i /BnZr /! E x /BnZr /! V /0 represents a call to the procedure /[/[i/]/]/, followed by a lookup of an occurrence of x Any transitions from V /0

n/. We will more fully describe how this data associated with value states is used later/. An abstract execution can be described independently of a program/, but we will

/BnZr/: OM/;/  /! S env /- S val Such a /BnZr may be unde/ned at constant occurrences/, but we require that /BnZr be

use abstract execution states to annotate program occurrences/: De/nition /4/./2/. Let M be a term/. Let /  be an occurrence environment/, and let A be an abstract execution/. An annotation map from /(M/; / /) to A is a partial map

otherwise total on OM/;/  /BnZr C/.

- /|E/BnZr/;i or Ei for the /rst component of /BnZr/(i/)/,
- When the context permits/, we may write
- /|V/BnZr/;i

or Vi for the second component of /BnZr/(i/)/,

- /|/ /BnZr/;i or / i for /- A /(V i /)/, or

i/ for all i in Dom/(/BnZr/)/, if V/BnZr/;i j /BnZr /! E is in A/, then E /= E /BnZr/;j /. A monovariant annotation map /BnZr associates each procedure j in its domain with one /\abstract closure/,/" given by the pair /(j/; E /BnZr/;j /)/. A monovariant annotation map

/|/ /BnZr/;i or / i for /	 A /(V i /)/. De/nition /4/./3/. Let A be an abstract execution/. Let M be a term/, and let /  be an occurrence environment/. An annotation map /BnZr from /(M/; / /) to A is monovariant

thus corresponds to Shivers/' well/-known /0CFA control/-/ow analysis/.

ACM Transactions on Programming Languages Lightweight Closure Conversion / /1/3 We next need to de/ne a notion of satisfaction to relate concrete and abstract executions/. Informally/, we say that the evaluation of a program /(i/; / /) /= /) oc /(j/; / /0 /) satis/es an annotation map /BnZr i/ whenever the input /  satis/es E /BnZr/;i /, then the output satis/es the value state V/BnZr/;i /. Moreover/, similar satisfaction relations also hold at all subcomputations/. In this way/, we may think of the pair /(E/BnZr/;i /; V /BnZr/;i /) as input and output assertions for a functional program/, analogous to Hoare/-style partial/correctness assertions for imperative programs /[Hoare /1/9/6/9/]/. Further/, if j is an occurrence of a procedure/, then we will require that the environments / and /  /0

map from occurrences to protocol tags/. We write / for such a map/. De/nition /4/./4/. We simultaneously de/ne two satisfaction relations j /= A/;/ env and

agree on all variables in / /BnZr/;i /, the invariance set associated with V /BnZr/;i /, and / /BnZr/;j must be the same as / /BnZr/;i /, the protocol tag associated with V/BnZr/;i /. We formalize these intuitions as follows/. De/ne a protocol assignment to be a

- j /= A/;/ val inductively on the depth of occurrence environments/: /(/1/) An occurrence environment /  satis/es an environment state E under an abstract

/  j /=

execution A and a protocol assignment //, written/:

- i/ for all x and V/, if E x /BnZr /! V in A/, then /(a/) x /2 Dom/(/ /) and / /(x/) j /= A/;/ val V and /(b/) if / /(x/) /= /(i/; / /0 /)/, and Proc/(i/)/, then for all y /2 / V /, y /2 Dom/(/ /) /\ Dom/(/ /0 /)/, /0

<!-- formula-not-decoded -->

env E

- and / /(y/) /= / /(y/)/. /(/2/) An occurrence closure /(i/; / /) satis/es a value state V under an abstract execution

A and a protocol assignment //, written/:

/(i/; / /)

j /=

<!-- formula-not-decoded -->

val V

/(b/) Proc/(i/)/, //(i/) /= / V /, and /9E such that V i /BnZr /! E in A and /  j /= A/;/ env E/. This de/nition is well founded because it is inductive in the structure of the occur/-

- i/ /(a/) Const/(i/) /\_ Var/(i/) or

rence environment / /; the empty occurrence environment serves as a base case/. The /rst condition for j /= A/;/ env requires pointwise satisfaction of the value states in the range of E by the values in / /. The second condition says that the variables in the invariance set associated with such a value state have bindings that are invariant

/[ /[i/] /] where the substitution satis/es E/.

ACM Transactions on Programming Languages

across environment lookups/, in case a lookup returns a procedure/. For j /= A/;/ val /, the /rst condition says that a value state is satis/ed by any value that is not a procedure/. The second condition says that for a procedure/, its protocol tag must match the protocol tag associated with the value state/; its occurrence index must appear as the label of a transition from the value state/; furthermore/, its closing environment must satisfy the environment state E reached by that transition/. This last requirement is equivalent to saying that U/[/[/(i/; / /)/]/] is a substitution instance of

/1/4

/ P/.A/. Steckler and M/. Wand

Dom/(E/) / Dom/(/ /)/, /  j /= A/;/ env E/. Lemma /4/./6/. Let A be an abstract execution/, and let E be an environment state in A/. Let /  be an occurrence environment/, and let / be a protocol assignment such that / j /= A/;/ env E/. Suppose that E /0 is an environment state in A such that for all x and V/, if E /0 x /BnZr /! V in A/, then E x /BnZr /! V in A/. Then /  j /= A/;/ E /0 /.

points in an abstract domain/; our

The following lemmas are immediate from the de/nition of j /= A/;/ env /: Lemma /4/./5/. Let A be an abstract execution/. If /  is a scalar environment/, then for any protocol assignment / and for all environment states E in A such that

env

/(i/; / /) j /= A/;/ val V might be written /(i/; / /) /2 Conc/(V/)/. However/, we derive suitable V by applying deduction rules rather than by abstract interpretation/. Such deduction rules are local constraints on the points in /BnZr/(i/) and their associated data/. We say that an annotation of a program is locally consistent i/ it satis/es all the constraints for that program/. In this section/, we de/ne these local constraints/. In Section /6 we work out an example/. Then/, in Section /7/, we show that any locally consistent annotation

/5/. LOCALLY CONSISTENT ANNOTATIONS Our notion of satisfaction corresponds to what is called /\concretization/" in the language of abstract interpretation /[Cousot and Cousot /1/9/7/7/]/. Thus we might consider occurrence closures as points in a concrete domain/, and value states as

of a program soundly describes the possible executions of that program/. More formally/, we state/: De/nition /5/./1/. Let M be a term/. Let /  be an occurrence environment/, and let A be an abstract execution/. An annotation map /BnZr from /(M/; / /) to A is locally

analogs in constraint/-based formulations of closure analysis/. Consider some of the deduction rules for protocol tags/. If the operator of an application i evaluates to a procedure with occurrence index j/, by the app/-tag/-

consistent i/ all the deduction rules in Figures /2 through /5 are satis/ed/. In Figure /2/, a double rule indicates a biimplication/. We can convey some of the intuitions behind the deduction rules/. Transitions from value states are meant to give us a closure analysis/: for a value state Vi/, Dom/(Vi/) should approximate the set of procedures to which i may evaluate/. Con/sider a term with occurrence index i/. If Proc/(i/)/, then for any / /, /(i/; / /) evaluates to itself/; so we have the proc/-self rule Vi i /BnZr /! Ei /. If App/(i/) and Vi/:rator j /BnZr /! B/, for some B/, then by the app/-rand/-bv rule/, in case V i/:rand k /BnZr /! C/, for some k and C/, also V j/:bv k /BnZr /! C/. This says that any procedure with index k that may be the result of evaluating the operand i/:rand may be an argument to any procedure j that may be the result of evaluating the operator i/:rator/. Similarly/, by the app/-body/-app rule/, if App/(i/) and V i/:rator j /BnZr /! B/, then in case V j/:body k /BnZr /! C/, also V i k /BnZr /! C/. This says that any procedure k that may be returned by the procedure j may also be the result of evaluating the application/. These particular deduction rules /nd exact

bv/-rand rule/, the protocol tag for the operand i/:rand and the binding variable j/:bv

ACM Transactions on Programming Languages Lightweight Closure Conversion / /1/5 have to agree/. This rule forces all procedures to which i/:rator might evaluate to take arguments tagged with the same protocol/. Similarly/, if the operator evaluates to a procedure j/, the app/-tag/-body/-app rule requires the protocol tag for j/:body to have the same tag as the application itself/. Thus for any procedure to which i/:rator might evaluate/, its body receives the same protocol tag as the body of any other such procedure/, and that tag is also the tag for the application/. The cond/-tag rule complicated/.

requires that the then/- and else/-parts of a conditional have the same protocol tag as the conditional itself/. For invariance sets/, the deduction rules are less obvious/. Since we have formulated the rules to deduce what variables are not in invariance sets/, these rules tell us which variables may get rebound during an evaluation/. Suppose /(i/; / /) /= /) oc /(j/; / /0 /) and that Proc/(j/) holds/. We want /i to be a set of variables whose bindings are the same in / and /  /0 /. With that in mind/, the signi/cance of most of the deduction rules for invariance sets should become clear in the proof of the Soundness Theorem /(Theorem /7/./1/)/. Here/, we describe the rules for applications/, which are the most

/(i/; / /) /= /) oc /(m/; /  /0/0/0 /) What values in /  are left invariant by this calculation/? / /0/0/0 is obtained from / in two steps/. First/, the operator is evaluated/, yielding a /  /0 agreeing with /  on the variables in / i/:rator /(by an appropriate induction hypothesis/)/. We then evaluate j/:body in an extension of /  /0 /, yielding / /0/0/0 /, which agrees with /  /0 on / j/:body /BnZr f/[ /[j/:bv /] /]g/. In order that / agrees with /  /0/0/0 on the variables in / i /, we must have that /i / / i/:rator /\ /(/ j/:body /BnZr f/[ /[j/:bv /] /]g/)/. This explains the rules app/-inv/-rator/, app/-inv/body/-app/, and app/-inv/-bv/-app/. The other conditions for the invariance sets are needed so that /  /0 /[/[ /[j/:bv /] /] /7/! /(k/; / /0/0 /)/] j /= A/;/ Ej/:body /, in support of the induction

<!-- formula-not-decoded -->

env hypothesis for the body/. The details appear in the proof of Theorem /7/./1/. The one protocol tag constraint/, app/-tag/-cons/, says that the protocol tag for the operator of an application may contain only the variables appearing in the in/variance set for the operator/. In other words/, the only candidate dynamic variables

given a term M and an occurrence environment / /. Abstract Execution/. We need to build an abstract execution/, so we construct

are those that have the same bindings in the current environment as in the closing environment for the procedure to which the operator evaluates/. We sketch how to construct a locally consistent and monovariant annotation map/,

- each of the items in De/nition /4/./1/: /(/1/) Generate a fresh token for each distinct lexical scope in M and / /. Senv consists

other than variables and primitive operators/. S val

ACM Transactions on Programming Languages

- of these tokens/. /(/2/) Generate a fresh token for each free variable in M and / /, a token for each occurrence of a binding variable and a token for each remaining occurrence/,

/1/6

/

P/.A/. Steckler and M/. Wand

V i/:else

<!-- image -->

Vi

j

/BnZr /! F

cond/-else/-cond

- Fig/. /2/. Deduction rules for transitions/. /(/3/) The set of transition labels T consists of all variables /(including binding vari/-
- rules in Figure /2/. /(/5/) The invariance set map /- is de/ned by taking the deductive closure of the rules
- ables/) in M and /  and the indices of all procedures in M and / /. /(/4/) The transition relations are computed by taking the deductive closure of the

ACM Transactions on Programming Languages Lightweight Closure Conversion cond/-inv/-else

<!-- image -->

/ i/:else

/ i

Fig/. /3/.

/ i

x /6/2

x /6/2

<!-- image -->

Deduction rules for invariance sets/.

/= / i/:then

Fig/. /4/.

/= / i/:else cond/-tag

Deduction rules for protocol tags/.

<!-- formula-not-decoded -->

x /6/2 d/ i/:rator e

Fig/. /5/.

Protocol tag constraint/.

ACM Transactions on Programming Languages

Cond/(i/) /= /)

/

/1/7

/1/8

/

P/.A/. Steckler and M/. Wand

in Figure /4 and solving the constraints generated by the rule in Figure /5/. Items /(/4/) through /(/6/) indicate the sources of transitions/, invariance sets/, and pro/tocol tags for an abstract execution A/, but a solution algorithm must heed /(and may take advantage of/) dependencies among the deduction rules/. We now brie/y

- in Figure /3/. /(/6/) The protocol tag map /	 is de/ned by taking the deductive closure of the rules

describe how a solution algorithm might proceed/. Solution Algorithm/. The building of the transition relations mentioned in item /(/4/) corresponds to a closure analysis /[Sestoft /1/9/9/1/]/. As we perform the closure analysis/, we may simultaneously apply the rules in Figure /5/, part of item /(/6/)/. Those rules

might result in removing an assertion about an invariance set/. In the last step/, constraint solution/, mentioned in item /(/6/)/, we choose a protocol tag for each equivalence class of tags/. Equivalence classes of protocol tags induce equivalence classes of occurrences/: for any two occurrences i and j/, if /[/ i /] /= /[/ j /]/, then /[i/] /= /[j/]/. The rule app/-tag/-cons shown in Figure /5 indicates what an appro/priate tag is/. For a given equivalence class of occurrences C/, we may choose any

build equivalence classes of protocol tags/; we defer solving for the actual tags/. Note/, however/, that rule proc/-inv in Figure /3 is not monotone/: it has a negation in its hypothesis/. That means that the closure analysis has to be /nished before performing the invariance analysis mentioned in item /(/5/)/. Were these analyses intermixed/, enlarging the domain of an environment state in the closure analysis

ordering on any subset of

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

MaxInv C /= f/ i/:rator j i/:rator /2 Cg If a variable does not occur free in some procedure within C/, there is no reason to

MaxInv C /\ fFV/(/[/[i/] /]/) j i /2 C /^ Proc/(i/)g In a compiler/, the choice of subset may involve performance considerations/, which

we still have an overall O/(n /3 /) time bound/.

we do not address here/. Complexity/. To determine the complexity of /nding a locally consistent annota/tion/, we may translate the rules in Figures /2 to /4 to the language of conditional constraints of Palsberg and Schwartzbach /[/1/9/9/4/, Chapter /5/]/. A constraint in their system is of the forms c /2 X/, X / Y /, or c /2 X /= /) Y / Z/. Let n be the number of occurrences in a program/. If the number of constraints is O/(n /2 /)/, then solving the constraints can be done in time O/(n /3 /)/. A program with n distinct occurrences generates O/(n /2 /) conditional constraints under a translation /(not shown here/)/. By this reduction/, our deduction rules may be solved in time O/(n /3 /)/. The only rule not translatable into a conditional constraint/, app/-tag/-cons/, requires us to take O/(n/) intersections of the complements of invariance sets of size O/(n/)/. Since each intersection can be done in time O/(n/)/, by using a bit/-vector representation of sets/,

ACM Transactions on Programming Languages Lightweight Closure Conversion / /1/9 Lemma /5/./2/. Let M be a term/. Let /  be an occurrence environment/, and let A be an abstract execution/. Let /BnZr be a locally consistent annotation from /(M/; / /) to A/. Let i be the occurrence index of a procedure in O M/;/  /. For any occurrence m of Proof/. By considering the deduction rules in Figure /2/. By var/, Em /[ /[m/] /] /BnZr /! Vm/. From the rules/, transitions from environment states propagate from subterms to terms/, so also Ei/:body /[ /[m/] /] /BnZr /! Vm/. By proc/-body/-ext/, Ei/:body /[ /[i/:bv /] /] /BnZr /! Vi/:bv /. /[ /[m/] /] /= /[ /[i/:bv /] /]/, so by the determinism of transitions in A/, Vm /= Vi/:bv /. The result for invariance sets and protocol tags follows from De//-

/[ /[i/:bv /] /] free in i/:body/, V/BnZr/;m /= V /BnZr/;i/:bv /, / /BnZr/;m /= / /BnZr/;i/:bv /, and / /BnZr/;m

/= / /BnZr/;i/:bv /.

nition /4/./1/. This lemma says that certain distinct occurrences must share value states/. Some of the rules in Figure /2 allow environment states to be shared by more than one occurrence/. For instance/, from the cond/-test/-inh rule/, the value states for a condi/tional and its test/-part have the same domains/, and they take the same transitions/; so a single value state may be used for both the conditional and the test/. Con/sidered another way/, the environment states for the conditional and the test are

<!-- formula-not-decoded -->

## extensionally equal functions/.

/(/f/:f c/) /(/x/:/y/:z /(succ x/)/) If we evaluate this term in an environment with a binding for z/, that binding is

write / to indicate the empty string/. Environment States/. As we suggested in our sketch of the solution algorithm/, we generate an environment state for each distinct scope in the program/. So we generate four environment states/, e /0 /, e f /, e x /, and e y /: e/0 for the the outermost scope/;

available at the call site f c/. We shall see that our analysis and closure conversion algorithm make z a dynamic variable at that site/. In Figure /6/, we present a table describing each occurrence in the term/. There we

ef for the scope inside the binding f/; e x for the scope inside the binding x/; and e y for the scope inside the binding y/. For each occurrence i in the program /(other than binding variables and primitive operators/)/, we de/ne Ei to be the environment state for the scope containing i/. For instance/, E / /, Erator /, and Erand are all de/ned to be e /0 /. Figure /6 indicates the

vy /.

For each occurrence i of a variable in the program/, either free or bound/, we

ACM Transactions on Programming Languages

environment states associated with occurrences/. Value States/. We /rst generate a value state for each free variable in the program and a value state for each binder/. This gives us four value states/, v z /, v f /, vx/, and

/2/0

/

P/.A/. Steckler and M/. Wand

rand/:body/:body/:rand/:rator succ

| index i                         |                                  |               |             |           |
|---------------------------------|----------------------------------|---------------|-------------|-----------|
|                                 | subterm /[ /[i/] /] term         |               | Ei          | Vi        |
|                                 | the                              | predicate App |             |           |
| occurrence / rator             | entire /f/:f c f                |               | e/0         | v/0 v/1   |
|                                 | binding                          | Proc /&#124;  | e/0 /&#124; |           |
| rator/:bv rator/:body           | f                                |               |             | v f       |
| rator/:body/:rator              |                                  | App           | e f f       | v/2       |
|                                 | c f x/)                          | Var Const     | e e f       | v         |
|                                 | c                                |               |             | f v/3 v/4 |
| rator/:body/:rand rand rand/:bv | /x/:/y/:z /(succ binding x x/) | Proc /&#124;  | e/0 /&#124; | vx        |
| rand/:body                      |                                  |               |             | v/5       |
| rand/:body/:bv                  | /y/:z /(succ binding y x/)      | Proc          | ex /&#124;  | vy        |
| rand/:body/:body                | z                                | /&#124;       |             |           |
|                                 | /(succ z x                       | App Var       | ey          |           |
| rand/:body/:body/:rator         | succ                             |               | ey ey       | v/6 vz    |
| rand/:body/:body/:rand          |                                  | PrimApp       |             | v/7       |

/|

/|

/|

Fig/. /6/. Occurrences and annotations/. de/ne Vi to be the value state v /[/[i/]/] /. So for instance/, we assign V rator/:body/:rator /= v f and Vrand/:body/:body/:rator /= vz /. We also generate a value state for each remaining occurrence in the program/, other than primitive operators/. For each such remain/ing occurrence i/, we de/ne V i to be vn /, for some integer n/. Figure /6 indicates the

rand/:body/:body/:rand/:rand ey vx

x Var

value states associated with occurrences/. Closure Analysis and Protocol Tag Equivalence Classes/. Now we can apply the rules in Figure /2 and Figure /4/. Because environment states are shared among occurrences in the same scope/, each of the /-inh rules in Figure /2/, except proc/-

- have

body/-inh/, is satis/ed automatically/. Therefore/, we do not consider those rules further/. Some rules have no premises/, so we may apply them immediately/. By var/, we

<!-- formula-not-decoded -->

/(/3/) Erand/:body/:body/:rand/:rand

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/(/6/) ex

/BnZr /! vx

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/(/8/) Vrand /BnZr /! Erand

ACM Transactions on Programming Languages

/BnZr /! Vrand/:body/:body/:rand/:rand

/(/9/) Vrand/:body

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/BnZr /!

/(/1/2/)

## v/5 /BnZr /! ex

Erand/:body

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/(/1/5/) Erand/:body/:body

/BnZr /! Vrand/:body/:bv

/(/1/8/) Eey /BnZr /! Vvy Note that /(/1/6/) is the same as /(/4/)/, and /(/1/7/) is the same as /(/6/)/.

/(/2/0/) / rator/:body /= / / /[app/-tag/-body/-app/] An occurrence i of a variable or binding variable has a value state v /[/[i/]/] /, so we will write / /[/[i/]/] for its protocol tag and / /[/[i/]/] for its invariance set/. Accordingly/, we write

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/(/2/1/) / f /= / rand Proceeding with the closure analysis/, we now consider the rules with premises/.

/(/2/5/) ef z /BnZr /! vz /[/(/2/4/)/, Erator /= e /0 /, Erator/:body /= e f /] We have applied to exhaustion those rules with transitions from environment states in their premises /(those with names ending in /-inh/)/. The remaining rules

cannot deduce such transitions/, so we will not have to examine these rules again/.

ACM Transactions on Programming Languages

Lightweight Closure Conversion

/

/2/1

/2/2

/ P/.A/. Steckler and M/. Wand

Continuing/, by app/-rand/-bv we have /(/2/6/) Vrator/:bv rand /BnZr /! Erand /[/(/7/)/, /(/8/)/]

/(/2/7/) vf /BnZr /! e/0

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/(/2/8/) Vrator/:body/:rator /BnZr /! Erand

/(/3/0/) V/ /BnZr /! Erand/:body /[/(/7/)/,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/(/2/9/)/]

/(/3/2/) v/0 /BnZr /! ex We have now applied all the deduction rules in Figure /2 to exhaustion/, completing the closure analysis/. Note that Dom/(E/ /) /= Dom/(e /0 /) /= fzg/. By Lemma /4/./5/, any

scalar environment with a binding for z will satisfy E / /.

/(/3/4/) / rand/:body

```
We can still make more deductions for protocol tags/. From /(/2/8/)/, we also have /(/3/3/) / rand/:bv /= / rator/:body/:rand /[app/-tag/-bv/-rand/]
```

<!-- formula-not-decoded -->

/= / rator/:body

/[app/-tag/-body/-app/]

/(/3/5/) / x /= / rator/:body/:rand Now we have applied the rules in Figure /4 to exhaustion/. We compute the

equivalence classes of protocol tags/:

f/ x /; / rator/:body/:rand g Invariance Sets/. The rules tell us which variables do not belong to invariance sets/.

```
f/ / /; / rator/:body /; / rand/:body g f/ f /; / rand g
```

The set of all variables in the program is ff/; v/; x/; zg /(y occurs only as a binder/)/.

ACM Transactions on Programming Languages

```
Lightweight Closure Conversion /(/3/6/) f/; v/; x /6/2 / rator /[proc/-inv/, E rator /= e /0 /, /(/2/4/)/] /(/3/7/) f/; v/; x /6/2 / rand /[proc/-inv/, E rand /= e /0 /, /(/2/4/)/]
```

we will not need to use rule proc/-inv again/.

/

/2/3

/(/3/8/) f/; v /6/2 / rand/:body /[proc/-inv/, E rand/:body /= e x /, /(/6/) or /(/1/7/)/, /(/2/2/)/] Since the domains of environment states were computed during closure analysis/,

/(/4/3/) f/; v/; x /6/2 / rand/:bv /[app/-inv/-rator/-bv/, /(/2/8/)/, /(/4/1/)/] Invariance sets only matter for the operators of applications/. From our deduc/-

```
Continuing/, we have /(/3/9/) f/; v/; x /6/2 / / /[app/-inv/-rator/, /(/3/6/)/] /(/4/0/) f/; v/; x /6/2 / rator/:bv /[app/-inv/-rator/-bv/, /(/7/)/, /(/3/6/)/] /(/4/1/) f/; v/; x /6/2 / rator/:body/:rator /[/ rator/:body/:rator /= / f /= / rator/:bv /, /(/4/0/)/] /(/4/2/) f/; v/; x /6/2 / rator/:body /[app/-inv/-rator/, /(/4/1/)/]
```

```
tions here/, we assign /(/4/4/) / rator /= fzg /[/(/3/6/)/] /(/4/5/) / rator/:body/:rator /= / f /= fzg /[/(/4/1/)/]
```

free variables of procedures/. / rator has no equality constraints/, and / rator /= fzg /(/4/4/)/. By the rule app/-tag//= hzi/. However/, z is not free in /[/[rator/]/] /=

/(/4/6/) / rand/:body/:body/:rator /= / z /= ff/; v/; x/; zg /[no constraints/] Constraint Solution/. Finally/, we assign protocol tags/. Within equivalence classes/, the protocol tag depends on the invariance sets for application operators and the

cons/, we might choose to assign / rator /f/:f c/. So instead/, we assign / rator /= h i/. Now/, / rator/:body/:rator /= fzg /(/4/5/)/, and / rator/:body/:rator /= / f /= / rator/:bv /. Also/, / rand is in the same equivalence class as / f /. Neither rator/:bv nor rand is an

to have the same protocol tag/, we assign / z /= h i/. The transformation depends on the protocol tags for application operators and procedures/. We have assigned tags to all such occurrences/, except the procedure rand/.body/. None of the tags in the equivalence class /[/ rand/:body /] is associated with an application operator/. Since we do not know that rand/.body is able to pick up its free variables at an application site/, we assign / rand/:body /= h i/. The other elements

application operator/, but /[/[rand/] /] is a procedure/. z occurs free in /[ /[r and /] /]/, so we assign / f /= hzi/. We also assign hzi to / rand /. The other application operator is rand/:body/:body/:rator /. There are no equality constraints on its protocol tag/, which is / z /. Since there are no procedures required

of the equivalence class/, / / and / rator/:body /, are also assigned the empty sequence/.

be bound to a procedure/, but x/, y/, and z cannot /(given an environment satisfying

ACM Transactions on Programming Languages

Summary of Results/. We now summarize the results of the analysis/. In Figure /7/, we show the transitions of the abstract execution/. Solid arrows indicate transitions from value states to environment states/; dotted arrows indicate transitions from environment states to value states/. Note that/, of v f /, vx/, vy /, and vz /, there is a transition only from v f /(/2/7/)/. The way to interpret this is that f may

/2/4

/

P/.A/. Steckler and M/. Wand

/c48

/c51

/c54

/c55

/c53

/c52

/c50

/c49

/c48

/c55

/c49

/c54

/c50

/c53

/c51

/c52

/d40

/d40

/c55

/c48

/c54

/c49

/c53

/c50

/c53

/c52

/c51

/d66

/d66

/d47

/d47

/c55

/c48

/c54

/c49

/c50

/c55

<!-- image -->

/c54

/c48

/c53

/c52

/c49

/c50

/c51

v/3

Fig/. /7/.

/d114

/d114

/c55

/c54

/c49

/c53

/c50

/c53

/c50

/c52

/c48

/c51

/c55

/c54

/c53

/c52

/c48

/c49

/c50

/c51

v/6

Closure analysis/.

rand/:body/:body/:rand/:rator

/c55

/c54

/c53

/c50

/c53

/c50

/c53

/c52

/c48

/c49

/c50

/c51

v/7

/c50

/c53

/c50

/c53

/c50

v/5

/c54

/c49

/c55

/c48

/c53

/c52

/c51

| index i                        |                               |         |
|--------------------------------|-------------------------------|---------|
|                                | / i                          |         |
|                                | fzg                           | / h    |
| occurrence /                  | fzg                           | i i i   |
| rator                          |                               | h       |
| rator/:bv                      | fzg                           | hzi h i |
| rator/:body rator/:body/:rator | fzg fzg x/;zg                 |         |
|                                | ff/;                          | hzi h i |
| rator/:body/:rand              |                               | hzi     |
| rand rand/:bv                  | v/; fzg                       | h i     |
| rand/:body                     | fzg fx/; zg                   |         |
| rand/:body/:bv                 | x/;zg                         | h i     |
| rand/:body/:body               | ff/; v/;                      | h i     |
|                                | ff/; v/; x/;zg ff/; v/; x/;zg | h       |
| rand/:body/:body/:rator        |                               | i h i   |
| rand/:body/:body/:rand         | ff/; v/; x/;zg                | h i     |

<!-- image -->

/|

/|

Fig/. /8/. Invariance sets and protocol tags/. E/ /)/. The lone transition from vf is labeled with rand/, so f may only be bound to the procedure with index rand/, namely/, /x/:/y/:z /(succ x/)/. The target of that

rand/:body/:body/:rand/:rand ff/; v/; x/; zg h i

transition is e /0 /, which describes the environment closing the procedure/. Figure /8 summarizes the results for invariance sets and protocol tags/. Ob/serve that for each of the three application operators/, //, rator/.body/.rator/, and

/7/. SOUNDNESS Now we show that any monovariant and locally consistent annotation of a program

rand/.body/.body/.rator/, the protocol tag contains only elements in the invariance set/.

makes the annotations valid/. The Soundness Theorem says that if the environment

ACM Transactions on Programming Languages

/c52

/c51

/d118

/d118

/c48

/c48

/c55

/c55

/c49

/c49

/c54

/c54

/c51

/c51

/c52

/c52

/d66

/d66

/d28

/d28

/d44

/d44

/d50

/d50

/d58

/d58

/c55

/c55

/c55

/c48

/c48

/c48

/c54

/c54

/c54

/c49

/c49

/c49

/c53

/c53

/c50

/c50

/c52

/c52

/c52

/c51

/c51

/c51

/d118

/d118

/d114

/d114

/d111

/d111

/d108

/d108

/c55

/c55

/c48

/c48

/c54

/c54

/c49

/c49

/c52

/c52

/c51

/c51

Lightweight Closure Conversion / /2/5 / /| the input /| satis/es E i /, the environment state for i/, and /(i/; / /) /= /) oc /(j/; / /0 /)/, then /(j/; /  /0 /) /| the output /| satis/es Vi /, the value state for i/; moreover/, similar

satisfaction relations hold for every subcomputation/. Theorem /7/./1 /(Soundness/)/. Let A be an abstract execution/. Let M be a term/, and let /  be an occurrence environment/. Let /BnZr be a monovariant and locally consis/tent annotation map from /(M/; / /) to A/, and let / be the protocol assignment de/ned by /8i/; //(i/) /= / /BnZr/;i /. Let i be an occurrence in M/, and suppose /  j /= A/;/ env E/BnZr/;i /. Suppose /(i/; / /) /= /) /(j/; / /0 /)/. Then for any subproof /(k/; /  /0/0 /) /= /) oc /(m/; / /0/0/0 /) of this derivation

<!-- formula-not-decoded -->

- oc A/;/

Proof/. Induction on the size of the derivation that /(i/; / /) /= /) oc /(j/; / /0 /)/. The base cases are all straightforward/. For each case in the induction step/, we /rst show that the consequent holds at the root of the derivation tree/. Next we show that the premise about j /= A/;/ env holds for all immediate subproofs of the root/,

/(/2 /) /(m/; / /0/0/0 /) j /= val V/BnZr/;k /, and /(/3 /) if Proc/(m/)/, then /8x /2 / /BnZr/;k /, x /2 Dom/(/  /0/0 /) /\ Dom/(/  /0/0/0 /)/, and /  /0/0 /(x/) /= / /0/0/0

/(x/)/.

so that the consequent holds at all proper subproofs/. Case PrimApp/(i/)/. For any primitive operator/, the result will be an occurrence closure where the index is a constant occurrence/, and the occurrence environment is empty/; see the evaluation rules in Figure /1/. So suppose we have the evaluation /(i/; / /) /= /) /(c/; /[ /]/)/. Since Const/(c/)/, by the de/nition of j /= A/;/ val /, /(c/; /[ /]/) j /= A/;/ Vi/. Also

quent holds at all proper subproofs/.

oc val since Const/(c/)/, the invariant holds trivially/. By the evaluation rules for primitive operators/, there is one immediate subproof/, /(i/:rand/; / /) /= /) oc /(j/; / /0 /)/, where Const/(j/)/. Since /BnZr is locally consistent/, if E i/:rand x /BnZr /! V/, then also Ei x /BnZr /! V/, by the primapp/-rand/-inh rule/. Since / j /= A/;/ env Ei /, by Lemma /4/./6/, also /  j /= A/;/ env Ei/:rand /. By the induction hypothesis at i/:rand/, the conse/-

<!-- formula-not-decoded -->

Then we can obtain the desired results as follows/:

/(i/; / /) /= /) oc /(m/; /  /0/0/0

/)

ACM Transactions on Programming Languages

- /2/6 /
- P/.A/. Steckler and M/. Wand

```
/(/1/) /  j /= A/;/ env Ei/:rator /[app/-rator/-inh/; Lemma /4/./6/] /(/2/) /  j /= A/;/ env Ei/:rand /[app/-rand/-inh/; Lemma /4/./6/] /(/3/) /(j/; / /0 /) j /= A/;/ val Vi/:rator /[IH for j /= A/;/ val at i/:rator/] /(/4/) x /2 / i/:rator /= /) x /2 Dom/(/ /) /\ Dom/(/  /0 /)/; / /(x/) /= / /0 /(x/) /[Proc/(j/)/; IH for invariance at i/:rator/] /(/5/) Vi/:rator j /BnZr /! Ej /[Proc/(j/)/; /(/3/)/; monovariance/] /(/6/) / /0 j /= A/;/ env Ej /[/(/3/)/; /(/5/)/; de/nition of j /= A/;/ env /] /(/7/) /(k/; / /0/0 /) j /= A/;/ val Vi/:rand /[IH for j /= A/;/ val at i/:rand/] /(/8/) if Proc/(k/) then V i/:rand k /BnZr /! Ek /[/(/7/)/; monovariance/] /(/9/) if Proc/(k/) then /  /0/0 j /= A/;/ env Ek /[/(/7/)/; /(/8/)/; de/nition of j /= A/;/ env /] /(/1/0/) if Proc/(k/) then x /2 / i/:rand /= /) x /2 Dom/(/ /) /\ Dom/(/  /0/0 /)/; / /(x/) /= / /0/0 /(x/) /[IH for invariance at i/:rand/] /(/1/1/) if Proc/(k/) then V j/:bv k /BnZr /! Ek /[/(/5/)/; /(/8/)/; app/-rand/-bv/)/] /(/1/2/) / i/:rand /= / j/:bv /[/(/5/)/; app/-tag/-bv/-rand/] /(/1/3/) / j/:body /= / i /[/(/5/)/; app/-tag/-body/-app/] /(/1/4/) / j/:bv / / i/:rator /[/(/5/)/; app/-inv/-rator/-bv/] /(/1/5/) / j/:bv / / i/:rand /[/(/5/)/; app/-inv/-rand/-bv/] /(/1/6/) /[ /[j/:bv /] /] /6/2 / j/:bv /[/(/5/)/; app/-inv/-bv/] /(/1/7/) / i / / j/:body /[/(/5/)/; app/-inv/-body/-app/] /(/1/8/) / i / / i/:rator /[app/-inv/-rator/] /(/1/9/) /[ /[j/:bv /] /] /6/2 / i /[/(/5/)/; app/-inv/-bv/-app/] /(/2/0/) if Proc/(k/) then x /2 /(/ i/:rator /\ / i/:rand /) /= /) x /2 Dom/(/  /0 /) /\ Dom/(/  /0/0 /)/; / /0 /(x/) /= / /0/0 /(x/) /[/(/4/)/; /(/1/0/)/] /(/2/1/) if Proc/(k/) then x /2 / j/:bv /= /) x /2 Dom/(/  /0 /) /\ Dom/(/  /0/0 /)/; / /0 /(x/) /= / /0/0 /(x/) /[/(/1/4/)/; /(/1/5/)/; /(/2/0/)/]
```

ACM Transactions on Programming Languages

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/(/8/)/;

<!-- formula-not-decoded -->

## /[ /[j/:bv /] /]

/(/9/)/;

/(/1/1/)/;

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/(/1/2/)/]

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/(/2/5/)/]

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

env /]

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/[/(/1/7/)/; /(/1/8/)/; /(/1/9/)/; /(/3/4/)/] The preceding steps establish the theorem consequent at the root of the derivation tree/. We also want to establish the consequent at all subproofs of the derivation tree/. There are three immediate subproofs of the root of the proof tree/. By step /(/1/)/, we have /  j /= A/;/ env Ei/:rator /, and by step /(/2/)/, we have /  j /= A/;/ env Ei/:rand /. Therefore/, the conse/quent holds at all subproofs of the evaluations of the operator and the operand/. The

other immediate subproof evaluates the body of the procedure that is the result of

ACM Transactions on Programming Languages

/2/7

/2/8 / P/.A/. Steckler and M/. Wand evaluating the operator/. Similarly/, by step /(/2/6/)/, / /0 /[/[ /[j/:bv /] /] /7/! /(k/; / /0/0 /)/] j /= A/;/ env Ej/:body /,

show only the case where the test is true/.

so the consequent holds at all subproofs of the evaluation of the procedure body/. Case Cond/(i/)/. There are two subcases/, depending on the result of the test/. We

/(i/; / /) /= /) oc /(k/; / /0/0 /) By the cond/-then/-inh rule/, if E i/:then x /BnZr /! V/, for some V/, then Ei x /BnZr /! V/. By assumption/, /  j /= A/;/ env Ei /, so by Lemma /4/./6/, also / j /= A/;/ env Ei/:then /. By the induction

<!-- formula-not-decoded -->

hypothesis at i/:then we have

/(k/; / /0/0 /) j /= A/;/ val Vi Also by the induction hypothesis/, if Proc/(k/)/, then /8x /2 / i/:then /; x /2 Dom/(/ /) /\ Dom/(/  /0/0 /) and / /(x/) /= / /0/0 /(x/)/. By the rule cond/-inv/-then/, / i / / i/:then /; hence if

/(k/; / /0/0 /) j /= A/;/ val Vi/:then By the rule cond/-tag/, / i /= / i/:then /, and by rule cond/-then/-inh/, if V i/:then m /BnZr /! B/, then Vi m /BnZr /! B/. By the de/nition of j /= A/;/ val /, we also have

Proc/(k/)/, then /8x /2 / i /; x /2 Dom/(/ /) /\ Dom/(/ /0/0 /)/, and / /(x/) /= / /0/0 /(x/)/. There are two immediate subproofs/, one for the evaluation of the test/, the other for the evaluation of the then/-part/. We already showed / j /= A/;/ env Ei/:then /, so the consequent holds at all subproofs of the evaluation of the then/-part/. Since /BnZr is locally consistent/, by the rule cond/-test/-inh/, if E i/:test x /BnZr /! V/, then E i x /BnZr /! V/; so by Lemma /4/./6/, /  j /= A/;/ env Ei/:test /. Therefore/, the consequent holds at all subproofs of the

## sets in the proc/-inv rule in Figure /3/.

evaluation of the test/. Note that for each use of the Figure /2 /-inh rules in the proof/, we relied only on the /\upward/" direction/. Including the /\downward/" direction in those rules has the e/ect of expanding the domains of environment states/. We want the domains of environment states to be as large as possible/, because that allows larger invariance

/8/. AN OUTPUT LANGUAGE So far/, we have shown how to annotate programs and proved that our annota/-

<!-- formula-not-decoded -->

tions are sound/. Now we are ready to consider the transformation enabled by the annotations/. The closure conversion transformation produces terms in an output language that

if M then M else M j /[M/; /: /: /: /; M/] j /#n M where PrimOp is de/ned as in Section /3 and where n is a positive integer/. The

productions for records and /eld selection

ACM Transactions on Programming Languages are new/;

otherwise/, the grammar is Fig/. /9/. Rules for evaluating / clos terms/. identical to that for / in /. We rede/ne a value to be any constant/, boolean value/, Val /:/:/= x j c j true j false j /x/:M j /[V /1 /; /: /: /: /; Vn/]

<!-- image -->

<!-- formula-not-decoded -->

where the V /'s themselves range over values/. Note that by this de/nition/, the empty record is a value/. In Figure /9/, we give the rules for evaluating terms in / clos /. Note that any value

/9/. AN EQUATIONAL REASONING SYSTEM Here we describe a system for reasoning equationally about terms in /clos /. Our

## self/-evaluates/.

motivation is to simplify the proof of the Correctness Theorem /(Theorem /1/1/./2/)/. Let /= w be the smallest binary relation on terms in / clos closed under the rules

<!-- formula-not-decoded -->

Theorem /9/./1 /(Coevaluation/)/.

//-convertible/, they are not /= w /.

If M /=w N then M /=/)

t

V i/ N

/= /)

t

V /.

ACM Transactions on Programming Languages

Proof/. Induction on the de/nition of /= w /. The converse of Theorem /9/./1 is false/. Consider the terms /
 /= /(/x/:xx/)/(/x/:xx/) and /
 /0 /= /(/x/:xxx/)/(/x/:xxx/)/(/x/:xxx/)/. Neither term reduces to a value/. An easy induction on the rules for /= w shows that for any pair of /clos terms M and N/, if M /=w N/, then M /=/ N /(treating if /BnZr then /BnZr else /BnZr/, record constructors /[/BnZr/; /: /: /: /; /BnZr/]/, and record selection operators as constants/)/. Since /
 and /
 /0 are not

/3/0

/

P/.A/. Steckler and M/. Wand

<!-- image -->

Fig/. /1/0/.

Closure conditions for /=w/.

<!-- image -->

Fig/. /1/1/.

The closure conversion transformation/.

ACM Transactions on Programming Languages Lightweight Closure Conversion

/

/3/1

examples/. Suppose we have an annotation map /BnZr from a term M and an environment to an abstract execution/. The transformation / /BnZr is a map from O M /, the set of occurrence

/1/0/. THE CLOSURE CONVERSION TRANSFORMATION Once we have annotated a program according to the deduction rules/, we can trans/form it according to the algorithm in Figure /1/1/. In the case for Proc/(i/)/, the applica/tion of /(//~ u/://(i/:body/)/) is a desugaring of the let/'s that appeared in our introductory

indices in M/, to / clos /, the language of output terms/. The formalism is

and in what order/.

/ /BnZr /: OM /! /clos Usually the annotation map /BnZr will be understood from context/, so we will write simply //, as in Figure /1/1/. For a procedure occurrence/, the algorithm uses its associ/ated protocol tag to determine which variables are included in the resulting closure/. For an application occurrence/, the protocol tag associated with the operator is used to determine which dynamic variables/, if any/, should be inserted as extra arguments

We extend the transformation to occurrence closures by giving a map

de/ned as

/^

//: O M /- O/

/! / clos

/^ //(i/; / /) /= //(i/)f /^ / / / g

Since occurrence environments are of /nite depth/, /^ / is well founded/. We now apply the transformation to the annotated term from Section /6/. We

/[/(/e /0 /; z/; x/:/[/(/e /0/0 /; y/:/(/x/; z/: app z /(succ x/)/) /(/#/1 e /0/0 /) /(/#/2 e /0/0

have

<!-- formula-not-decoded -->

As expected/, z is inserted as a dynamic variable at the call site f

/)/)/; /[x/; z/]/]/)/; /[ /]/]

/1/1/. CORRECTNESS How do we know that the closure conversion transformation produces correct code/?

c/.

In words/: when we evaluate a closure/-converted program/, the result is the transform of the original answer/. The Correctness Theorem states this property formally/. Before we can prove that

is a value in / clos /.

result/, we need the following/: Lemma /1/1/./1/. For an occurrence environment / /, if x /2 Dom/(/ /)/, then /^ //(/ /(x/)/)

Proof/. The proof follows by induction on the depth of occurrence environments/. Let / /(x/) /= /(j/; / /0 /)/. The only di/cult case is for procedures/. Suppose Proc/(j/)/. We have /^ //(j/; / /0 /) /= //(j/)f /^ / / / /0 g/. Suppose /j /= hv /1 /; /: /: /: /; v n i/.

where e is fresh/, d/~

ue /= FV /(/[ /[j/] /]/) /BnZr fv /1 /; /: /: /: /; v n g/, and m /= k/~

uk/.

<!-- formula-not-decoded -->

ACM Transactions on Programming Languages

/3/2 / P/.A/. Steckler and M/. Wand Applying the substitution to the record means applying it to each record /eld/. The /rst /eld is a procedure/, so we get a substitution instance of the procedure/, which is a value/. Applying the substitution to the second /eld/, we get either an empty record/, which is a value/, or by the induction hypothesis/, a record of values/,

Now we can show the Correctness Theorem/. Theorem /1/1/./2 /(Correctness/)/. Let A be an abstract execution/. Let M be a term/, and let / be an occurrence environment/. Let /BnZr be a monovariant and locally consistent annotation map from /(M/; / /) to A/, and let / be the protocol assignment de/ned by /8i/; //(i/) /= / /BnZr/;i /. Let i be an occurrence index in M/, and A/;/

which is also a value/. Hence/, the entire record is a value/.

suppose /  j /=

then

/(i/; / /)

/(j/; /

<!-- formula-not-decoded -->

/)

/^ //(i/; / /) /= /) t /^ //(j/; / /0 /)

/d15

/d15

/d15

/d15

/^ //(i/; / /) t /^ //(j/; / /0 /) Proof/. Follows by induction on the size of the derivation that /(i/; / /) /= /) oc /(j/; / /0 /)/. The only di/cult case is for applications/. Suppose App/(i/)/, and we have the deriva/-

/= /) oc

<!-- formula-not-decoded -->

tion

/(i/; / /) /= /) oc /(m/; /  /0/0/0 /) We want to show that /^ //(i/; / /) /= /) t /^ //(m/; / /0/0/0 /)/. We use our equational reasoning system to /nd a term that coevaluates with the transform/, and we show that the

/d43

/d51

/d43

/d51

<!-- formula-not-decoded -->

term evaluates to /^ //(m/; / /0/0/0 /)/.

/= app /^ //(i/:rator /; / /) /^ //(/ /(v /1 /)/) / / / /^ //(/ /(v n /)/) /^ //(i/:rand/; / /) We sketch what the proof tree for the evaluation of /^ //(i/; / /) should look like in Figure /1/2/. Since we have not yet shown that the evaluation is valid/, a question

<!-- formula-not-decoded -->

ACM Transactions on Programming Languages In order to use the application rule/,

env E/BnZr/;i /.

If

/^

<!-- image -->

/^

//(m/; /

/0/0/0

/)

/0/0/0

Fig/. /1/2/. Evaluating an application/. app /^ /^ /^

//(m/; /

/)

//(i/:rator /; / /) //(/ /(v /1 /)/) / / / //(/ /(v n /)/) should evaluate to some procedure/, which we have written as /x/:M in the proof tree/. Rather than work our way through the steps in this proof tree/, we will reason /^

and /^

equationally/, using the /= w relation/. Also/, instead of reasoning with //(i/; / /) itself/, we present a term that coevaluates with /^ //(i/; / /)/, and we work with that term/. Consider the proof tree in Figure /1/2/. By an easy induction on the de/nition of /= /) t /, only values may appear on the right of /= /) t /, so /^ //(j/; / /0 /) and /^ //(k/; / /0/0 /) must be values that self/-evaluate/. Therefore/, we can replace /^ //(i/:rator /; / /) by /^ //(j/; / /0 /)/,

app /^ //(j/; / /0 /) /^ //(/ /(v /1 /)/) / / / /^ //(/ /(v n /)/) /^ //(k/; / /0/0 /) /= /) t /^ //(m/; / /0/0/0 /) We can now use equational reasoning to simplify the term to evaluate/. By the

ACM Transactions on Programming Languages

<!-- formula-not-decoded -->

//-rule for /= w /, we have

<!-- formula-not-decoded -->

Lightweight Closure Conversion

/

/3/3

/3/4 / P/.A/. Steckler and M/. Wand From the occurrence closure derivation/, we know that Proc/(j/)/, so //(j/) is a closure

/= /(/v /1 /; / / / /; v n /; /[ /[j/:bv /] /]/:/(//~ u/://(j/:body /)/) /(/#/1 /[/~ u/]/) / / / /(/#p /[/~ u/]/)/)f /^ where e is fresh/, d/~ ue /= FV /(/[ /[j/] /]/) /BnZr fv /1 /; /: /: /: /; v n g/, and p /= k/~ uk/.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/= w /(/v /1 /; / / / /; v n /; /[ /[j/:bv /] /]/:/(//~ u/://(j/:body /)/) /(/#/1 /[/~ u/]/) / / / /(/#p /[/~ u/]/)/)f /^ / / / /0 g Let N be the term //[/[j/:bv /]/]/:/(//~ u/://(j/:body /)/) /(/#/1 /[/~ u/]/) / / / /(/#p /[/~ u/]/)/. By the trans

/(/v /1 /; / / / /; v n /:N /)f /^ / / / /0 g /^ //(/ /(v /1 /)/) / / / /^ //(/ /(v n /)/) /^ //(k/; / /0/0 /) By Lemma /1/1/./1/, each term in /^ //(/ /(v /1 /)/) / / / /^ //(/ /(v n /)/) is a value/, and we can

/= Nf /^ / / / /0 g The /rst step is an explicit //-conversion where v /0 /1 is fresh/. Each /=w step represents a use of the //-rule plus some number of uses of the cong rule/. Each /= representing

<!-- formula-not-decoded -->

syntactic equality can be replaced by /= w /, so by repeated application of the trans rule/, the /rst term is weakly equivalent to the last/. In the last two steps lies the key to lightweight closure conversion/; here is where we use our invariance sets/. Since /(i/:rator/; / /) /= /) oc /(j/; / /0 /) and Proc/(j/)/, by Theorem /7/./1/, /8x /2 / i/:rator /, x /2 Dom/(/ /) /\ Dom/(/  /0 /)/, and / /(x/) /= / /0 /(x/)/. By the app/-tag/-cons rule/, since / i/:rator /= hv /1 /; /: /: /: /; v n i/, then fv/1 /; /: /: /: /; v n g / / i/:rator /. So in the next/-to/-last

ACM Transactions on Programming Languages

step/, in the extended /  /0 /, we can replace / /(v /1 /)/; /: /: /: /; / /(v n /) by /  /0 /(v /1 /)/; /: /: /: /; / /0 /(v n /)/.

Another //-conversion allows the substitution to be moved inside the body of the

procedure/:

/= /(/x /0 /:/(/(//~ u/://(j/:body /)/)/[x /0 /=/[ /[j/:bv /] /]/] /(/#/1 /[/~ u/]/) / / / /(/#p /[/~ u/]/)/)f /^ / / / /0 g/) Since d/~ ue / FV /(/[/[j/] /]/)/, we know /[/[j/:bv /] /] is not in /~ u/. Therefore/, the substitution of

/)

Lightweight Closure Conversion

```
/= Nf /^ / / / /0 g /= /(//[ /[j/:bv /] /]/:/(//~ u/://(j/:body/)/) /(/#/1 /[/~ u/]/) / / / /(/#p /[/~ u/]/)/)f /^ / / / /0 g /= /(/x /0 /:/(/(//~ u/://(j/:body /)/) /(/#/1 /[/~ u/]/) / / / /(/#p /[/~ u/]/)/)/[x /0 /=/[ /[j/:bv /] /]/]/)f /^ / / / /0 g /= /(/x /0 /:/(//~ u/://(j/:body /)/)/[x /0 /=/[ /[j/:bv /] /]/] /(/#/1 /[/~ u/]/) / / / /(/#p /[/~ u/]/)/)f /^ / / / /0 g
```

fresh variable x /0

<!-- formula-not-decoded -->

for /[ /[j/:bv /] /] possibly a/ects only the inner procedure/. By cong and repeated application of trans/, we have app /^ //(j/; / /0 /) /^ //(/ /(v /1 /)/) / / / /^ //(/ /(v n /)/) /^ //(k/; / /0/0 /) /= w /(/x /0 /:/(/(//~ u/://(j/:body /)/)/[x /0 /=/[ /[j/:bv /] /]/] /(/#/1 /[/~ u/]/) / / / /(/#p /[/~ u/]/)/)f /^ / / / /0 g/) /^ //(k/; / /0/0

/= w /(//~ u /0 /://(j/:body /)/[/~ u /0 /=/~ u/]f /^ / / / /0 /[/[ /[j/:bv /] /] /7/! /(k/; / /0/0 /)/]g/) /^ //(/ /0 /(u /1 /)/) / / / /^ //(/ /0 /(u m /)/) u /0

<!-- formula-not-decoded -->

Each variable in /~ is fresh/. The last step follows by repeated application of the select rule/, also using the cong and trans rules/. By Lemma /1/1/./1/, each of /^ //(/ /0 /(u /1 /)/) / / / /^ //(/ /0 /(u m /)/) is a value/. So by repeated

/= //(j/:body/)f /^ / / / /0 /[/[ /[j/:bv /] /]

/7/! /(k/; /

/^ //(j/:body/; / /0

But this last term is the same as

<!-- formula-not-decoded -->

/)/]g

/[/[ /[j/:bv /] /]

/7/! /(k/; /

<!-- formula-not-decoded -->

/

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/)/]/)

j /= env Ej/:body

ACM Transactions on Programming Languages

By Theorem /7/./1/,

/

/3/5

/3/6 / P/.A/. Steckler and M/. Wand

Hence

<!-- formula-not-decoded -->

/)

/^ //(i/; / /) /= /) t /^ //(m/; / /0/0/0 /) Corollary /1/1/./3/. Let A be an abstract execution/. Let M be a term/, and let / be an occurrence environment/. Let /BnZr be a monovariant and locally consistent annotation map from /(M/; / /) to A/, and let / be the protocol assignment de/ned by /8i/; //(i/) /= / /BnZr/;i /. Let i be an occurrence index/, and let / be an occurrence A/;/

environment such that /  j /=

env

<!-- formula-not-decoded -->

and j is the occurrence index of a constant c/, then

/(i/; / /) /= /) oc /(j/; / /0 /)

/= /)

/^ //(i/; / /)

t

c

/[/1/9/6/9/] to assert that a program meets a speci/cation/. Like Hoare/, we do not assume termination of annotated programs/; our states are partial correctness assertions/. Kildall /[/1/9/7/3/] described the iterative solution of data/ow equations for a compiler/.

/1/2/. RELATED WORK The use of input/-output assertions to verify programs began with Floyd /[/1/9/6/7/]/. Like Floyd/'s/, our notion of soundness uses input and output assertions /(our environment states and value states/) that are valid for all subcomputations/. Our environment and value states also correspond to the pre/- and postconditions used by Hoare

Aho et al/. /[/1/9/8/6/, Chapter /1/0/, section /1/0/./1/1/] suggest a general framework for solving data/ow equations for programs with basic blocks/. Many researchers have now considered how to perform closure analysis/, a phrase coined by Sestoft/. A closure analysis computes a set of procedures to which an ex/pression may evaluate/. In our analysis/, the transitions from a value state associated with an occurrence represent the set of procedures to which that occurrence may evaluate/. Sestoft /[/1/9/8/8/] originally used a closure analysis to prove the correctness of a transformation that replaces parameter passing by assignment to global vari/ables/. Bondorf /[/1/9/9/1/] adapted Sestoft/'s analysis for a subset of Scheme/. Shivers/' dissertation presented two analyses called /0CFA and /1CFA for a version of Scheme/, using an abstract interpretation /[Shivers /1/9/9/1/]/. /0CFA is directly comparable to our analysis/; /1CFA is a /ner analysis that indexes abstract closures by their call sites/. Ayers /[/1/9/9/3/] used similar techniques to compute a highly optimized version of /0CFA/. Palsberg and Schwartzbach /[/1/9/9/5/] use a constraint/-based closure analysis similar to ours to support safety analysis/. Stefanescu and Zhou /[/1/9/9/4/] have formu/lated a generalized closure analysis framework using abstract interpretation that can handle both mono/- and polyvariance/. Sabry and Felleisen /[/1/9/9/4/] compare the results of closure analysis for programs written in direct style with the results from

analyzing their continuation/-passing/-style transforms/.

ACM Transactions on Programming Languages

t

Lightweight Closure Conversion / /3/7 Flanagan and Felleisen /[/1/9/9/5/] have formulated closure analysis using A/-normal forms/; this technique may o/er a way to avoid some of the complexity associated with our occurrence closures/. Their closure analysis supported a /\soft/-typing/" transformation/, in which some operations that check the types of their arguments

solution to a set of constraints yields a correct transformation/, in the context of partial evaluation/. The idea of approximating an occurrence closure by an abstract closure comes from Jones /[/1/9/8/1/]/; this is the extension of the idea of record types used in Jones

at run time are replaced by nonchecking equivalents/. Heintze /[/1/9/9/2/] analyzed programs using constraints on sets of program values in his dissertation for logic/, imperative/, and functional languages/. His focus was on the algorithmics of solving constraints/, rather than using solutions to justify program transformations/. Wand /[/1/9/9/3/] introduced the idea of showing that any

and Muchnick /[/1/9/8/2/] to an occurrence closure evaluator/. Wand /[/1/9/9/2/] gave an alternative proof of correctness for a closure conversion algorithm by semantic methods/. There/, the correctness proof was that/, under

namide et al/. /[/1/9/9/6/] describe a closure conversion algorithm for ML programs that produces well/-typed terms in which closures have existential type/. We have used techniques related to those described in this article for other anal/yses/. The /\Ultra/-//" transformation in Steckler /[/1/9/9/4/, Chapter /5/] eliminates redun/dant binding of procedure parameters/; the /\selective thunki/cation/" transformation in Steckler /[/1/9/9/4/, Chapter /6/] and Steckler and Wand /[/1/9/9/4a/] prevents thunking of procedure arguments that are certain to be evaluated under call/-by/-name/; and the analysis in Steckler /[/1/9/9/6/] detects local channels in a concurrent/, distributed lan/-

certain restrictions/, if the closure/-converted term produced a constant/, then the original term produced the same constant/. Landin was the /rst to describe the use of closures to represent higher/-order functions /[Landin /1/9/6/4/]/. Many compiler writers have described their closure con/version algorithms/; see Steele /[/1/9/7/8/]/, Kranz /[/1/9/8/8/]/, and Appel /[/1/9/9/2/]/. Fradet and Le M/ etayer /[/1/9/9/1/] describe how closure creation may be avoided in some cases/. Shao and Appel /[/1/9/9/4/] use linked closures and allocation of closures in registers to reduce heap usage and memory tra/c in the SML//NJ compiler/. Starting from the work described here/, Hannan /[/1/9/9/5/] has shown how to annotate programs for lightweight closure conversion using a type system described in the ELF theorem prover/. Mi/-

## guage/.

wide applicability/.

/1/3/. CONCLUSIONS We have presented a method for proving the correctness of an optimized closure conversion transformation/. Our analysis relies on applying deduction rules to pro/vide program annotations/. Some components of our annotations/, e/.g/./, the closure analysis given by the transitions of an abstract execution/, might be made the sub/ject of an abstract interpretation/. Other components/, e/.g/./, our invariance sets/, do not seem easily expressible in that framework/. These other portions/, which do not represent individual program states/, but relate program states/, seem to fall into F/. Nielson/'s category of /\second/-order/" analyses /[Nielson /1/9/8/5/]/. Because we have used similar techniques in a number of other analyses/, we think the methods here are of

ACM Transactions on Programming Languages

## /3/8 /

P/.A/. Steckler and M/. Wand

for T E X /(see http/:////www/.brics/.dk///~krisrose//Xy/-pic/.html/)/.

ACKNOWLEDGMENTS Thanks to Richard Kelsey for discussing escape analysis and its possible applica/tions/. Robert Muller and Jens Palsberg made useful comments on earlier versions of this work/. The anonymous reviewers made helpful/, detailed comments/. Some of the diagrams were typeset using Kristo/er Rose and Ross Moore/'s X Y /-pic macros

- REFERENCES
- Appel/, A/. W/. /1/9/9/2/. Compiling with Continuations/. Cambridge University Press/, Cambridge/, England/. Appel/, A/. W/. and Jim/, T/. /1/9/8/9/. Continuation/-passing/, closure/-passing style/. In Conference
- Aho/, A/. V/./, Sethi/, R/./, and Ullman/, J/. D/. /1/9/8/6/. Compilers/: Principles/, Techniques/, and Tools/. Addison/-Wesley/, Reading/, Mass/.
- Record of the /1/6th ACM Symposium on Principles of Programming Languages/. ACM/, New York/, /2/9/3/{/3/0/2/.
- Ayers/, A/. E/. /1/9/9/3/. Abstract analysis and optimization of Scheme/. Ph/.D/. thesis/, MIT/, Cambridge/, Mass/.
- Augustsson/, L/. /1/9/8/4/. A compiler for lazy ML/. In Proceedings of the /1/9/8/4 ACM Symposium on Lisp and Functional Programming/. ACM/, New York/, /2/1/8/{/2/2/7/.
- Bondorf/, A/. /1/9/9/1/. Automatic autoprojection of higher/-order recursive equations/. Sci/. Comput/. Program/. /1/7/, /1/-/3 /(Dec/./)/, /3/{/3/4/. Cousot/, P/. and Cousot/, R/. /1/9/7/7/. Abstract interpretation/: A uni/ed lattice model for static
- typing/. Tech/. Rep/. COMP TR/9/5/-/2/5/3/, Dept/. of Computer Science/, Rice Univ/./, Houston/, Tex/. Oct/.
- analysis of programs by construction of approximation of /xpoints/. In Conference Record of the /4th ACM Symposium on Principles of Programming Languages/. ACM/, New York/, /2/3/8/{/2/5/2/. Flanagan/, C/. and Felleisen/, M/. /1/9/9/5/. Set/-based analysis for full scheme and its use in soft/-
- Floyd/, R/. W/. /1/9/6/7/. Assigning meanings to programs/. In Proceedings of the Symposium on Applied Mathematics/. American Mathematical Society/, Providence/, R/.I/.
- Workshop on Types for Program Analysis/. Computer Science Dept/./, Aarhus Univ/./, Denmark/, /4/8/{/6/2/. Available as DAIMI PB/-/4/9/3/.
- Fradet/, P/. and Le M/ etayer/, D/. /1/9/9/1/. Compilation of functional languages by program trans/formation/. ACM Trans/. Program/. Lang/. Syst/. /1/3/, /1 /(Jan/./)/, /2/1/{/5/1/. Hannan/, J/. /1/9/9/5/. Type systems for closure conversion/. In Participants/' Proceedings of the
- Heintze/, N/. /1/9/9/2/. Set based program analysis/. Ph/.D/. thesis/, Carnegie/-Mellon Univ/./, Pittsburgh/, Pa/.
- national Colloquium on Automata/, Languages/, and Programming/. Lecture Notes in Computer Science/, vol/. /1/1/5/. Springer/-Verlag/, Berlin/, /1/1/4/{/1/2/8/. Jones/, N/. D/. and Muchnick/, S/. S/. /1/9/8/2/. A /exible approach to interprocedural data /ow analysis
- Hoare/, C/. A/. R/. /1/9/6/9/. An axiomatic basis for computer programming/. Commun/. ACM /1/2/, /5/7/6/{/5/8/0/, /5/8/3/. Jones/, N/. D/. /1/9/8/1/. Flow analysis of lambda expressions /(preliminary version/)/. In The /8th Inter/-
- and programs with recursive data structures/. In Conference Record of the /9th ACM Symposium on Principles of Programming Languages/. ACM/, New York/, /6/6/{/7/4/.
- Haven/, Conn/. Landin/, P/. J/. /1/9/6/4/. The mechanical evaluation of expressions/. Comput/. J/. /6/, /4/, /3/0/8/{/3/2/0/. Minamide/, Y/./, Morrisett/, G/./, and Harper/, R/. /1/9/9/6/. Typed closure conversion/. In Conference Record of the /2/3rd ACM Symposium on Principles of Programming Languages/. ACM/, New
- Kildall/, G/. /1/9/7/3/. A uni/ed approach to global program optimization/. In Conference Record of the ACM Symposium on Principles of Programming Languages/. ACM/, New York/, /1/9/4/{/2/0/6/. Kranz/, D/. A/. /1/9/8/8/. Orbit/: An optimizing compiler for Scheme/. Ph/.D/. thesis/, Yale Univ/./, New

York/, /2/7/1/{/2/8/3/.

ACM Transactions on Programming Languages

- Lightweight Closure Conversion / /3/9
- Palsberg/, J/. and Schwartzbach/, M/. I/. /1/9/9/4/. Object/-Oriented Type Systems/. Wiley Professional Computing/. Wiley/, Chichester/.
- Nielson/, F/. /1/9/8/5/. Program transformations in a denotational setting/. ACM Trans/. Program/. Lang/. Syst/. /7/, /3 /(July/)/, /3/5/9/{/3/7/9/.
- Palsberg/, J/. and Schwartzbach/, M/. I/. /1/9/9/5/. Safety analysis versus type inference/. Inf/. Com/put/. /1/1/8/, /1 /(Apr/./)/, /1/2/8/{/1/4/1/.
- Proceedings of the ACM SIGPLAN /'/9/4 Conference on Programming Language Design and Implementation/. ACM/, New York/, /1/{/1/2/.
- Plotkin/, G/. D/. /1/9/7/5/. Call/-by/-name/, call/-by/-value and the //-calculus/. Theor/. Comput/. Sci/. /1/, /1/2/5/{/1/5/9/. Sabry/, A/. and Felleisen/, M/. /1/9/9/4/. Is continuation/-passing useful for data /ow analysis/? In
- Sestoft/, P/. /1/9/8/8/. Replacing function parameters by global variables/. M/.S/. thesis/, DIKU/, Univ/. of Copenhagen/.
- Shao/, Z/. and Appel/, A/. W/. /1/9/9/4/. Space/-e/cient closure representations/. Tech/. Rep/. CS/-TR//4/5/4/-/9/4/, Princeton Univ/./, Princeton/, N/.J/. Mar/.
- Sestoft/, P/. /1/9/9/1/. Analysis and e/cient implementation of functional programs/. Ph/.D/. thesis/, DIKU/, Univ/. of Copenhagen/, Denmark/.
- Shivers/, O/. /1/9/9/1/. Control/-/ow analysis of higher/-order languages/. Ph/.D/. thesis/, Carnegie/-Mellon Univ/./, Pittsburgh/, Pa/.
- tional Static Analysis Symposium/, B/. L/. Charlier/, Ed/. Lecture Notes in Computer Science/, vol/. /8/6/4/. Springer/-Verlag/, Berlin/, /1/6/2/{/1/7/8/. Steckler/, P/. and Wand/, M/. /1/9/9/4b/. Tracking available values for lightweight closures /(sum/mary/)/. In Proceedings of the Atlantique Workshop on Semantics Based Program Manipulation/,
- Steckler/, P/. /1/9/9/6/. Detecting local channels in Distributed Poly//ML/. LFCS Rep/. ECS/-LFCS//9/6/-/3/4/0/, Univ/. of Edinburgh/, Scotland/. Jan/. Steckler/, P/. and Wand/, M/. /1/9/9/4a/. Selective thunki/cation/. In Proceedings of the /1st Interna/-
- N/. Jones and C/. Talcott/, Eds/. DIKU/, Univ/. of Copenhagen/, Denmark/, /6/3/{/7/0/. Available as DIKU Rep/. No/. /9/4///1/2/.
- Steele/, G/. L/. /1/9/7/8/. Rabbit/: A compiler for Scheme/. M/.S/. thesis/, MIT/, Cambridge/, Mass/. Available as MIT Arti/cial Intelligence Laboratory Tech/. Rep/. /4/7/4/. Stefanescu/, D/. and Zhou/, Y/. /1/9/9/4/. An equational framework for the /ow analysis of higher/-order
- Steckler/, P/. A/. /1/9/9/4/. Correct higher/-order program transformations/. Ph/.D/. thesis/, Northeastern Univ/./, Boston/, Mass/.
- functions/. In Proceedings of the /1/9/9/4 ACM Symposium on Lisp and Functional Programming/. ACM/, New York/, /3/1/8/{/3/2/7/. Wand/, M/. /1/9/9/2/. Correctness of procedure representations in higher/-order assembly language/. In Proceedings of the /7th International Conference on the Mathematical Foundations of Program/-
- Wand/, M/. /1/9/9/3/. Specifying the correctness of binding/-time analysis/. J/. Funct/. Program/. /3/, /3/, /3/6/5/{/3/8/7/. Wand/, M/. and Steckler/, P/. /1/9/9/4/. Selective and lightweight closure conversion/. In Conference Record of the /2/1st ACM Symposium on Principles of Programming Languages/. ACM/, New
- ming Semantics/, S/. Brookes/, Ed/. Lecture Notes in Computer Science/, vol/. /5/9/8/. Springer/-Verlag/, Berlin/, /2/9/4/{/3/1/1/.

York/, /4/3/5/{/4/4/5/.

Received December /1/9/9/5/; revised June /1/9/9/6/; accepted September /1/9/9/6

ACM Transactions on Programming Languages