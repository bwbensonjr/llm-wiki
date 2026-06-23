---
type: summary
title: The Janet Programming Language
created: 2026-06-23
source: https://janet-lang.org/
raw: raw/2026-06-23-the-janet-programming-language.md
tags: [janet, lisp, programming-languages]
---

# The Janet Programming Language

## Summary

The official homepage of [[janet|Janet]], presenting the language and its
feature set. Janet is pitched as a system scripting language and an embeddable
language, implemented mostly in standard C99 and running on Windows, Linux, and
macOS. Unlike many embeddable languages it ships with more out of the box:
threading, networking, an event loop, subprocess handling, and a built-in PEG
(parsing expression grammar) library for text matching.

Highlighted features include first-class closures and green threads
(continuations), garbage collection, tail-call optimization, lexical scoping,
[[lisp|Lisp]]-style macros, and mutable/immutable variants of arrays
(array/tuple), hashtables (table/struct), and strings (buffer/string). It offers
direct C interop (abstract types, C functions, dynamic library loading), a REPL
with an interactive debugger, Erlang-style supervision trees integrated with the
event loop, and a core library of 600+ functions and macros. Projects export to
standalone executables via the companion `jpm` build tool, and Janet embeds into
a project by adding just `janet.c` and `janet.h`.

The page also surveys the ecosystem: a `jpm`-installable package listing,
libraries (HTTP via Circlet, the Joy web framework, JSON, SQLite, WebView,
Raylib bindings via Jaylib, cryptography), broad editor support, community on
Zulip and GitHub Discussions, and learning resources — the official docs, the
beginner-friendly *Janet Guide* by [[ian-henry|Ian Henry]], and Janet Docs.

## Why this matters

This matters to me because it is a high-level and comprehensive description of
the Janet Lisp dialect.
