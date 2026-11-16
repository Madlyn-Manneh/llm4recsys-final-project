# Homework 1 — Literature-Grounded Research Question (Individual)

**Course**: LLM4Rec, HSE University · **Instructor**: Seungmin Jin (sedzhin@hse.ru), GitHub <https://github.com/dryjins>
**Task type**: Individual homework — each student personally authors and submits their own report as the two required files below; there is no single team submission
**Required files (exactly two, as in the homework guidelines §4)**:
- PDF report: `<student-name>_session1_report.pdf`
- AI session export: `<student-name>_session1_session.json` (tool-native format accepted; see §14)
**Naming**: these follow the existing pattern `<student-id-or-name>_<assignment-id>_<report|session>.<pdf|json>` (guidelines §4.2). They are naming examples only and add no new student-ID requirement
**Submission channel**: the established homework submission channel announced in class / course chat (guidelines §4.5). A repository file, a repository link or a Markdown draft is not the submission; convert your draft to PDF and submit the PDF together with the session export
**Report format and length**: Follow existing homework report structure and page limit; this instruction adds no new format or page limit
**Header**: full student name, team name and date on the first page of the report
**Deadline**: To be announced (TBA)

---

## 1. What Session 1 asks for

Session 1 is the **Define / team** milestone: one question, one data example, one comparison. In this homework **each student converts that discussion into their own report** — personally authored, not a system-building task and not a literature survey. A reader must be able to say what you will test, on what data, against what comparison, and why the answer would matter. The target is a narrow, defensible workshop- or short-paper-level contribution; promising a complete financial advisory product is out of scope. The overall course assessment (homework-style 30, Stanford AI review 20, benchmark ranking 50) is unchanged. No Session-1-specific point allocation has been announced, so none is assigned here, and this document is not a grading rubric.

The content below is written to fit **inside the existing homework report structure** (guidelines §5); §11 gives the section-by-section mapping. Nothing here replaces the report template, the page limit or the two-file submission rule.

## 2. The shared project and the shared evaluation

Every team works on the same public data and benchmark: **FAR-Trans**, the financial asset recommendation dataset released by the University of Glasgow.

- Dataset archive: <https://researchdata.gla.ac.uk/1658/>
- Paper: <https://arxiv.org/abs/2407.08692> — Sanz-Cruzado, Droukas, McCreadie, "FAR-Trans: An Investment Dataset for Financial Asset Recommendation" (2024).

Team members may share one team topic, one dataset and one common baseline, and individual reports may **align with or refine** the team direction. Individual questions do **not** have to be mutually distinct: several members may work on closely related questions. The requirement is that **you** write your own question, your own arguments and your own comparison, not that you invent a question nobody else on the team has.

The common output is fixed: for the same evaluated users, a **Top-10 ranked list** per user, scored by **nDCG@10 against the assets each user actually purchases in the future evaluation window**.

- Intermediate **candidate generation may differ** between students.
- The encoder side, the ranker side, or **both** is not restricted. A combined system is allowed provided the report contains an ablation that separates the contributions.
- A study interested in **explanation** still emits the common Top-10 list; explanation quality is then a secondary research question, never a replacement for the shared ranking output.
- What is restricted is the **claim**: one primary question and one main comparison.

The exact **item scope, split and eligibility protocol** — evaluated users and assets, which transactions count as labels, how the evaluation window is cut — is **pending** and will be fixed by the instructor before Session 2. Until then, state your assumptions explicitly and do not present them as official.

## 3. Team registration (project administration, not a graded submission)

Team registration is **project administration**. These five fields are exactly the five columns of the **Projects** tab in the course grade sheet. Register once per team; every member still submits their own two files.

| Field | What to write |
|---|---|
| Group Name | Short team name, unique within the cohort |
| Group Leader Telegram ID | One leader; used for course communication |
| Members (Full Names in Russian) | One full name per member, as listed |
| Project Name | Working project title |
| GitHub Link | Team repository holding code and documents |

