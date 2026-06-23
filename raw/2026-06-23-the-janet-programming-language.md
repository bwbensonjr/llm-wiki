---
source: https://janet-lang.org/
fetched-at: 2026-06-23
converter: jina
---

Title: The Janet Programming Language

URL Source: https://janet-lang.org/

Published Time: Sat, 09 May 2026 01:57:09 GMT

Markdown Content:
## Use Cases

Janet makes a good system scripting language, or a language to embed in other programs. Janet also can be used for rapid prototyping, dynamic systems, and other domains where dynamic languages shine. Implemented mostly in standard C99, Janet runs on Windows, Linux and macOS. The few features that are not standard C (dynamic library loading, compiler specific optimizations), are fairly straightforward. Janet can be easily ported to new platforms. While Janet is embeddable, it comes with a bit more out of the box than many other such easily embeddable languages such as threading, networking, an event loop, subprocess handling, regex-like library called PEG, and more.

## Features

*   Minimal setup - one binary and you are good to go!
*   Builtin support for threads, networking, and an event loop
*   First class closures
*   Garbage collection
*   First class green threads (continuations)
*   Mutable and immutable arrays (array/tuple)
*   Mutable and immutable hashtables (table/struct)
*   Mutable and immutable strings (buffer/string)
*   Macros
*   Tail call optimization
*   Direct interop with C via abstract types and C functions
*   Dynamically load C libraries
*   Lexical scoping
*   REPL and interactive debugger
*   Parsing Expression Grammars built in to the core library
*   600+ functions and macros in the core library
*   Erlang-style supervision trees that integrate with the event loop
*   Export your projects to standalone executables with a companion build tool, jpm
*   Add to a project with just `janet.c` and `janet.h`

## Code Example

```
(defn sum3
  "Solve the 3SUM problem in O(n^2) time."
  [s]
  (def tab @{})
  (def solutions @{})
  (def len (length s))
  (for k 0 len
    (put tab (s k) k))
  (for i 0 len
    (for j 0 len
      (def k (get tab (- 0 (s i) (s j))))
      (when (and k (not= k i) (not= k j) (not= i j))
        (put solutions {i true j true k true} true))))
  (map keys (keys solutions)))

(let [arr @[2 4 1 3 8 7 -3 -1 12 -5 -8]]
  (printf "3sum of %j: " arr)
  (printf "%j" (sum3 arr)))
```

## Try It

>

(print "hello, world!")

## Get Started

