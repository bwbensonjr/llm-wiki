---
source: https://docs.racket-lang.org/rhombus-guide/standalone.html
fetched-at: 2026-11-01
converter: jina
---

Title: 10.5 Standalone Rhombus Programs

URL Source: https://docs.racket-lang.org/rhombus-guide/standalone.html

Markdown Content:
[![Image 1: Racket](assets/2026-11-01-10-5-standalone-rhombus-programs/img-1.png)](https://racket-lang.org/)

1.1+9.3

Rhombus

### 10.5[](https://docs.racket-lang.org/rhombus-guide/standalone.html)Standalone Rhombus Programs[🔗](https://docs.racket-lang.org/rhombus-guide/standalone.html#(part._standalone) "Link to here")[ℹ](https://docs.racket-lang.org/rhombus-guide/standalone.html "Internal Scribble link and Scribble source")

Racket tools generally work on Rhombus programs, and that includes tools for creating and distributing standalone executables.

To generate a standalone executable prog from prog.rhm, use [raco exe](https://download.racket-lang.org/releases/9.3/doc/local-redirect/index.html?tag=%28part._%28.%27%28lib._scribblings%2Fraco%2Fraco..scrbl%29.%27._.%27exe.%27%29%29&version=9.3):

> raco exe prog.rhm

That’s only the first step to creating an executable that can run on other machines, however. The resulting prog works on the machine used to build it, but it still relies on a Racket and Rhombus installation. To create a distribution that can be installed on another machine, use [raco dist](https://download.racket-lang.org/releases/9.3/doc/local-redirect/index.html?tag=%28part._%28.%27%28lib._scribblings%2Fraco%2Fraco..scrbl%29.%27._.%27test.%27%29%29&version=9.3):

> raco dist prog_dist prog

which assembles all needed files in "prog_dist".

By default, a standalone executable and distribution simply packages up all of the support needed to run a program the same as when running rhombus or racket directly. If a program does not use dynamic compilation facilities such as [eval](https://docs.racket-lang.org/rhombus-reference/Eval.html?version=9.3#%28def._%28%28submod._%28lib._rhombus%2Fprivate%2Famalgam..rkt%29._core%29._eval%29%29), then demodularizing and removing unneeded code can produce a smaller implementation that starts up more quickly. The [raco demod](https://download.racket-lang.org/releases/9.3/doc/local-redirect/index.html?tag=%28part._%28.%27%28lib._scribblings%2Fraco%2Fraco..scrbl%29.%27._.%27test.%27%29%29&version=9.3) tool performs that kind of pruning:

> raco demod -g --work /tmp/work -o prog_small.zo prog.rhm

The output "prog_small.zo" can then be converted to an executable and/or distribution.

For cross compilation, see [raco cross](https://download.racket-lang.org/releases/9.3/doc/local-redirect/index.html?tag=%28part._%28.%27%28lib._raco%2Fprivate%2Fcross%2Fraco-cross..scrbl%29.%27._.%27top.%27%29%29&version=9.3).
