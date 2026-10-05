# Owner fidelity review findings — 2026-10-05

Source: owner-completed `FIDELITY_REVIEW.md`, read without modifying it.

The owner identified numeric forms and compound splits as the same spoken words. In Call 4, the owner heard approved `is` rather than ASR `was`, and heard the `I` missed by ASR. These resolve those particular recognizer disagreements in favor of approved words; they do not supply precise word boundaries.

The owner confirmed spoken `a` at 132.44–134.80 seconds in Call 4 and 129.82–132.16 seconds in Call 6. The authoritative submitted text says `They eat cereal out of mug because all the dishes are dirty`; recognition says `out of a mug`. The confirmed additional article violates the current exact approved-word fidelity criterion. Neither tested coherent source can currently be recorded as passing that mandatory criterion. This finding concerns these outputs, not universal infeasibility of B.

The Call 4 note `in and and both in the same sentence` does not unambiguously resolve the disputed word. Approved context: `pull back the curtain in The Wizard of Oz and realize`. Recognized context: `pull back the curtain and the wizard of Oz and Realize`. The owner needs to specify the actual phrase around `curtain` to distinguish the approved later `and` from a substitution/addition at the disputed position.

The full-source check lines remain instructions, without an explicit returned finding. Do not infer full-source fidelity, truncation or clipping acceptance from those unchanged lines. Independent boundary-reference/mapping validation remains unresolved separately.

**S5: NOT_YET_PASS.** B initial + B affected-segment correction remains the selected owner policy, not an accepted passing acoustic implementation. Do not silently amend approved text to accommodate generated speech, weaken exact fidelity, regenerate or make provider calls. The smallest next owner decision is whether `out of a mug` should become explicitly approved fixture text or whether these outputs must remain fidelity failures against the original text. A text amendment does not retroactively change the submitted request provenance or establish that future generation preserves exact words; document any such decision separately.

Zero provider calls were made in recording this review. No source WAV or owner review was modified. S6/S9, production implementation, TASKS.md, deployment and purchases were not performed.
