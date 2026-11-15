---
type: summary
title: Formalizing the US tax code
created: 2026-11-15
source: https://lexifina.com/blog/formalizing-the-us-tax-code
raw: raw/2026-11-15-formalizing-the-us-tax-code.md
tags: [formal-methods, program-verification, agentic-coding, legislation-formalization]
---

# Formalizing the US tax code

## Summary

[[lexifina|Lexifina]] describes applying [[formal-methods|formal methods]] to
US tax legislation through its versioned global-law repository and
[[lean-proof-assistant|Lean]]. The November 10, 2026 article distinguishes
three kinds of work: structural checks on statutory text, an executable model
of a household's 2025 federal income tax, and searches for advantageous
combinations of rules. These have different coverage: the executable model
does not formalize the entire Internal Revenue Code.

For structural checking, a parser extracts explicit and prose cross-references
from the official Title 26 XML release current to November 3, 2026. The project
reports 257 findings, triaged by AI into 98 intended references, 21 false alarms
in editorial hyperlinks, and 138 drafting faults. Those faults comprise 67 stale
references, 24 typos or other citation defects, eight wrong subdivision labels,
nine duplicate numbers, and 30 unclosed parentheses. Each reported fault has a
Lean certificate carrying evidence from the XML. Version history attributes
faults to public laws, and regression checks flag newly introduced defects.

The income-tax model separates income, deductions, tax, and credits. AI agents
translate provisions into Lean; a different agent reviews the translation.
Tests compare outputs with IRS tables and examples and three independent
calculators on 5,000 households. The article reports exact agreement with
PolicyEngine-US for 4,993 households, with the remaining seven differing by at
most $11 because of EITC table-versus-formula treatment. Differential testing
also exposed two mistakes in the project's own model. Proofs establish
properties over all modeled inputs, such as deductions not increasing as
income rises, rather than merely testing sampled households.

Searches evaluate 195,787 single-year returns and roughly 30,000 multi-year
plans. They rediscover established planning strategies and produce three
findings the authors say they could not locate in practitioner sources:
Social Security and investment-income interactions under separate filing,
and a claimed discrepancy between Schedule 8812 and the refundable-child-credit
statute. These are reported model findings, not independently established
legal conclusions. The article also describes effective-date mismatches,
rounding differences, and benefit cliffs as distinct sources of surprising
behavior.

The dependency diagram separates drafting certificates, the income-tax model,
and loophole searches into three groups. It reports 2,159 declarations,
including 516 theorems, linked by 3,577 dependencies across 12,063 source lines;
its maximum dependency depth is 12. The diagram makes the layered construction
of checks, definitions, proofs, and searches visible.

The authors explicitly identify translation from law into Lean as a lossy
step. Drafting triage and adversarial reviews were performed by AI agents and
had not been checked by a lawyer or CPA. The model omits several tax categories
and preferences, and its multi-year searches hold 2025 law constant. Agreement
among calculators may reflect a shared misreading. Human judgment remains
necessary to distinguish deliberate policy choices, drafting defects,
compilation artifacts, and errors in administrative forms.

## Why this matters

The question is whether [[legislation-formalization|legislation formalization]]
can be useful beyond tax law. This example suggests separating the broadly
reusable structural work, such as checking references, numbering, and effective
dates, from the harder task of faithfully modeling legal meaning. Versioned
text, executable rules, independent comparisons, and regression checks form a
plausible method to investigate in other legislative domains; their success
there remains an inference, not a result demonstrated by this article.

The connection to [[agentic-coding|agentic coding]] is especially useful:
agents can lower the cost of constructing formal models, while proof checking
provides precise feedback. The boundary matters just as much as the promise:
a proof establishes consequences of the chosen definitions, so legal review
and evidence that those definitions match the legislation remain central.
