# PyP6Xer Review — Correctness, Spec Compliance, Performance
**Date:** 2026-10-28 · **Repo:** HassanEmam/PyP6Xer @ 0452d9f (clone: `~/PyP6Xer-review`)
**Method:** 3 independent review passes (correctness, spec-vs-Oracle data map, performance) + empirical probes. All 36 existing tests pass; none cover the findings below. Spec reference: Oracle XER Import/Export Data Map (Project) v19 — all 63 table pages parsed and machine-diffed against the library.

---

## 1. VERDICT

The reader is broadly faithful for the core tables (CALENDAR, TASKACTV, UDFVALUE, SCHEDOPTIONS, TASKPRED structure are near-perfect on field names), but the library has:

- **7 wrong-source assignments** — an attribute read from the wrong XER column, silently corrupting data even on a perfect round-trip
- **5 tables silently dropped by the writer** (ROLES, ROLERATE, RCATTYPE, RCATVAL, RSRCRCAT) + RSRCCURV never read
- **4 critical parser defects** (encoding loss, blank-line crash, cross-file state leak, narrow-schema crash)
- **DCMA14 is unreliable**: check #5 matches a nonexistent code, checks #12–#14 unimplemented, and it crashes on ordinary schedules
- **~2.1× available performance win**, already implemented and tested on a branch

## 2. CRITICAL (data corruption or crash on common inputs)

| # | Where | What |
|---|---|---|
| C1 | reader.py:327 | `encoding='utf-8', errors='ignore'` — XER files are CP1252; every non-ASCII character in names/codes is **silently deleted** ("Café" → "Caf"). Verified. |
| C2 | reader.py:330 | `row[0]` on an empty row (trailing blank line) → `IndexError`; file unparseable. Verified. |
| C3 | task.py:31, taskpred.py:22, wbs.py:24, calendar.py:24 + ~16 more classes | Class-level `obj_list` shared across all Readers. Parse file B after A in one process → B's tasks resolve to **A's calendars** (wrong durations) and A's relationships pollute B's `has_no_predecessor/successor`. Verified. |
| C4 | dcma14/analysis.py:118 | Hard-constraint check tests `['CS_MANDFIN','CS_MANDFIN']` — a duplicated, **nonexistent** XER code (real: `CS_MSO`, `CS_MEO`, …). The check can never fire on real data. |
| C5 | dcma14/analysis.py:185, 97/107, 153 | Crashes on ordinary schedules: `None > datetime` TypeError, ZeroDivisionError with 0 relationships, KeyError on missing proj_id. Verified. |

## 3. MAJOR

**Wrong-source (read column X, store under name Y) — all empirically verified:**
- taskpred.py:29 — `pred_proj_id` read from `proj_id` → cross-project relationships corrupted on round-trip
- taskrsrc.py:64 — `act_this_per_qty` read from `act_this_per_cost`
- rsrc.py:56 — `last_checksum` read from `level_flag`
- project.py:87 — `last_baseline_update_date` read from `last_fin_dates_id`
- role.py:33 — `last_checksum` read from `role_descr`
- rsrcrcat.py:25 — `rsrc_catg_id` read from `rsrc_catg_type_id`
- schedoption.py:48 — `key_activity_for_multiple_longest_paths` dropped when a *different* field is empty (wrong guard key)

**Reader/writer defects:**
- reader.py:335 — rows shorter than the header truncate via `zip`, then unguarded `.strip()` in wbs.py:29–51 crashes → **any older/narrower PROJWBS schema fails to parse at all**. Longer rows silently lose columns.
- reader.py:328 — csv default `quotechar='"'` corrupts fields starting with `"` (XER quotes are literal data). Fix: `quoting=csv.QUOTE_NONE`.
- write.py — `roles`, `rolerates`, `rcattypes`, `rcatvals`, `rsrccats` collections are parsed but **never written**; ROLE rows in input vanish from output (verified). Also `roles.py:32` emits `%T ROLE` (should be `ROLES`).
- write.py:23 — ERMHDR is hardcoded (version 8.0, date 2021-11-02, user "admin"); source header never preserved on round-trip.
- task.py:258 — `Task.totalint` references nonexistent `total_int_hr_cnt` → AttributeError; also hardcodes ÷8.0.
- task.py:202–206 — bare `try/except pass` around external dates: one bad date leaves **both** attributes unset → later AttributeError in get_tsv.
- task.py:44 — `phys_complete_pct=''` → ValueError (uses `in params` instead of truthiness).
- tasks.py:180–188 — `Tasks.__iter__` is one-shot: second iteration silently returns nothing.
- tasks.py:87 — `duration_greater_than` uses `self.calendar` on the collection → AttributeError. tasks.py:94–120 — float filters crash on `None` total float / unresolved calendar.
- activitiyresources.py:71 — `len()` on ActivityResources crashes (class-attr reference).
- reader.py:124 — `summary()` references nonexistent `self.tasks`.
- wbs.py:69–91 — `get_json`/`get_childs` overwrite dict keys in loops → only the last root/child survives.
- calendar_data.py:86–102 — `get_days` keys are positional, and non-working days are unrepresentable (`len(x) > 0` always True); returns `None` on unmatched data.
- Dates: `%Y-%m-%d %H:%M` only — seconds-precision exports raise ValueError (risk, unverified against real export).

