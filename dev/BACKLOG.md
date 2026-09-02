# Backlog

Forward-looking work for Collisions — feature ideas and deferred TODOs.
Started 2026-09-02, after the incremental MVC/OOD refactor wrapped up (that
completed log is archived in [REFACTOR.md](REFACTOR.md)).

## Ground rules (carried over from the refactor)

- One small, verifiable change at a time. Jim regression-tests manually in
  the app, then commits and pushes.
- Don't touch unrelated code in the same increment — log it here instead.
- Jim has a long Java background but is not a veteran Python developer.
  Flag un-Pythonic / Java-habit patterns when spotted (a brief mention in
  passing is enough), see also the standing note in the memory file.
- When starting a task here, move it to the Log section below with what
  changed and why once done.

## Tasks

### 1. Coalesce rapid slider drags

**Type:** feature (not refactor cleanup). **Status:** not started.
**Discussed:** 2026-08-27.

A slider drag much faster than a transformation can compute (physicist on
an ordinary laptop) currently runs — and redraws — one transformation per
slider tick, which looks jerky. Want: only run the transformation for the
latest value once the in-flight one finishes.

This is the goal the old `PostMediator` threading code was a broken attempt
at; that dead code was deleted 2026-09-02 (see REFACTOR.md log). Don't
resurrect it — it called Qt-touching code off the main thread, blocked the
caller anyway, and had inconsistent poll/timeout math.

**Recommended approach:** a Qt-idiomatic debounce — on each slide event,
stash the latest value and (re)start a single-shot `QTimer` (~100-150ms);
run the transformation only when the timer fires with no newer event since.
Stays on the main thread, no locks, no cross-thread widget access.

**Scope / design calls to make:**
- Apply this to the transformation-triggering
  `BoostParameterASliderUpdateHandler` path
  ([view/controls_view/slider.py](../view/controls_view/slider.py)). The
  coordination handlers (`SliderCoordinationUpdateHandler` /
  `FourVectorSliderUpdateHandler`, which just update sibling sliders)
  probably want to stay synchronous or the drag feels laggy — confirm by
  feel.
- `SliderUpdateHandler` currently has no `__init__` and its subclasses
  aren't `QObject`s. A bare `QTimer()` (no parent) works as long as the
  event loop is running; decide whether to give the handler a parent or
  keep it parentless.
- The `handle_slide_event` -> `post_value` return value is still an
  unused "was there a problem?" boolean (`TODO` in the code) — the debounce
  is a chance to decide whether to wire up the "revert the slider on a bad
  value" idea or drop the boolean.
- If the transformation itself turns out heavy enough to stall the event
  loop even once coalesced, that's the point to reach for a real
  `QThread` / `QThreadPool` worker that computes off-thread and reports
  back via a `Signal`, never touching widgets directly.

### 2. `Transformation` class(es) for `model/transformation.py`

**Type:** OOD. **Status:** idea only, not fleshed out.

Per [dev_notes.txt](dev_notes.txt) ("We need a Transformation(s) class
(es)"). [model/transformation.py](../model/transformation.py) is currently all
module-level functions (`set_up_config_data`, `handle_transformation`,
`transform`, `validate_vectors`, `check_for_errors`). The empty do-nothing
`Transformation` class that used to sit at the top of the file was deleted
2026-09-02 (zero references) so this starts from a clean slate.

Open questions before starting: what state would a `Transformation` object
actually hold (argument type, boost parameter, the vector pair?), does it
subsume `LightConeRapidityMatrixConfigurationData` or wrap it, and how does
it land in `TransformationController` without just being a namespace. Worth
a short design discussion with Jim first.

## Log

_(nothing completed yet)_
