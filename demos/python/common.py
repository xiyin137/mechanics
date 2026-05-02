"""Shared helpers for mechanics demo scripts.

The helpers in this file are intentionally small.  Each demo should remain
readable as a standalone teaching script, while still sharing one convention
for JSON diagnostics and output paths.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Callable

try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - import-time fallback for help text.
    np = None  # type: ignore[assignment]


def json_ready(value: Any) -> Any:
    """Convert NumPy-heavy demo outputs into strict JSON values."""

    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if np is not None:
        if isinstance(value, np.ndarray):
            return json_ready(value.tolist())
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.floating):
            value = float(value)
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else value
    if isinstance(value, Path):
        return str(value)
    return value


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(json_ready(data), handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")


def add_output_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="print a machine-readable JSON summary instead of text")
    parser.add_argument("--json-output", type=Path, default=None, help="write a machine-readable JSON summary")
    parser.add_argument("--output-dir", type=Path, default=None, help="write standard outputs to this directory")


def add_preset_args(parser: argparse.ArgumentParser, *, include_long: bool = True) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--quick", action="store_true", help="short classroom/smoke-test configuration unless overridden")
    group.add_argument("--lecture", action="store_true", help="moderate lecture-demo configuration unless overridden")
    if include_long:
        group.add_argument("--long", action="store_true", help="larger project-scale configuration unless overridden")


def fill_defaults(args: argparse.Namespace, defaults: dict[str, Any]) -> None:
    for key, value in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, value)


def configure_standard_outputs(
    args: argparse.Namespace,
    *,
    stem: str,
    plot_name: str | None = None,
) -> None:
    """Populate JSON and plot outputs when ``--output-dir`` is used."""

    if getattr(args, "output_dir", None) is None:
        return
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if getattr(args, "json_output", None) is None:
        args.json_output = args.output_dir / f"{stem}.json"
    if plot_name is not None and getattr(args, "plot", None) is None:
        args.plot = args.output_dir / plot_name


def emit_summary(
    summary: dict[str, Any],
    args: argparse.Namespace,
    text_printer: Callable[[dict[str, Any]], None],
) -> None:
    """Write JSON outputs and then print either JSON or the human report."""

    outputs = summary.setdefault("outputs", {})
    if getattr(args, "plot", None) is not None:
        outputs["plot"] = str(args.plot)
    if getattr(args, "json_output", None) is not None:
        outputs["json"] = str(args.json_output)
        write_json(args.json_output, summary)

    if getattr(args, "json", False):
        print(json.dumps(json_ready(summary), indent=2, sort_keys=True, allow_nan=False))
    else:
        text_printer(summary)
        if getattr(args, "plot", None) is not None:
            print(f"wrote_plot={args.plot}")
        if getattr(args, "json_output", None) is not None:
            print(f"wrote_json={args.json_output}")
