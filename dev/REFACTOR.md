# MVC Refactor

> **ARCHIVAL — do not need to read on a fresh session.** This is the completed
> working log of the 2026-08-20 → 2026-09-02 incremental MVC/OOD refactor. All
> backlog items are fixed (see the Log below for what changed and why, useful if
> a regression points back here). Forward-looking work now lives in
> [BACKLOG.md](BACKLOG.md) (same folder).
>
> This file lived in the repo root until 2026-09-02; its many `[path](path)`
> links to source files are still written relative to the root, so they're one
> level off now (`view/...` should read `../view/...`). Left as-is deliberately
> — the file is archival and the paths are still readable.

Working log for the incremental refactor toward strict MVC. Started 2026-08-20,
completed 2026-09-02.

## Goal

Classic MVC with an independent controller layer — not PySide/PyQt's Model/View
framework (`QAbstractItemModel` etc.), which buries the controller inside the
view via delegates. Target boundary:

- **model/** — pure Python + numpy/sympy. No PySide6 imports, no Qt signals,
  no UI concerns. Owns physics/math and decisions derived from it.
- **view/** — widgets and layout only. Reads/displays state, forwards user
  input to a controller. Should not import `model` directly or branch on
  model-derived business decisions itself.
- **controller/** — mediates between view and model. Owns the decisions that
  currently leak into the view (e.g. which config/argument type to use).
- **app/** — application bootstrap/window chrome (`application.py`,
  `custom_title_bar.py`). Not a strict MVC layer itself, wires the others
  together.

## Ground rules for each increment

- One small, verifiable change per day.
- Jim regression-tests manually after each change, then commits and pushes.
- Don't touch unrelated code in the same increment, even if noticed in passing
  (log it here instead, under Backlog).
- Jim has a long Java background but is not a veteran Python developer.
  Proactively flag un-Pythonic patterns or Java-habit carryovers when
  spotted — e.g. needless getter/setter methods where a plain attribute or
  `@property` would do, manual loops where a comprehension/generator reads
  better, verbose null-style checks instead of truthiness/`is None`, or
  overuse of inheritance where duck typing or a plain function suffices.
  This applies whenever touching Python code here, not just during MVC/OOD
  increments — a brief mention in passing is enough, it doesn't need to
  become its own task unless Jim wants to act on it.

## Current state (as of 2026-08-20)

Checked import boundaries across the whole tree:

- `model/` imports nothing from `view/` or `controller/`, and no PySide6 —
  clean.
- `controller/` imports from `model/` only (`transformation_controller.py`,
  `experiment_controller.py`) — clean.
- `view/` no longer imports `model` directly anywhere (fixed 2026-08-21, see
  Log). `controller/` remains the only layer importing `model.util`.

## Backlog (violations found, not yet fixed)

Scope isn't limited to MVC boundary violations — general OOD issues noticed
along the way (poor encapsulation, misplaced responsibilities, God objects,
etc.) get logged here too, flagged as such.

Broader Pythonicness/design survey done 2026-08-24 (see Log). Items already
fixed and dropped from this list: getter/setter-heavy accessors (2026-08-25),
missing `match` default case (2026-08-26). Of what's still listed below: the
failure-signaling item (#5) had its sentinel/guard part fixed 2026-08-27; the
transformations dead-code item (#2) was fixed 2026-08-28; the
`step_2_uses_system_of_equations` dead-config item (#1) was fixed 2026-08-29.
See Log for each.

1. **Dead code / dead config — `step_2_uses_system_of_equations` front-end
   path** — *Fixed 2026-08-29 (see Log).* `config.step_2_uses_system_of_equations`
   was permanently `False`; deleted the flag, the front-end
   system-of-equations path (`BackgroundCalculations` / `WaitingPopup`, the
   third-vector dropdown UI), the `third_vector` plumbing it fed through
   `model.transformation`, the now-dead `model/transformations.py` +
   `solve_for_second_step_transformation_exp_2yT`, and both `scipy` and
   (already-unused) `sympy` from `requirements.txt`.
2. **Dead code — transformations code** — *Fixed 2026-08-28 (see Log).*
   Sprawl in the transformation-solving path:
   [model/transformation_solutions.py](model/transformation_solutions.py)
   imports `minkowski_dot`/`calculate_m_2` from `model.util` then immediately
   shadows them with local redefinitions; its
   `SecondStepTransformationEquationSystem` carries four abandoned solver
   methods (`find_exp_2yT`, `find_exp_2yT_numerical`, `find_exp_2yT_symbolic`,
   `find_exp_2yT_numerical_2`) alongside the one actually used in production
   (`find_exp_2yT_numerical_3`, and even that's only reached via a separate,
   leaner duplicate class in
   [model/transformations.py](model/transformations.py), not this file).
   [test/transformations_2.py](test/transformations_2.py) and
   [test/transformation_solutions_2.py](test/transformation_solutions_2.py)
   are further exploratory scratch copies with no `TestCase`. Also:
   [model/general_matrix.py](model/general_matrix.py) is 100% commented out —
   same transformation-matrix domain as the rest of this item.
3. **Dead code — use_threading** — *Dead code removed 2026-09-02 (see Log).*
   The unreachable threaded slider-update path (`PostMediator`,
   `use_threading`, the `threading.Lock`, `signal_post_stream_end`) in
   [view/controls_view/slider.py](view/controls_view/slider.py) was deleted
   — `use_threading=True` was never passed anywhere and the implementation
   was broken several ways (Qt-touching code called off the main thread;
   `start_thread` did `start()` then an immediate blocking `join()` and
   wasn't even called; `post_threaded` ran synchronously from
   `handle_slide_event` in a `while: sleep(1)` loop; poll cadence/timeout
   math inconsistent). The *coalescing feature* it was a stalled attempt at
   is now tracked in [BACKLOG.md](BACKLOG.md), not as a refactor backlog
   item.
4. **Not Pythonic-specific, general hygiene** — *Fixed 2026-09-01 (see Log).*
   `print()` used as ad hoc debug logging instead of the `logging` module:
   scattered through
   [model/transformation_solutions.py](model/transformation_solutions.py)
   (deleted 2026-08-28) and the `save_experiment` error path in
   [view/view.py:141](view/view.py#L141) (the `load_experiment` prints
   were removed 2026-08-29, see Log).
   `main.py`/`crash_handler.py` already set up
   `redirect_streams()`/`log_environment()`; routing these through `logging`
   is consistent with that. (Stray `print()`s outside this backlog's
   transformation/CSV scope remain in `view/transformations.py:40` and
   `view/controls_view/custom_menu_bar.py:98` — noted, not touched.)
5. **OOD** — No consistent failure-signaling convention across the codebase.
   Originally four conventions in play; fixed 2026-08-27 (see Log): the
   sentinel `None` at `model/transformation.py:51` never actually worked —
   it was unconditionally overwritten before anything downstream could read
   it as a failure signal — so it and its now-dead guard in `transform()`
   were removed. Two conventions remain, left as-is since they serve
   different needs rather than being inconsistent for no reason: an
   empty-list-means-ok convention (`check_for_errors`/`validate_vectors`,
   for reporting multiple independent pre-flight validation problems at
   once), and `(value, message)` tuples where `message` is `None` on
   success (the `exp_2yT` solvers, which must always return a usable
   value even on failure). The `SquareRootOfNegativeNumber` exception
   convention went away with #1 on 2026-08-28 — it lived only in the
   deleted `model/transformation_solutions.py`. Nothing left to address
   here.
6. **OOD / not Pythonic — `View.pre_treat_csv_data` and split CSV
   validation** — *Fixed 2026-08-31 (see Log).*
   [view/view.py:145](view/view.py#L145).
   `pre_treat_csv_data(data)` mutates the caller's list in place
   (`del data[0]`) and returns `None` — a Java out-parameter side effect;
   should return the header-stripped rows instead (e.g. `strip_header`
   returning `rows[1:]`). Its header-equality check
   (`data[0] == config.vector_fields`) also overlaps the separate
   first-row-width check in `load_experiment`
   ([view/view.py:161](view/view.py#L161)) — two half-checks in two
   places; a single `rows[0] == config.vector_fields` header check
   subsumes both. Latent fragility: relies on `config.vector_fields`
   staying a `list` (a tuple would make the `==` silently never match, so
   the header row leaks through as data). Also only the header row's
   width is validated — a good header with a malformed data row passes
   here and fails deeper. Split out of the 2026-08-29 `load_experiment`
   fix as its own increment.

The refactor backlog is now empty (all six items fixed). The
import-boundary check still holds: `model/` imports no `view`/`controller`
and no PySide6; `controller/` imports `model` only; `view/` has zero
direct `model` imports. Forward-looking work (feature ideas, remaining
TODOs) moved to [BACKLOG.md](BACKLOG.md) on 2026-09-02.

## Log

- 2026-09-02: Cleared the last of the backlog and both `build.txt` /
  empty-`Transformation`-class loose ends from backlog #1's fallout.
  - Backlog #3 (use_threading): deleted the unreachable threaded
    slider-update path from
    [view/controls_view/slider.py](view/controls_view/slider.py) — the
    `PostMediator` class, the `use_threading` constructor params on all
    four `SliderUpdateHandler` classes, the `threading.Lock`, the
    `use_threading` branch in `handle_slide_event`, `signal_post_stream_end`,
    and the `import threading` / `import time`. `use_threading=True` was
    never passed and the code was broken several ways (see backlog #3).
    Updated the one caller that passed the old positional `False`
    ([view/controls.py:57](view/controls.py#L57)). The coalescing feature
    this was a stalled attempt at is now recorded in
    [BACKLOG.md](BACKLOG.md), not the refactor backlog. Follow-on in the same pass: with
    the threaded path gone, `SliderUpdateHandler`'s `latest_value` /
    `previous_value` bookkeeping (and the `initial_value` ctor arg that
    fed it, threaded through all four handler classes and their three
    call sites) was dead — `previous_value` was written but never read,
    part of an unbuilt "revert the slider on a bad value" idea. Removed
    it; `SliderUpdateHandler` no longer needs an `__init__`. The revert
    intent is preserved as a one-line TODO on `post_value`'s return.
  - Loose end — empty `Transformation` class: deleted the do-nothing
    `class Transformation` from
    [model/transformation.py](model/transformation.py) (zero references
    anywhere). The module stays as top-level functions; if an OOD pass
    wraps them in a class later (per `dev_notes.txt`), it starts clean.
  - Loose end — `build.txt`: the `--exclude-module=PyQt5` flag was only
    ever needed for `sympy.plotting` (SymPy removed 2026-08-29; PyQt5 not
    installed). Dropped the flag and rewrote the note to say why, with a
    pointer to re-add it if a future PyInstaller run pulls PyQt5 in
    transitively.
  Ran the full suite (`.venv/Scripts/python.exe -m unittest discover -s
  test`): 15 tests, same 2 pre-existing failures
  (`test_basic_case_minkowski_Y_vec_lcc_out`,
  `test_basic_case_minkowski_Y_vec_mink_out`), no new failures. Import
  smoke test of `view.controls_view.slider`, `view.controls`,
  `model.transformation`, `controller.transformation_controller` clean.
  Not yet regression-tested manually — Jim to test in the app and
  commit/push.
  With this, the incremental MVC/OOD refactor is complete and this file is
  archival. Started [BACKLOG.md](BACKLOG.md) for forward-looking work; its
  first entry is the slider-drag coalescing feature (moved out of the old
  "Future feature ideas" section here). Added an ARCHIVAL banner at the top
  of this file.
- 2026-09-01: Fixed backlog #4 (`print()` → `logging`), scoped to the
  `save_experiment` error path in [view/view.py](view/view.py) — the only
  remaining site in this backlog's scope after
  `model/transformation_solutions.py` was deleted (2026-08-28) and the
  `load_experiment` prints were removed (2026-08-29). The two `except`
  arms there swallowed the failure with a bare `print()` and no user
  feedback — a save the user asked for could silently do nothing (same
  smell as the 2026-08-29 `load_experiment` fix, worse here since there
  was no dialog at all). Collapsed the redundant separate
  `FileNotFoundError` arm into `except (OSError, csv.Error)` (it's an
  `OSError` subclass), which now `logging.exception(...)`s for the crash
  log and shows the user a `QMessageBox.warning(self, "Save failed", ...)`
  — parented/modal, matching `load_experiment`'s "Open failed" box. Added
  `import logging` to [view/view.py](view/view.py). Ran the full suite
  (`.venv/Scripts/python.exe -m unittest discover -s test`): 15 tests,
  same 2 pre-existing failures (`test_basic_case_minkowski_Y_vec_lcc_out`,
  `test_basic_case_minkowski_Y_vec_mink_out`), no new failures. Import
  smoke test of `view.view` clean. Backlog is now down to #3
  (use_threading — deferred, `QTimer`-debounce approach recorded), plus
  the two `build.txt` / empty-`Transformation`-class loose ends from
  backlog #1's fallout. Not yet regression-tested manually — Jim to test
  in the app and commit/push.
- 2026-08-31: Fixed backlog #6 (`View.pre_treat_csv_data` / split CSV
  validation) in [view/view.py](view/view.py). Deleted `pre_treat_csv_data`
  — the Java out-parameter method that did `del data[0]` on the caller's
  list and returned `None`. Header stripping is now a plain `rows[1:]` slice
  at the one call site in `load_experiment`. Replaced the two half-checks
  (the header-equality check inside `pre_treat_csv_data` and the separate
  first-row-width check in `load_experiment`) with one `@staticmethod`
  `check_csv_rows(rows)` that returns a human-readable problem string or
  `None`: it checks the file is non-empty, the header row equals
  `config.vector_fields` exactly, there's at least one data row, and
  *every* data row has the expected width (was only the header's width) —
  reporting the first offending line number. Compares against
  `list(config.vector_fields)` so the check still works if `vector_fields`
  is ever changed to a tuple (the old `==` would have silently stopped
  matching, leaking the header through as data). `load_experiment` now
  shows that one message via `QMessageBox.warning` and returns early.
  Ran the full suite (`.venv/Scripts/python.exe -m unittest discover -s
  test`): 15 tests, same 2 pre-existing failures
  (`test_basic_case_minkowski_Y_vec_lcc_out`,
  `test_basic_case_minkowski_Y_vec_mink_out`), no new failures. Not yet
  regression-tested manually — Jim to test in the app and commit/push.
  Backlog is now down to #3 (use_threading — deferred, `QTimer`-debounce
  approach recorded) and #4 (`print()` → `logging`, now just the
  `save_experiment` error path since `transformation_solutions.py` was
  deleted), plus the two `build.txt` / empty-`Transformation`-class loose
  ends from backlog #1's fallout.
- 2026-08-20: Created this doc. Surveyed import boundaries between
  model/view/controller/app. Found violation #1 (view deciding
  `get_config_argument` itself); not yet fixed.
- 2026-08-21: Fixed violation #1. Added `get_config_argument` and
  `is_v_minus_y_argument_type` to `TransformationController`
  ([controller/transformation_controller.py](controller/transformation_controller.py)),
  with passthroughs on `ExperimentController`
  ([controller/experiment_controller.py](controller/experiment_controller.py))
  for the plot-canvas call site. Updated
  [view/experiment/widgets.py](view/experiment/widgets.py) and
  [view/plot_view/plot_canvas.py](view/plot_view/plot_canvas.py) to call the
  controller instead of `model.util` directly, and removed their now-unused
  `from model import util` imports. `view/` has zero direct `model` imports
  now.
- 2026-08-22: Fixed violation #2. `TimeM2SlidersCoordinator`
  ([view/controls_view/slider.py](view/controls_view/slider.py)) was
  computing physics directly — `calculate_m2` duplicated the existing
  `model.util.calculate_m_2` (minkowski_dot self-product), and `calculate_t`
  solved the inverse (t from m², x, y, z) with no model equivalent. Added
  `calculate_t_from_m_2_and_xyz` to
  [model/util.py](model/util.py), and `calculate_m2`/`calculate_t`
  passthroughs on `ControlsController`
  ([controller/controls_controller.py](controller/controls_controller.py)).
  `TimeM2SlidersCoordinator` now takes the controller in its constructor
  (wired from `SliderGroupFrame`, which already had it) and calls through it
  instead of computing locally; removed the two local methods. `view/` still
  has zero direct `model` imports. Surveyed for the next violation while
  here — found two more, logged above under Backlog rather than fixed in
  this increment. Not yet regression-tested — Jim to test and commit/push.
- 2026-08-23: Fixed the `View.save_experiment` double-write bug that was
  logged in the backlog. [view/view.py](view/view.py) wrote the CSV once
  inside a `try/except`, then again unconditionally right after, outside
  any exception handling — redundant on success, and on failure the second
  write repeated the same failing call uncaught. Removed the second,
  unguarded write. Not an MVC violation; picked as today's increment for
  being a clear, low-risk fix. The m2-slider-limits MVC violation remains
  in the backlog, unstarted.
  Separately (not the daily MVC increment), narrowed all 8 `except
  Exception` catches in the codebase after Jim asked about the Ruff
  `BLE001` ("blind except") warning: 6 narrowed to specific exception
  types ([view.py](view/view.py) I/O: `OSError`/`UnicodeError`/`csv.Error`;
  [model/transformation_solutions.py](model/transformation_solutions.py)
  solver fallbacks: `ValueError`/`TypeError`), 2 left deliberately blanket
  with a `# noqa: BLE001` and an explanatory comment since they're
  safety-net code that must never itself raise
  ([app/crash_application.py](app/crash_application.py)'s Qt `notify()`
  override, [crash_handler.py](crash_handler.py)'s own exception hook).
  Also added a standing ground rule (above): since Jim comes from Java and
  isn't a Python veteran, flag un-Pythonic/Java-habit patterns whenever
  they're noticed, not just during MVC/OOD-focused increments.
- 2026-08-24: Fixed the last backlogged violation.
  `TimeM2SlidersCoordinator.calculate_and_set_m2_slider_limits`
  ([view/controls_view/slider.py](view/controls_view/slider.py)) was
  deriving `m2_min`/`m2_max` from `x, y, z` and `config.t_max` directly in
  the view. Added `calculate_m2_slider_limits` to
  [model/util.py](model/util.py) (same pattern as the existing
  `calculate_t_from_m_2_and_xyz`), with a passthrough on
  `ControlsController`
  ([controller/controls_controller.py](controller/controls_controller.py)).
  The view method now just calls the controller and applies the returned
  range to the slider; removed its local math and the now-unused `import
  math`. `view/` still has zero direct `model` imports. Backlog is now
  empty — surveyed for new violations while here and found none; the
  import-boundary check (`model`/`controller` clean, `view` zero `model`
  imports) still holds across the whole tree. Not yet regression-tested —
  Jim to test and commit/push.
  Separately, at Jim's request, surveyed the whole codebase (~4400 lines
  across model/view/controller/app) for Pythonicness and general design
  issues beyond MVC boundaries. Found five, logged above under Backlog,
  ranked by impact. #1 (getter/setter-heavy accessors on `Collision`/
  `Experiment`) picked as the next increment.
- 2026-08-25: Fixed the getter/setter-heavy accessors on `Collision`
  ([model/collision.py](model/collision.py)) and `Experiment`
  ([model/experiment.py](model/experiment.py)). For each, sorted the
  existing `get_x()`/`set_x()` methods into three buckets and treated each
  differently rather than doing a blanket property conversion:
  - Trivial wrappers around an already-public attribute (e.g.
    `Collision.get_four_vectors()` returning `self.vectors`,
    `Experiment.get_collision()` returning `self.collision`,
    `Experiment.get_boost_parameter_A()`/`set_boost_parameter_A()` around
    `self.boost_parameter_A`) added no encapsulation the attribute didn't
    already have, so these were deleted outright and call sites updated to
    read/write the attribute directly.
  - Parameterless computed getters with no backing field, or delegations
    where a `()` call read as noise (`Experiment.get_particle_names()`,
    `Experiment.get_original_four_vectors()`,
    `Experiment.has_transformation()`) became `@property`. Followed the
    precedent already set by `Particle.four_vector`
    ([model/particle.py](model/particle.py)), which was already doing this
    correctly. `has_transformation` also now returns
    `self.transformed_collision is not None` instead of the collision
    object itself, so it's an actual bool rather than a truthy object.
  - Methods that take an argument to do a real lookup (`get_four_vector`,
    `get_original_four_vector`, `get_transformed_four_vector`) or that do
    real work per call (`get_original_vectors`, `get_vectors_column`,
    `get_vectors_spatial_columns`, `get_spatial_vectors_xyz`,
    `set_transformation`, `set_transformed_four_vectors`,
    `clear_transformation`) were left as ordinary methods — taking an
    argument or doing non-trivial work is a normal reason for a method to
    exist, not a Java-getter smell. `record_transformation_arguments`,
    only ever called internally, was renamed
    `_record_transformation_arguments` to mark it as an implementation
    detail.
  - Also deleted, while in the same two classes: `Collision.get_vectors()`
    (flagged in the backlog entry as an exact, unused duplicate of
    `get_four_vectors()`, both now gone) and four further methods found to
    be completely unused anywhere in the codebase —
    `Collision.get_particles()`, `Collision.get(name)`,
    `Collision.num_particles()`, and three-way-duplicated spatial-vector
    getters on `Experiment` (`get_original_spatial_vectors()`,
    `get_vectors_spatial_columns()` — identical body to the former — and
    `get_spatial_vectors()`), plus `Experiment.get_transformed_spatial_vectors()`.
    These are dead code rather than pure getter/setter style, bordering on
    backlog item #1 (dead code), but they were getter-named methods on the
    exact two classes this increment targeted, so cleaning them up here
    kept the fix in one place instead of splitting it across two
    increments.
  Updated all call sites across
  [controller/experiment_controller.py](controller/experiment_controller.py),
  [controller/transformation_controller.py](controller/transformation_controller.py),
  [controller/controls_controller.py](controller/controls_controller.py),
  [model/transformation.py](model/transformation.py),
  [view/experiment/widgets.py](view/experiment/widgets.py),
  [view/plot_view/plot_canvas.py](view/plot_view/plot_canvas.py), and
  [view/plot_view/plot_2D.py](view/plot_view/plot_2D.py). Also deleted the
  stale `# TODO: Pick one or the other of these names` comment in
  `experiment_controller.py` — it was flagging the
  `get_transformation_type`/`get_transformation_particle_pair_names`
  naming mismatch, which no longer exists now that both are just
  `experiment.argument_type` and `experiment.V_Y_particle_names`.
  Ran the full test suite (`python -m unittest discover -s test`) after the
  change: 17 tests, same 2 pre-existing failures as before
  (`test_basic_case_minkowski_Y_vec_lcc_out`,
  `test_basic_case_minkowski_Y_vec_mink_out` — pre-existing, unrelated to
  this change), no new failures. `view/` still has zero direct `model`
  imports.
  Not yet regression-tested manually — Jim to test in the app and
  commit/push. Backlog #2 (dead code sprawl) is next.
- 2026-08-26: Fixed the correctness-adjacent gap (former backlog #4).
  `set_up_config_data`'s `match argument_type` in
  [model/transformation.py](model/transformation.py) had no `case _:` — an
  unrecognized `argument_type` silently left `rest_frame_vector` as `None`,
  which would only surface later as an opaque `AssertionError` in
  `qcd_matrix.py`. Added `case _: raise ValueError(f"Unknown argument_type:
  {argument_type!r}")`, matching the structurally parallel `match` in
  `handle_transformation` (same file), which already raised this way. Not
  yet regression-tested — Jim to test and commit/push. Backlog #2 (dead
  code sprawl) remains next.
- 2026-08-27: Discussed backlog #3 (use_threading) with Jim without
  implementing — logged the recommended `QTimer`-debounce approach directly
  in that backlog entry (see above) for whenever it's picked up. Then fixed
  part of backlog #5 (OOD/failure-signaling), specifically the exact
  sentinel cited there:
  [model/transformation.py:51](model/transformation.py#L51) set
  `matrix_configuration_data.exp_2yT = None` with a comment claiming this
  signals failure, but it was unconditionally overwritten two lines later
  by the result of `solve_for_second_step_transformation_exp_2yT` — which,
  per its implementation in
  [model/transformations.py](model/transformations.py)
  (`find_exp_2yT_numerical_3`), always returns a usable float plus an
  optional warning message, never `None`. So the sentinel never actually
  fired downstream. `transform()`'s corresponding
  `if matrix_configuration_data.exp_2yT is not None:` guard was therefore
  dead code too, and was a *weaker* duplicate of the
  `assert self.exp_2yT is not None` already enforced inside
  `LightConeRapidityMatrixConfigurationData.calculate_calculated_values()`
  ([model/qcd_matrix.py:110](model/qcd_matrix.py#L110)), which
  `FourVectorTransformationMatrix.__init__` always calls
  ([model/four_vector_matrix.py:53](model/four_vector_matrix.py#L53)).
  Removed the dead sentinel assignment/comment and the now-always-true
  guard in `transform()`, unindenting its body. This leaves the codebase's
  two other failure-signaling conventions untouched (list-of-messages from
  `check_for_errors`/`validate_vectors`, and the `(value, message)` tuple
  from the `exp_2yT` solvers) — they serve genuinely different needs
  (multiple independent pre-flight checks vs. a solver that must always
  return a usable value), so "consistent" here meant removing the one
  mechanism that didn't actually work, not collapsing all three into one
  shape. The `SquareRootOfNegativeNumber` exception convention remains
  unaddressed, since it's only reachable from the dead code in backlog #1,
  not yet cleaned up. Ran the full suite
  (`.venv/Scripts/python.exe -m unittest discover -s test`): 17 tests, same
  2 pre-existing failures as before
  (`test_basic_case_minkowski_Y_vec_lcc_out`,
  `test_basic_case_minkowski_Y_vec_mink_out`), no new failures. Not yet
  regression-tested manually — Jim to test in the app and commit/push.
- 2026-08-28: Fixed backlog #1 (dead code — transformations code). Deleted
  four files:
  - [model/transformation_solutions.py](model/transformation_solutions.py) —
    the whole `SecondStepTransformationEquationSystem` class. Its five
    `find_exp_2yT*` solver variants were all dead: four abandoned outright,
    and the one production ever wanted (`find_exp_2yT_numerical_3`) is
    reached only through the leaner duplicate `TransformationEquationSystem`
    in [model/transformations.py](model/transformations.py) via
    `model.transformation.solve_for_second_step_transformation_exp_2yT`.
    This file was also the sole importer of `sympy` and the sole home of
    the `SquareRootOfNegativeNumber` exception (backlog #5's last loose
    end — now moot).
  - [model/general_matrix.py](model/general_matrix.py) — 100% commented out.
  - [test/transformations_2.py](test/transformations_2.py),
    [test/transformation_solutions_2.py](test/transformation_solutions_2.py) —
    scratch copies, no `TestCase`, not matched by `unittest discover`'s
    `test*.py` pattern so never run.
  Renamed `test/test_transformation_solutions.py` →
  [test/test_transformations.py](test/test_transformations.py) and
  retargeted both its cases at
  `model.transformations.TransformationEquationSystem.find_exp_2yT_numerical_3`
  (one previously called the now-deleted `find_exp_2yT()` symbolic solver).
  Tidied [model/transformations.py](model/transformations.py): dropped its
  local `minkowski_dot`/`calculate_m_2` redefinitions in favour of
  `from model.util import ...` (same bodies, removes the shadowing).
  Ran the full suite (`.venv/Scripts/python.exe -m unittest discover -s
  test`): 17 tests, same 2 pre-existing failures
  (`test_basic_case_minkowski_Y_vec_lcc_out`,
  `test_basic_case_minkowski_Y_vec_mink_out`), no new failures; suite is
  much faster now that the slow sympy `solve()` path is gone. `sympy` is
  now unreferenced anywhere in the tree and can be dropped from
  `requirements.txt`. `scipy` stays: [model/transformations.py](model/transformations.py)
  still imports `scipy.optimize.fsolve` at module load and sits on the live
  `model.transformation` import path, even though with
  `step_2_uses_system_of_equations = False` the call is never reached at
  runtime — removing it is folded into backlog #1 (dead code / dead
  config), since renumbered to the top of the list. Left
  `requirements.txt` untouched today per Jim's instruction (pathway still
  standing). Also noticed but not touched (would be scope creep):
  `model/transformations.py`'s `find_exp_2yT_numerical_3` clamps to a
  magic `10` while its message quotes `config.boost_A_max` — flagged for a
  later pass. Not yet regression-tested manually — Jim to test in the app
  and commit/push.
- 2026-08-29: Fixed backlog #1 (dead code / dead config —
  `step_2_uses_system_of_equations`). The flag
  ([config.py](config.py)) had been permanently `False`, gating an
  abandoned "solve a system of equations for the second-step boost
  parameter" front end. Removed end to end:
  - `config.step_2_uses_system_of_equations` deleted.
  - [view/plot_view/plot_canvas.py](view/plot_view/plot_canvas.py): the
    `is_v_minus_y_argument_type(...) and config.step_2_uses_system_of_equations`
    branch collapsed to its `else` body (the direct
    `create_initial_transformation(...)` call); dropped the
    `BackgroundCalculations`/`WaitingPopup` imports and the third entry
    (`transformation_config["third_vector"]`) from `particles_names_picked`.
  - [view/transformations_view/widgets.py](view/transformations_view/widgets.py):
    deleted `BackgroundCalculations` (`QThread`) and `WaitingPopup`
    (`QProgressBar` "solving system of equations…" dialog), and the
    third-vector dropdown machinery in `AbstractTransformationPopup` —
    `post_transformation_check`, `particle_names_combo_box_activated`,
    `get_combobox_names`, `update_submit_buttons_state`, and the
    `particle_names_combo_box`/`third_vector_label` widgets built in
    `create_argument_type_checkboxes` (which loses its `all_particle_names`
    param). The `(V' - Y', Y)` checkbox / `V_MINUS_Y` argument type stays —
    it just always uses the default `config.exp_2yT` boost now.
    `ConfigureTransformationPopup` loses its `get_combobox_names` /
    `update_submit_buttons_state` overrides and the
    `transformation_config["third vector"]`/`["third_vector"]` entries.
  - [view/experiment/widgets.py](view/experiment/widgets.py) (`VectorIssueCheck`):
    deleted the `update_third_vector_combobox` method + its call, and the
    now-orphaned `get_combobox_names` override.
  - [model/transformation.py](model/transformation.py): dropped the
    `third_vector` param from `set_up_config_data`/`transform`/
    `handle_transformation`/`validate_vectors` and the
    `TransformationEquationSystem` import; deleted
    `solve_for_second_step_transformation_exp_2yT`. The `V_MINUS_Y` case in
    `set_up_config_data` collapses to just setting `rest_frame_vector` (the
    `exp_2yT` default was already applied at the top of the function).
  - [controller/transformation_controller.py](controller/transformation_controller.py) /
    [controller/experiment_controller.py](controller/experiment_controller.py):
    removed the `third_vector` plumbing through `unpack_vector_arguments`
    (no longer returns it), `handle_transformation`, `validate_vectors`,
    `pre_check_transformation`, `plot_transformation`; removed the
    `background_thread_preparation` param (only `BackgroundCalculations`
    ever passed it) and the orphaned `is_v_minus_y_argument_type`
    passthroughs.
  - Deleted [model/transformations.py] (only reachable via the removed
    `solve_for_second_step_transformation_exp_2yT`; sole importer of
    `scipy.optimize.fsolve`) and `test/test_transformations.py` (tested only
    that module).
  - `requirements.txt`: dropped `scipy` and `sympy` (both now unreferenced
    tree-wide).
  Ran the full suite (`.venv/Scripts/python.exe -m unittest discover -s
  test`): 15 tests (was 17; the 2 removed were the deleted
  `test_transformations.py` cases), same 2 pre-existing failures
  (`test_basic_case_minkowski_Y_vec_lcc_out`,
  `test_basic_case_minkowski_Y_vec_mink_out`), no new failures. Import smoke
  test of the app modules clean. Not yet regression-tested manually — Jim to
  test in the app and commit/push.
  Noticed, not touched (scope): `boost_default_set_message` /
  `failure_message` returned by `set_up_config_data` → `transform` →
  `handle_transformation` is now always `None` (the `exp_2yT` solver was its
  only non-`None` source), so the `if not failure_message:` guards on that
  path in the controllers are now always true — a follow-on cleanup, same
  shape as the 2026-08-27 sentinel removal. *Done 2026-08-30 (see Log).*
  Also `build.txt`'s
  `--exclude-module=PyQt5` note is now stale (it was needed because of
  `sympy.plotting`). And `model.transformation.Transformation` is still an
  empty do-nothing class.
- 2026-08-29 (2nd change): Reworked `View.load_experiment`
  ([view/view.py:149](view/view.py#L149)) after a review flagged
  backlog #4/#5 smells there. Fixed a real bug: the `except` handlers only
  `print()`d with no `return`, so an I/O/decode failure fell through to
  the column-count check and showed the user a misleading *"file does not
  have 5 columns"* dialog instead of the actual read error. Now the read
  is done inside the `try`, both error paths and the wrong-column-count
  path all report via `QMessageBox.warning(self, ...)` (was `None` parent
  in one spot — a parentless box isn't centered/modal against the
  window), and failures `return` early. Swept up in the same lines:
  dropped the redundant separate `FileNotFoundError` handler (it's an
  `OSError` subclass, now caught and shown properly); `data = None` +
  populate-inside-`try` collapsed to a single assignment; `open(...,
  mode="r")` → `open(..., newline="")` (drops the redundant default mode,
  adds the `newline=""` the `csv` reader wants, matching
  `save_experiment`); message string concatenation → f-string; removed
  the `if file_path:` nesting via early return. `pre_treat_csv_data` and
  the split CSV validation left untouched — logged as backlog #6 for its
  own increment. Not yet regression-tested manually — Jim to test in the
  app and commit/push.
- 2026-08-30: Follow-on dead-code cleanup from backlog #1 — removed the
  now-always-`None` `failure_message` / `boost_default_set_message` thread
  that used to carry the `exp_2yT`-solver warning up from the model. Since
  that solver went with backlog #1 on 2026-08-29, nothing downstream can
  ever be non-`None` here, so:
  - [model/transformation.py](model/transformation.py): `set_up_config_data`
    drops its `boost_default_set_message` local and returns just
    `matrix_configuration_data` (was a 2-tuple); `transform` returns
    `(transformed_vectors, exp_2yT)` (was a 3-tuple); `handle_transformation`
    returns `(transformed_vectors, boost_parameter_A_used)` (was a 3-tuple)
    and loses its `failure_message` local. Unpacking updated at the five
    internal `transform(...)` call sites (`_` tuple slots dropped).
  - [controller/transformation_controller.py](controller/transformation_controller.py):
    `handle_transformation` returns just `boost_parameter_A_used`; the
    always-true `if not failure_message:` guard around `set_transformation`
    is gone (call is now unconditional). Also deleted the stale
    commented-out `retransform_experiment_vectors` block below
    `transformation_exists` — it referenced two already-removed APIs
    (`get_transformation_type`, the old `handle_transformation` signature).
  - [controller/experiment_controller.py](controller/experiment_controller.py):
    `plot_transformation` returns just `boost_parameter_A_used` and calls
    `plot_transformed_experiment_vectors` unconditionally (guard dropped);
    `create_initial_transformation` no longer returns anything (its only
    value was the dead `failure_message`).
  - [view/plot_view/plot_canvas.py](view/plot_view/plot_canvas.py): dropped
    the `failure_message = create_initial_transformation(...)` capture and
    the dead `if failure_message: transformation_issue_popup(...)` branch
    after it. The pre-check `results` popup path just above it is untouched.
  - [view/experiment/widgets.py](view/experiment/widgets.py):
    `transformation_issue_popup` loses its now-unused `failure_message`
    param and the corresponding first `if` branch. Its `axis`/`value`
    params are also currently dead (the `get_slider_transformation_issue_popup`
    caller was commented out in an earlier commit) but left alone — that's a
    separate slider-path thread, overlaps backlog #3.
  Ran the full suite (`.venv/Scripts/python.exe -m unittest discover -s
  test`): 15 tests, same 2 pre-existing failures
  (`test_basic_case_minkowski_Y_vec_lcc_out`,
  `test_basic_case_minkowski_Y_vec_mink_out`), no new failures. Import smoke
  test of model/controller/view modules clean. Still open from backlog #1's
  fallout: `build.txt`'s stale `--exclude-module=PyQt5` note, and the empty
  do-nothing `model.transformation.Transformation` class. Not yet
  regression-tested manually — Jim to test in the app and commit/push.