Check out the [documentation](https://janet-lang.org/docs/index.html) for an introduction and installation instructions.

## Usage

A REPL is launched when the `janet` binary is invoked with no arguments. Pass the `-h` flag to display the usage information. Individual scripts can be run with `janet myscript.janet`

If you are looking to explore, you can print a list of all available macros, functions, and constants by entering the command `(doc)` into the REPL.

```
$ janet
Janet 1.40.1-1449ad8b linux/x64/gcc - '(doc)' for help
repl:1:> (+ 1 2 3)
6
repl:2:> (print "Hello, World!")
Hello, World!
nil
repl:3:> (os/exit)
$ janet -h
usage: janet [options] script args...
Options are:
  --help (-h)             : Show this help
  --version (-v)          : Print the version string
  --stdin (-s)            : Use raw stdin instead of getline like functionality
  --eval (-e) code        : Execute a string of janet
  --expression (-E) code arguments... : Evaluate an expression as a short-fn with arguments
  --debug (-d)            : Set the debug flag in the REPL
  --repl (-r)             : Enter the REPL after running all scripts
  --noprofile (-R)        : Disables loading profile.janet when JANET_PROFILE is present
  --persistent (-p)       : Keep on executing if there is a top-level error (persistent)
  --quiet (-q)            : Hide logo (quiet)
  --flycheck (-k)         : Compile scripts but do not execute (flycheck)
  --syspath (-m) syspath  : Set system path for loading global modules
  --compile (-c) source output : Compile janet source code into an image
  --image (-i)            : Load the script argument as an image file instead of source code
  --nocolor (-n)          : Disable ANSI color output in the REPL
  --color (-N)            : Enable ANSI color output in the REPL
  --library (-l) lib      : Use a module before processing more arguments
  --lint-warn (-w) level  : Set the lint warning level - default is "normal"
  --lint-error (-x) level : Set the lint error level - default is "none"
  --install (-b) dirpath  : Install a bundle from a directory
  --reinstall (-B) name   : Reinstall a bundle by bundle name
  --uninstall (-u) name   : Uninstall a bundle by bundle name
  --update-all (-U)       : Reinstall all installed bundles
  --prune (-P)            : Uninstall all bundles that are orphaned
  --list (-L)             : List all installed bundles
  --                      : Stop handling options
```

## Modules and Libraries

See some auxiliary projects on [GitHub](https://github.com/janet-lang). Here is a short list of libraries for Janet to help you get started with some interesting stuff. See [the Janet Package Listing](https://github.com/janet-lang/pkgs) for a more complete list. Packages in the listing can be installed via `jpm install pkg-name`.

*   [Circlet](https://github.com/janet-lang/circlet) - An HTTP server for Janet
*   [Joy Web Framework](https://joy.swlkr.com/) - Framework for web development in Janet
*   [JSON](https://github.com/janet-lang/json) - A JSON parser and encoder
*   [SQLite3](https://github.com/janet-lang/sqlite3) - Bindings to SQLite
*   [WebView](https://github.com/janet-lang/webview) - Spawn a browser window for creating HTML+CSS UIs on any platform
*   [Jaylib](https://github.com/janet-lang/jaylib) - Bindings to Raylib for 2d and 3d game development
*   [JHydro](https://github.com/janet-lang/jhydro) - Cryptography for Janet
*   [JanetUI](https://github.com/janet-lang/janetui) - Bindings to [libui](https://github.com/andlabs/libui)

## Editor Support

Janet support exists for a number of editors. See the links below for some editor-specific details. The Zulip Instance also has an [editors and tooling](https://janet.zulipchat.com/#narrow/stream/409409-editors-and-tooling) discussion area.

*   [Neovim](https://github.com/sogaiu/janet-editor-and-tooling-info/blob/master/doc/neovim.md)
*   [Vim](https://github.com/sogaiu/janet-editor-and-tooling-info/blob/master/doc/vim.md)
*   [VSCode](https://github.com/sogaiu/janet-editor-and-tooling-info/blob/master/doc/vscode.md)
*   [Emacs](https://github.com/sogaiu/janet-editor-and-tooling-info/blob/master/doc/emacs.md)
*   [Sublime Text](https://github.com/sogaiu/janet-editor-and-tooling-info/blob/master/doc/sublime-text.md)
*   [Kakoune](https://github.com/sogaiu/janet-editor-and-tooling-info/blob/master/doc/kakoune.md)
*   [TIC-80](https://github.com/sogaiu/janet-editor-and-tooling-info/blob/master/doc/tic-80.md)
*   [Helix](https://github.com/sogaiu/janet-editor-and-tooling-info/blob/master/doc/helix.md)

### Zulip

View or join the Janet Zulip Instance at [https://janet.zulipchat.com](https://janet.zulipchat.com/) ([Invite Link](https://janet.zulipchat.com/join/3ahdqkn5cvr6233x6ytzlcvq/))

### Forum

We also support [GitHub Discussions](https://github.com/janet-lang/janet/discussions), but Zulip has richer functionality.

### Janet Guide

The [Janet Guide](https://janet.guide/) is a beginner-friendly on-ramp to the language that provides a more opinionated tutorial than the official documentation.

### Janet Docs

For help, you can also check out [Janet Docs](https://janetdocs.org/) for Janet documentation with user-provided examples. Feel free to contribute your own examples here to help fellow programmers.
