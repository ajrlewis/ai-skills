#!/usr/bin/env python3
"""Compute a reviewer-friendly semantic diff between two JSON documents."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


@dataclass
class Discrepancy:
    """Represents a semantic difference between two JSON values."""

    path: str
    kind: str
    expected: Any
    actual: Any
    note: str


def _normalize_string(value: str) -> str:
    """Collapse whitespace for more useful string comparisons."""

    return " ".join(value.split())


def _to_decimal(value: Any) -> Decimal | None:
    """Parse a value as Decimal when it behaves like a number."""

    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))
    if not isinstance(value, str):
        return None
    candidate = value.strip().replace(",", "").replace("$", "").replace("%", "")
    if not candidate:
        return None
    try:
        return Decimal(candidate)
    except InvalidOperation:
        return None


def _compare_scalars(path: str, expected: Any, actual: Any) -> list[Discrepancy]:
    if isinstance(expected, str) and isinstance(actual, str):
        if _normalize_string(expected) == _normalize_string(actual):
            return []
    left_num = _to_decimal(expected)
    right_num = _to_decimal(actual)
    if left_num is not None and right_num is not None and left_num == right_num:
        return []
    if expected == actual:
        return []
    return [
        Discrepancy(
            path=path,
            kind="value_mismatch",
            expected=expected,
            actual=actual,
            note="Scalar values differ after normalization.",
        )
    ]


def _sort_key_for_scalar(value: Any) -> str:
    if isinstance(value, str):
        return _normalize_string(value).casefold()
    numeric = _to_decimal(value)
    if numeric is not None:
        return f"num:{numeric}"
    return json.dumps(value, sort_keys=True, default=str)


def _list_identity(item: Any) -> str | None:
    if not isinstance(item, dict):
        return None
    for key in ("number", "name", "id", "key"):
        value = item.get(key)
        if value not in (None, ""):
            return f"{key}:{value}"
    return None


def compare_values(expected: Any, actual: Any, path: str = "$") -> list[Discrepancy]:
    """Compare two JSON-like values recursively."""

    if isinstance(expected, dict) and isinstance(actual, dict):
        discrepancies: list[Discrepancy] = []
        for key in sorted(expected.keys() - actual.keys()):
            discrepancies.append(
                Discrepancy(
                    path=f"{path}.{key}",
                    kind="missing_in_actual",
                    expected=expected[key],
                    actual=None,
                    note="Key present in expected JSON but missing in actual JSON.",
                )
            )
        for key in sorted(actual.keys() - expected.keys()):
            discrepancies.append(
                Discrepancy(
                    path=f"{path}.{key}",
                    kind="unexpected_in_actual",
                    expected=None,
                    actual=actual[key],
                    note="Key present in actual JSON but not in expected JSON.",
                )
            )
        for key in sorted(expected.keys() & actual.keys()):
            discrepancies.extend(compare_values(expected[key], actual[key], f"{path}.{key}"))
        return discrepancies

    if isinstance(expected, list) and isinstance(actual, list):
        if all(_list_identity(item) for item in expected + actual):
            expected_map = {_list_identity(item): item for item in expected}
            actual_map = {_list_identity(item): item for item in actual}
            discrepancies: list[Discrepancy] = []
            for key in sorted(expected_map.keys() | actual_map.keys()):
                subpath = f"{path}[{key}]"
                if key not in actual_map:
                    discrepancies.append(
                        Discrepancy(
                            path=subpath,
                            kind="missing_in_actual",
                            expected=expected_map[key],
                            actual=None,
                            note="Object missing from actual list.",
                        )
                    )
                    continue
                if key not in expected_map:
                    discrepancies.append(
                        Discrepancy(
                            path=subpath,
                            kind="unexpected_in_actual",
                            expected=None,
                            actual=actual_map[key],
                            note="Unexpected object present in actual list.",
                        )
                    )
                    continue
                discrepancies.extend(compare_values(expected_map[key], actual_map[key], subpath))
            return discrepancies

        if all(not isinstance(item, (dict, list)) for item in expected + actual):
            left = sorted((_sort_key_for_scalar(item), item) for item in expected)
            right = sorted((_sort_key_for_scalar(item), item) for item in actual)
            if [item[0] for item in left] == [item[0] for item in right]:
                return []

        discrepancies = []
        max_len = max(len(expected), len(actual))
        for index in range(max_len):
            subpath = f"{path}[{index}]"
            if index >= len(expected):
                discrepancies.append(
                    Discrepancy(
                        path=subpath,
                        kind="unexpected_in_actual",
                        expected=None,
                        actual=actual[index],
                        note="Actual list contains an unexpected extra item.",
                    )
                )
                continue
            if index >= len(actual):
                discrepancies.append(
                    Discrepancy(
                        path=subpath,
                        kind="missing_in_actual",
                        expected=expected[index],
                        actual=None,
                        note="Actual list is missing an expected item.",
                    )
                )
                continue
            discrepancies.extend(compare_values(expected[index], actual[index], subpath))
        return discrepancies

    return _compare_scalars(path, expected, actual)


def build_summary(expected: Any, actual: Any) -> dict[str, Any]:
    """Return a machine-readable summary suitable for tests or reports."""

    discrepancies = compare_values(expected, actual)
    counts: dict[str, int] = {}
    for item in discrepancies:
        counts[item.kind] = counts.get(item.kind, 0) + 1
    return {
        "match": not discrepancies,
        "discrepancy_count": len(discrepancies),
        "counts_by_kind": counts,
        "discrepancies": [asdict(item) for item in discrepancies],
    }


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", type=Path, help="Path to expected JSON file.")
    parser.add_argument("actual", type=Path, help="Path to actual JSON file.")
    args = parser.parse_args()

    summary = build_summary(_load_json(args.expected), _load_json(args.actual))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