## 4. SPEC COMPLIANCE (vs Oracle data map, per table)

| Table | Verdict | Key evidence |
|---|---|---|
| CALENDAR | COMPLIANT | 13/13 correct sources |
| TASKACTV, UDFVALUE, CURRTYPE, OBS, ACCOUNT, RSRCRATE, TASKPROC, RSRCCURVDATA, PROJPCAT, TASKRSRC-structure | COMPLIANT | field-aligned, header=row counts |
| TASK | MAJOR GAPS | reads `int_path`/`int_path_order` but spec+writer say `float_path`/`float_path_order` → always None + round-trip loss; drops `review_end_date`, `review_type` |
| TASKPRED | MAJOR GAPS | pred_proj_id wrong source; invents `comments`,`float_path`,`aref`,`arls` (not on v19 page) |
| TASKRSRC | MAJOR GAPS | act_this_per_qty wrong source; drops 7 spec fields (pend_*, prior_ts_*, wbs_id) |
| PROJECT | MAJOR GAPS | last_baseline_update_date wrong source; drops 17 spec fields; invents 10 |
| RSRC | MAJOR GAPS | last_checksum wrong source; drops 4; invents 3 |
| ROLES | MAJOR GAPS | wrong source; **never written** |
| RSRCCURV | UNSUPPORTED | rows silently ignored by reader |
| ACTVTYPE / PCATTYPE | MAJOR GAPS | drop `super_flag` (secure-code flag) / weights; invent fields |
| PROJWBS, SCHEDOPTIONS, ACTVCODE, UDFTYPE, PCATVAL, RCATTYPE, RCATVAL | MINOR GAPS | 1–2 dropped/invented fields each |
| — | UNSUPPORTED | 34 spec tables unhandled (PROJCOST, FINDATES, MEMOTYPE, WBSMEMO, TASKFIN, TRSRCFIN, …) — OK for a project-focused parser, but should be documented |

Full field-level diff cached in `~/.hermes/cache/scratch/xerspec/spec_fields.json`.

## 5. PERFORMANCE

Benchmark: synthetic 32 MB XER, 270k rows (50k TASK, 100k TASKPRED, 100k TASKRSRC, 20k PROJWBS).

- **Baseline: 4.3–4.7 s, 417 MiB peak RSS**, 42.5M function calls.
- Second parse in same process: +400 MiB (the `obj_list` leak) and stale lists slow every scan.
- Hot spots: `locale.atof` ×1M calls (51 sites; each does localeconv + regex), `datetime.strptime` ×333k (~25% of profile), `Calendar.find_by_id` full-list scan **per task row**, 26-way `elif` per record.
- **Fixed branch exists**: `/tmp/pyp6xer-perf` (branch `perf-fixes`, commit c1be89d; your repo untouched). `locale.atof`→`float`, `strptime`→`fromisoformat`, dispatch dict, early-exit calendar lookup. **2.1× faster (2.0–2.3 s), 36/36 tests pass.** One deliberate revert: `Project.add_date` keeps strict `strptime` (date-only input must stay invalid).

## 6. RECOMMENDED FIX ORDER

1. **Now (correctness):** the 7 wrong-source assignments; `encoding='cp1252'` fallback (or chardet) + skip blank rows + `quoting=csv.QUOTE_NONE`; instance-level registries replacing class-level `obj_list`; writer: emit ROLES/ROLERATE/RCATTYPE/RCATVAL/RSRCRCAT and preserve ERMHDR.
2. **DCMA14:** fix check #5 codes, guard None dates/zero divisions, implement #12–#14, fix the invalid-dates denominator.
3. **Adopt the perf branch** (2.1×, tests green) — merge after items 1 so the fixes apply to the new code.
4. **Tests:** every finding above has a repro script (`~/.hermes/cache/scratch/probe1–5*.py`) — promote them to pytest cases; the existing suite covers none of these paths.
