---
source: https://drmeister.wordpress.com/2016/01/29/improving-the-clasp-programming-experience/
fetched-at: 2026-10-31
converter: jina
---

Title: Improving the Clasp programming experience

URL Source: https://drmeister.wordpress.com/2016/01/29/improving-the-clasp-programming-experience/

Published Time: 2016-01-29T16:46:27+00:00

Markdown Content:
I’ve been working quietly to improve the Clasp programming experience by implementing a C++ scraper for Clasp that extracts all information from the C++ code required to expose that code to Common Lisp.

This means functions, classes, methods, symbols, enums and initialization functions are identified by the scraper and code is automatically generated to expose these entities to the Common Lisp programming environment. This replaces thousands of calls that were hand coded by me and were called at startup to expose C++ functionality to Common Lisp with automatically generated code. To expose a C++ function now all you do is some variation on this:

> namespace ext {  
>  CL_LAMBDA(x y &optional (z 0));  
>  CL_DOCSTRING(R”doc(* Arguments  
>  – x :: A fixnum  
>  – y :: A fixnum  
>  – z :: A fixnum  
>  * Description  
>  Add up to three fixnums together as long as they fit into an int.  
>  If they don’t, an error will be signaled.)doc”);  
>  CL_DEFUN int add_numbers(int x, int y, int z) {  
>  return x + y;  
>  }

The CL_LAMBDA(…), CL_DOCSTRING(…), and CL_DEFUN tags are read from the C++ source code by the scraper and code is generated to enable things like (ext:add-numbers 4 5) to be called from Common Lisp. Above is a complicated example using the optional CL_LAMBDA(…) and CL_DOCSTRING(…) macros – something as simple as below is all that is necessary to bind the C++ function to the ext:add-two-numbers symbol:

> CL_DEFUN int ext__add_two_numbers(int x, int y) {return x+y;}

The C-preprocessor is run on all of the source code with macros defined for tags like CL_DEFUN, CL_DEFMETHOD, CL_DOCSTRING(…), LISP_CLASS(…) etc. prior to the scraper searching for the tags. The scraper then generates code that is run at startup to expose everything. The scraper is run every time Clasp is built but it’s smart about only rebuilding generated code that needs to be rebuilt.

There are several benefits to this: (1) adding functions, classes, methods etc. to Clasp Common Lisp is easier now because you just add the entity and there are no more worries about where to add the call at startup to expose the entity. (2) The scraper builds a database of source location for all of these entities. So now, from Slime you can hit M-. on a Clasp symbol and emacs will jump to the source in the C++ source or Common Lisp source – wherever it is defined.

At the same time I’ve added code to extract and generate lambda-lists and docstrings for C++ functions and methods and they are also available now within the Common Lisp environment.

The scraper is written in standard Common Lisp and sbcl has been added as a build dependency for Clasp. The python scrapers Clasp used up to this point have all been retired and python is no longer a dependency for Clasp.