1. The team creates one shared repository, which stays **project-level**: code, shared baselines and common results live there, and the instructor is a collaborator. Registration and repository access are not a substitute for any member's two-file homework submission.
2. Register the repository link in the **Projects** sheet using the five fields above.
3. Invite the instructor as a collaborator: GitHub user **dryjins** (<https://github.com/dryjins>).
4. Each member submits their own PDF report and AI session export through the established homework submission channel (guidelines §4.5). Do not submit a shared file on behalf of the team.

Shared inputs — the team topic, the dataset, the common baseline, a shared candidate set — are legitimate to reuse and should be attributed as shared in your report.

## 4. The primary research question

Write **exactly one** primary question of your own, in the form used in class:

> We test whether [change] improves [outcome] over [baseline] for [population or condition].

A usable question names the **intervention**, the **control**, the **outcome** and the **population**. A direction hypothesis is optional; a predicted negative or null result is valid and must not be hidden. Your question may reproduce the team's common question, refine it into a narrower claim, or align with a shared baseline — but you write it, you justify it, and you own the comparison. It does not have to be a method that nobody else on the team studies.

| Example | Question shape | One sentence of business value | Minimum comparison |
|---|---|---|---|
| A | Does an LLM-written summary of past transactions beat the structured transaction history itself, for users with sparse history? | A better cold-start list means fewer users receive generic, uninformed suggestions. | Same candidates, item information and downstream ranker; only the history representation changes |
| B | With identical candidates and item information, does an LLM re-ranker beat a classical learned ranker and a rule-based baseline? | A measured gain (or its absence) tells a product owner whether LLM re-ranking is worth its latency. | Classical ranker and rule baseline, same inputs, users and metric |
| C | Does swapping two users' histories change the ranking in a way that tracks real user relevance, not only text style? | A personalization claim that survives swapping is defensible to a compliance reviewer. | History-swap ablation; relevance judged by a human or objective check, never a screenshot or self-assigned score |

These are **illustrative shapes, not established novelty**. Adopting one is allowed; it is not permission to claim that the cited papers have already answered your question.

## 5. Literature grounding: 3–5 studies

Cite **3–5 genuinely related studies** in **your own** focused comparison, not a reading list and not a table copied from a teammate:

| Study (authors, year, venue) | Problem and method | Data and evaluation | Limitation and link to your question |
|---|---|---|---|
| | | | |

Then state in one short paragraph which study is the **nearest prior work**, what it **did answer**, what it **did not answer** (the gap you target), and why your comparison stays informative even if your result is close to that work. A study the team discussed together may appear here, but the selection and the gap argument must be yours; if a teammate reads the same paper, say what you took from it.

Citations: authors, year, venue and a resolvable URL or DOI must be correct. Do not invent citations, venues or numbers, and do not write "no research exists" — write "we did not find a study reporting X under condition Y". A hallucinated reference is a research-integrity failure. Two leads from course discussion, **FLARKO** and **ConvFinRe**, are worth investigating as possible nearest prior work; verify each yourself and cite only what you opened.

This material belongs in **§2 Related Work** of the report, with the reference list in IEEE numbered format.

## 6. Data example: one actual record

Opening the official archive and reading a small raw data file yourself is part of this task; the instructor does not supply an extracted record for you, and a record you have not opened and checked yourself does not count — even if a teammate found it. Show **one actual record**, sanitized, with its **field names** and **verbatim values** — never fabricated, never paraphrased from the paper. State the **source file**, the **row or record id**, the **field names**, the **values**, and which **window or split** the record belongs to. If a field is masked, missing or empty, show it as it is and say so. Never attach a real person's identity to a record and do not republish anything outside the public release; anonymised customer and asset identifiers are fine.

```
file: <path inside the released archive>   row id: <verbatim id>
fields: <field 1>, <field 2>, <field 3>, ...
values: <verbatim value 1>, <verbatim value 2>, ...
window/split: <period or split this record belongs to>
```

The placeholders above are **not** a real record. Classify every profile field you use as **observed**, **predicted/estimated** or **missing**, and timestamp it; any value knowable only after the prediction time is future leakage and must be excluded.

This material belongs in **§3 Method** (data and fields) of the report.

## 7. Research importance versus business value

Two distinct arguments, both required; do not merge them into one paragraph about revenue.

| | Research importance | Business value |
|---|---|---|
| Answered | What new knowledge does the field gain? | Which decision changes for a named stakeholder? |
| Audience | Researchers on FAR and LLM-based ranking | Advisor, product owner, or compliance reviewer |
| Positive result | Which claim becomes supported, under which condition? | What would that stakeholder change? |
| Negative result | What assumption should the field drop? | What cost or risk is avoided by not deploying? |

Observed transactions are **behaviour**, not advice and not profit: a user buying an asset is not evidence that the asset was a good investment. Do not claim your metric measures profitability unless you define and justify it, and do not assert causal effects on clicks or revenue. Ground the business hypothesis in the cited literature, not in intuition. State what the experiment would show; do not promise publication.

These two arguments belong in **§1 Introduction** (motivation and contributions) and are revisited in **§5 Discussion**.

## 8. Minimal study design

Fill this table. Blank rows, or "TBD" without a stated reason, count against you.

| Field | What to specify |
|---|---|
| RQ and scope | The one primary question; what is explicitly out of scope |
| Evaluated users and subgroups | Who is scored; cold / light / heavy activity subgroups if analysed |
| Data fields used | Field names with the real example from §6, and their timestamps |
| Baseline(s) | At least one, receiving the **same information** as the proposed method |
| Proposed method | The single change under test: encoder, ranker, or both, with an ablation |
| Ablations and controls | Variant removing the change; controls for prompt, candidate set and information asymmetry |
| Primary metric | Common Top-10 list, nDCG@10 over the shared users and future purchases |
| Secondary metrics | Subgroups, explanation or qualitative measures; ROI-style measures secondary only |
| Seeds, repeats, cost | Number of runs, what varies, expected runtime and budget |
| Feasibility in four sessions | What is finished by Sessions 2, 3 and 4 |
| Ethical and leakage risks | Privacy, re-identification, LLM knowledge contamination, temporal leakage |
| Current state | Baseline working or not; the next concrete step |

This table belongs in **§3 Method**.

## 9. Team Discussion and Individual Position (inside the report)

This is a **required part of your individual report** — written in the report itself, not a separate team deliverable and not a team-authored document. Because the project is shared, the report must show what the team discussion contributed and what you decided yourself. Keep it brief: it goes into **§5 Discussion** and adds no extra file or page budget of its own.

Cover four things:

1. **Topics and options discussed** — which questions, methods, baselines, data slices or comparison designs the team considered, including the ones that were dropped.
2. **Agreement and unresolved differences** — what the team converged on, and where members still differ. Unresolved disagreement is acceptable and must be reported honestly; nobody has to claim the team reached consensus, and no consensus requirement exists.
3. **Your own contribution to the discussion** — the options you proposed, the evidence you brought, the objections you raised, and the work you did (paper read, data explored, baseline probed).
4. **Your position and why** — which option you adopt in this report, which you reject, and the technical or evidential reason. "The team chose it" is not a reason; "it was the only option nobody had time to check" is.

| Field | What to write |
|---|---|
| Topics and options discussed | The candidate questions or designs the team weighed |
| Team agreement | What the team settled on, as far as it settled |
| Unresolved differences | Where members still disagree, stated plainly, possibly unresolved |
| Your contribution | What you personally proposed, checked or argued in the discussion |
| Your adopted position and reason | The option you take here, and the reason it is yours |
| Rejected options and reason | What you are not doing, and why |

Two integrity rules:

- **Separate joint ideas from your own analysis.** Mark which parts came out of the team discussion and which are your own reading, data check or argument. Shared inputs — the team topic, the dataset, the common baseline, a shared candidate set — are legitimate to reuse and should be attributed as shared.
- **No verbatim team text.** Do not copy a teammate's or a joint draft and present it as your individual work. Identical or near-identical submissions, or text whose authorship you cannot explain, are treated as a research-integrity problem, not as collaboration.

## 10. Scope guards, feasibility and ethics

- The project must fit **four sessions**; if it does not fit, cut the question, not the evaluation.
- This is **not** a full financial service, not a brokerage system and not live trading: no real money, no real orders, no personal investment advice. Short-horizon returns over a few days are not an acceptable primary metric.
- The **team project** produces the common Top-10 output; explanation work ships it too.
- The baseline must receive the **same information** as the LLM condition. If the LLM sees profile text and the baseline does not, the comparison is confounded and the result is not about the method.
- An **LLM judge is never the sole ground truth**; pair it with human review, rule-based checks, or an objective metric.
- **LLM knowledge contamination** is a real risk: state the model, version, knowledge cutoff, and how you control for content the model may have seen during pretraining.
- Secondary data and historical confounds — market regime, survivorship, stale profiles — must be named in the report, not discovered in the results.

## 11. How this maps into the existing report structure

The report keeps the section structure, headings and page limit of the homework guidelines (guidelines §5). This homework adds content, not a new format and not a new section list.

| Existing section (guidelines §5) | What goes there in Homework 1 |
|---|---|
| Title block | Paper-style title; student name, team, email, date; assignment line |
| Abstract | Existing 4-sentence structure. If no experiment has been run, the third sentence states the planned comparison and what would count as support — no invented number or result |
| Index Terms (optional) | 3–5 keywords, IEEE format |
| §1. Introduction | Problem statement, motivation, one concrete example, contributions; research importance and business value as two separate arguments (this document §7) |
| §2. Related Work | The 3–5-study comparison table, nearest prior work, explicit gap; IEEE numbered references |
| §3. Method | The proposed study: RQ and four elements, design table (this document §8), data example and field provenance (this document §6), baselines, ablations, metric, seeds/cost, feasibility, ethics and leakage |
| §4. Experiments | Only what was actually run: setup, results, comparison, verification. If nothing has been run, this section states the evaluation **plan**, explicitly labelled as planned, and contains **no fabricated results, tables or numbers** |
| §5. Discussion | The analysis you can defend: gap and validity threats, what a positive or negative result would mean, and the Team Discussion and Individual Position (this document §9). No invented failure cases or results |
| §6. AI Usage Disclosure (guidelines §6) | **Mandatory.** Tools and versions, how AI was used, what you personally verified, what you trusted without verification, and the session-export reference (this document §14) |
| References | IEEE numbered format, continuing from §2; only sources you actually opened |

Ordering, headings and length follow the existing guidelines and template unchanged; the page limit is the existing one (maximum 5 pages excluding references), and earlier work may be shorter.

## 12. Checklist

- [ ] Two files submitted: `<student-name>_session1_report.pdf` and `<student-name>_session1_session.json`.
- [ ] The PDF is the report, converted from your draft if needed; a repository file, repository link or Markdown draft is not the submission.
- [ ] Report follows the existing homework structure and page limit; no new format or page limit is introduced here.
- [ ] Title block carries your full student name, team name and date.
- [ ] Exactly one primary question with intervention, control, outcome and population.
- [ ] §2 Related Work has 3–5 genuinely related studies in a comparison table, each with a stated limitation; the nearest prior study is named with what it answered and what it left open.
- [ ] One actual sanitized record with source file, row id, field names and verbatim values; every used field timestamped; observed/predicted/missing stated; no future leakage.
- [ ] Research importance and business value written as two separate arguments.
- [ ] §3 Method: baseline and proposed method receive identical information; ablation and controls defined; design table complete, with no blank or unexplained "TBD".
- [ ] Common Top-10 / nDCG@10 deliverable acknowledged, including by explanation-oriented studies.
- [ ] Feasibility for four sessions, with seeds, repeats and cost.
- [ ] Ethical, privacy and LLM-contamination risks named.
- [ ] §4 Experiments reports only what was run; if nothing was run, it is explicitly labelled as a plan with no fabricated results.
- [ ] §5 Discussion contains the Team Discussion and Individual Position: options, agreement/unresolved differences, your contribution, your position and reasons, rejected options.
- [ ] Joint ideas distinguished from your own analysis; nothing copied verbatim from a teammate or a joint draft.
- [ ] §6 AI Usage Disclosure is present and honest, including personal verification of critical outputs, and matches the session export; if no AI was used, §6 says so.
- [ ] Session export is the unmodified tool-native log (Codex JSONL is acceptable) showing tool calls, file changes and results.
- [ ] No invented citations, no invented data values, no promise of publication.

## 13. Review criteria

No point values are published here; these are the six qualities reviewers look for. The existing rubric and grading structure are unchanged.

| Criterion | What reviewers look for |
|---|---|
| Research question is clear | One question of your own; four elements named; narrow enough to be answered |
| Literature is grounded | Real, resolvable, related studies; honest gap; no novelty overclaim |
| Business importance is argued | Named stakeholder and changed decision; importance separated from business value |
| Evaluation is valid | Shared Top-10 and nDCG@10; identical information; ablation and controls; no leakage |
| Feasibility | Fits four sessions; credible baseline plan; seeds, repeats and cost addressed |
| Individual authorship is visible | Team Discussion present inside the report; your own contribution and position argued; joint and individual work distinguished; no copied joint text |

## 14. AI assistance, the session export and research integrity

AI assistance is **permitted** for searching literature, reading papers, drafting and checking code. Verification stays **yours**: every citation, number and data value must be confirmed by you against the primary source. The guidelines' §6 and §9 rules apply unchanged; nothing here grants an exemption or requires you to use AI.

- **Disclose in §6** the tools and versions used and how AI materially shaped the report, together with what you personally verified and what you trusted without verification.
- **Submit the session export** as the audit trail: use your tool's native export. Codex JSONL is accepted as-is, and no conversion to another format is imposed. A derivative export is acceptable only if it preserves the code, tool calls and results that produced the work, and it carries a note saying what was derived and why. The original ordering remains valid.
- **Do not add AI use that did not happen**, and do not hide AI use that did. If you used no AI, §6 states that, per the existing guidelines' FAQ.
- AI-generated text is not a substitute for your own position: the Team Discussion must reflect a discussion that actually happened, and you must be able to defend every claim in the report.

## 15. Version

- **v1.2** — 2026-11-03 — Corrects the delivery rules of v1.1, which were wrong (recorded here so the mistake is neither left active nor silently historical): the homework is the two files required by the guidelines §4 — a PDF report plus an AI session export — and not a Markdown draft, not a submission where a PDF is unnecessary, and not the team repository treated as the submission. Removes the page limit invented in v1.1; the existing report structure and page limit apply unchanged, and §6 AI Usage Disclosure is mandatory. Content requirements (one question, 3–5 studies, one real data record, research importance and business value, minimal design, team discussion) are retained and mapped into the existing report sections (§11). Deadline remains TBA; rubric and grading unchanged.
- v1.1 — Session 1 — Homework 1 moved to individual submission with a required Team Discussion and Individual Position section (deadline TBA). Its delivery-format and page-limit statements are superseded by v1.2; its content requirements remain in force.
- v1.0 — Session 1 — Initial Homework 1 instructions (deadline TBA). Superseded by v1.1 and v1.2 on delivery format.