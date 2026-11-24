#!/usr/bin/env python3
"""Initialize, validate, summarize, authorize, and checkpoint pentest state."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "2.0"
PATH_STATUSES = {"active", "deep_dive", "parked", "closed"}
SCOPE_STATUSES = {"draft", "confirmed"}
AUTONOMY_LEVELS = {"L0", "L1", "L2"}
REQUIRED_TOP_LEVEL = {
    "schema_version", "engagement_id", "objective", "scope", "authorization_profile",
    "context", "domain_context", "module_stack", "observations", "assets",
    "credential_refs", "findings", "attack_paths", "actions", "blockers",
    "persistent_changes", "artifacts", "next_decision", "last_updated",
}
REQUIRED_OBSERVATIONS = {"facts", "inferences", "hypotheses", "unknowns", "rejected"}
SECRET_KEYS = {
    "password", "passwd", "secret", "token", "token_value", "api_key",
    "private_key", "raw_hash", "credential",
}
OBSERVATION_KEYS = {
    "fact": "facts",
    "inference": "inferences",
    "hypothesis": "hypotheses",
    "unknown": "unknowns",
    "rejected": "rejected",
}
CONFIDENCE_LEVELS = ("confirmed", "high", "medium", "low")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def parse_levels(value: str) -> list[str]:
    levels = [item.strip().upper() for item in value.split(",") if item.strip()]
    invalid = sorted(set(levels) - AUTONOMY_LEVELS)
    if invalid:
        raise ValueError(f"invalid autonomous levels: {', '.join(invalid)}")
    return list(dict.fromkeys(levels))


def new_state(
    engagement_id: str,
    objective: str,
    domain: str,
    scope_status: str,
    autonomous_levels: list[str] | None = None,
) -> dict[str, Any]:
    if autonomous_levels is None:
        autonomous_levels = ["L0"] if scope_status == "draft" else ["L0", "L1"]
    return {
        "schema_version": SCHEMA_VERSION,
        "engagement_id": engagement_id,
        "objective": objective,
        "scope": {"status": scope_status, "assets": [], "exclusions": [], "constraints": []},
        "authorization_profile": {
            "autonomous_levels": autonomous_levels,
            "approved_action_classes": [],
            "excluded_actions": [],
            "scale_limits": {},
            "stop_conditions": [],
            "approvals": [],
        },
        "context": {
            "domain": domain,
            "phase": "initialization",
            "current_access": [],
            "network_position": [],
            "controls": [],
        },
        "domain_context": {
            "primary_domain": domain,
            "supporting_domains": [],
            "transition_reason": "",
            "return_target": "",
        },
        "module_stack": [],
        "observations": {
            "facts": [], "inferences": [], "hypotheses": [], "unknowns": [], "rejected": [],
        },
        "assets": [],
        "credential_refs": [],
        "findings": [],
        "attack_paths": [],
        "actions": [],
        "blockers": [],
        "persistent_changes": [],
        "artifacts": [],
        "next_decision": {},
        "last_updated": now_iso(),
    }


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"state file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError("state root must be a JSON object")
    return data


def validate_state(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - data.keys())
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    for field in ("engagement_id", "objective"):
        if not isinstance(data.get(field), str) or not data.get(field, "").strip():
            errors.append(f"{field} must be a non-empty string")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        errors.append("scope must be an object")
    else:
        if scope.get("status") not in SCOPE_STATUSES:
            errors.append(f"scope.status must be one of {sorted(SCOPE_STATUSES)}")
        for field in ("assets", "exclusions", "constraints"):
            if not isinstance(scope.get(field), list):
                errors.append(f"scope.{field} must be a list")

    authorization = data.get("authorization_profile")
    if not isinstance(authorization, dict):
        errors.append("authorization_profile must be an object")
    else:
        levels = authorization.get("autonomous_levels")
        if not isinstance(levels, list):
            errors.append("authorization_profile.autonomous_levels must be a list")
        elif not set(levels).issubset(AUTONOMY_LEVELS):
            errors.append(f"authorization_profile.autonomous_levels must use {sorted(AUTONOMY_LEVELS)}")
        for field in ("approved_action_classes", "excluded_actions", "stop_conditions", "approvals"):
            if not isinstance(authorization.get(field), list):
                errors.append(f"authorization_profile.{field} must be a list")
        if not isinstance(authorization.get("scale_limits"), dict):
            errors.append("authorization_profile.scale_limits must be an object")

    context = data.get("context")
    if not isinstance(context, dict):
        errors.append("context must be an object")
    else:
        for field in ("domain", "phase"):
            if not isinstance(context.get(field), str) or not context.get(field, "").strip():
                errors.append(f"context.{field} must be a non-empty string")
        for field in ("current_access", "network_position", "controls"):
            if not isinstance(context.get(field), list):
                errors.append(f"context.{field} must be a list")

    domain_context = data.get("domain_context")
    if not isinstance(domain_context, dict):
        errors.append("domain_context must be an object")
    else:
        if not isinstance(domain_context.get("primary_domain"), str) or not domain_context.get("primary_domain", "").strip():
            errors.append("domain_context.primary_domain must be a non-empty string")
        if not isinstance(domain_context.get("supporting_domains"), list):
            errors.append("domain_context.supporting_domains must be a list")
        for field in ("transition_reason", "return_target"):
            if not isinstance(domain_context.get(field), str):
                errors.append(f"domain_context.{field} must be a string")

    stack = data.get("module_stack")
    if not isinstance(stack, list):
        errors.append("module_stack must be a list")
    else:
        for index, frame in enumerate(stack):
            if not isinstance(frame, dict):
                errors.append(f"module_stack[{index}] must be an object")
                continue
            for field in ("module_id", "parent_path", "objective", "return_target", "called_at"):
                if not isinstance(frame.get(field), str) or not frame.get(field, "").strip():
                    errors.append(f"module_stack[{index}].{field} must be a non-empty string")

    observations = data.get("observations")
    if not isinstance(observations, dict):
        errors.append("observations must be an object")
    else:
        missing_observations = sorted(REQUIRED_OBSERVATIONS - observations.keys())
        if missing_observations:
            errors.append(f"missing observation classes: {', '.join(missing_observations)}")
        for field in REQUIRED_OBSERVATIONS:
            if field in observations and not isinstance(observations[field], list):
                errors.append(f"observations.{field} must be a list")

    for field in ("assets", "credential_refs", "findings", "attack_paths", "actions", "blockers", "persistent_changes", "artifacts"):
        if field in data and not isinstance(data[field], list):
            errors.append(f"{field} must be a list")

    for index, path in enumerate(data.get("attack_paths", [])):
        if not isinstance(path, dict):
            errors.append(f"attack_paths[{index}] must be an object")
            continue
        if path.get("status") not in PATH_STATUSES:
            errors.append(f"attack_paths[{index}].status must be one of {sorted(PATH_STATUSES)}")
        if not path.get("id"):
            errors.append(f"attack_paths[{index}].id is required")

    for index, reference in enumerate(data.get("credential_refs", [])):
        if not isinstance(reference, dict):
            errors.append(f"credential_refs[{index}] must be an object")
            continue
        exposed = sorted(SECRET_KEYS.intersection(key.lower() for key in reference))
        if exposed:
            errors.append(f"credential_refs[{index}] contains secret-like fields: {', '.join(exposed)}; store references only")

    if "next_decision" in data and not isinstance(data["next_decision"], dict):
        errors.append("next_decision must be an object")
    timestamp = data.get("last_updated")
    if not isinstance(timestamp, str):
        errors.append("last_updated must be an ISO-8601 string")
    else:
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            errors.append("last_updated must be a valid ISO-8601 timestamp")
    return errors


def write_state(path: Path, data: dict[str, Any], overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        raise ValueError(f"refusing to overwrite existing state: {path}; use --force")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_checked(path: Path, data: dict[str, Any], backup: bool = False) -> None:
    errors = validate_state(data)
    if errors:
        raise ValueError("invalid state: " + "; ".join(errors))
    if backup:
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    data["last_updated"] = now_iso()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_init(args: argparse.Namespace) -> int:
    if args.scope_status == "confirmed" and not args.authorization_ref:
        raise ValueError(
            "--scope-status confirmed requires --authorization-ref "
            "(ticket, authorization letter, or email id); scope cannot be self-confirmed"
        )
    levels = parse_levels(args.autonomous_levels) if args.autonomous_levels else None
    state = new_state(args.engagement_id, args.objective, args.domain, args.scope_status, levels)
    if args.authorization_ref:
        state["scope"]["authorization_ref"] = args.authorization_ref
    if args.scope_root:
        state["scope_root"] = args.scope_root
    write_state(args.path, state, args.force)
    print(f"initialized {args.path}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_state(load_state(args.path))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"valid state: {args.path}")
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    errors = validate_state(data)
    if errors:
        print("state is invalid; run validate for details", file=sys.stderr)
        return 1
    path_counts = {status: 0 for status in sorted(PATH_STATUSES)}
    for path in data["attack_paths"]:
        path_counts[path["status"]] += 1
    summary = {
        "engagement_id": data["engagement_id"], "objective": data["objective"],
        "scope_status": data["scope"]["status"],
        "autonomous_levels": data["authorization_profile"]["autonomous_levels"],
        "primary_domain": data["domain_context"]["primary_domain"],
        "supporting_domains": data["domain_context"]["supporting_domains"],
        "module_depth": len(data["module_stack"]), "phase": data["context"]["phase"],
        "facts": len(data["observations"]["facts"]), "hypotheses": len(data["observations"]["hypotheses"]),
        "findings": len(data["findings"]), "attack_paths": path_counts,
        "blockers": len(data["blockers"]), "persistent_changes": len(data["persistent_changes"]),
        "last_updated": data["last_updated"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def cmd_authorize(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    profile = data.get("authorization_profile")
    if not isinstance(profile, dict):
        raise ValueError("state has no valid authorization_profile")
    if args.levels:
        profile["autonomous_levels"] = parse_levels(args.levels)
    for field, values in (
        ("approved_action_classes", args.approve_action),
        ("excluded_actions", args.exclude_action),
        ("stop_conditions", args.stop_condition),
    ):
        profile[field] = list(dict.fromkeys([*profile.get(field, []), *values]))
    save_checked(args.path, data, args.backup)
    print(f"updated authorization profile: {args.path}")
    return 0


def cmd_push_module(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    data["module_stack"].append({
        "module_id": args.module_id, "parent_path": args.parent_path,
        "objective": args.objective, "return_target": args.return_target,
        "called_at": now_iso(),
    })
    if args.supporting_domain and args.supporting_domain not in data["domain_context"]["supporting_domains"]:
        data["domain_context"]["supporting_domains"].append(args.supporting_domain)
    save_checked(args.path, data, args.backup)
    print(f"pushed module {args.module_id}: depth={len(data['module_stack'])}")
    return 0


def cmd_pop_module(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    if not data["module_stack"]:
        raise ValueError("module_stack is empty")
    top = data["module_stack"][-1]
    if args.module_id and top["module_id"] != args.module_id:
        raise ValueError(f"top module is {top['module_id']!r}, not {args.module_id!r}")
    data["module_stack"].pop()
    save_checked(args.path, data, args.backup)
    print(f"popped module {top['module_id']}: depth={len(data['module_stack'])}")
    return 0


def cmd_checkpoint(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    save_checked(args.path, data, args.backup)
    print(f"checkpointed {args.path}")
    return 0


def find_path(data: dict[str, Any], path_id: str) -> dict[str, Any]:
    for record in data.get("attack_paths", []):
        if isinstance(record, dict) and record.get("id") == path_id:
            return record
    raise ValueError(f"attack path not found: {path_id}")


def cmd_fact(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    bucket = OBSERVATION_KEYS[args.observation_class]
    records = data["observations"].setdefault(bucket, [])
    record: dict[str, Any] = {
        "statement": args.statement,
        "source": args.source,
        "class": args.observation_class,
        "confidence": args.confidence,
        "recorded_at": now_iso(),
    }
    if args.asset:
        record["assets"] = list(args.asset)
    records.append(record)
    save_checked(args.path, data, args.backup)
    print(f"recorded {args.observation_class} #{len(records)}: {args.statement[:70]}")
    return 0


def cmd_path(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    paths = data.setdefault("attack_paths", [])
    record = next((p for p in paths if isinstance(p, dict) and p.get("id") == args.id), None)
    if record is None:
        record = {"id": args.id}
        paths.append(record)
    record.update({
        "title": args.title,
        "status": args.status,
        "next_action": args.next_action,
        "updated_at": now_iso(),
    })
    if args.parent_path:
        record["parent_path"] = args.parent_path
    if args.value:
        record["value"] = args.value
    save_checked(args.path, data, args.backup)
    print(f"path {args.id}: {args.status}")
    return 0


def cmd_park(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    record = find_path(data, args.id)
    record["status"] = "parked"
    record["reactivation_condition"] = args.reactivation_condition
    record["updated_at"] = now_iso()
    save_checked(args.path, data, args.backup)
    print(f"parked {args.id}: reactivate when {args.reactivation_condition}")
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    record = find_path(data, args.id)
    record["status"] = args.status
    record.setdefault("supporting_evidence", []).append({
        "statement": args.trigger_evidence,
        "recorded_at": now_iso(),
    })
    record.pop("reactivation_condition", None)
    record["updated_at"] = now_iso()
    save_checked(args.path, data, args.backup)
    print(f"promoted {args.id}: {args.status}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    data = load_state(args.path)
    errors = validate_state(data)
    if errors:
        print("state is invalid; run check for details", file=sys.stderr)
        return 1
    paths = data.get("attack_paths", [])
    by_status: dict[str, list[dict[str, Any]]] = {}
    for record in paths:
        by_status.setdefault(record.get("status", "unknown"), []).append(record)

    lines = [
        f"# Engagement report: {data['engagement_id']}",
        "",
        f"- objective: {data['objective']}",
        f"- scope: {data['scope']['status']} ({len(data['scope']['assets'])} assets)",
        f"- observations: " + ", ".join(
            f"{bucket}={len(data['observations'].get(bucket, []))}"
            for bucket in REQUIRED_OBSERVATIONS
        ),
        f"- findings: {len(data.get('findings', []))}",
        f"- persistent changes: {len(data.get('persistent_changes', []))}",
        f"- blockers: {len(data.get('blockers', []))}",
        "",
        "## Attack paths",
    ]
    if not paths:
        lines.append("- none recorded")
    for status in sorted(by_status):
        lines.append(f"### {status}")
        for record in by_status[status]:
            title = record.get("title") or record.get("id")
            line = f"- {record.get('id')}: {title}"
            if record.get("next_action"):
                line += f" → {record['next_action']}"
            if record.get("reactivation_condition"):
                line += f" (reactivate when: {record['reactivation_condition']})"
            lines.append(line)
    lines.extend(["", f"_last_updated: {data['last_updated']}_", ""])
    text = "\n".join(lines)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"report written to {args.out}")
    else:
        print(text)
    return 0


def add_path_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--path", type=Path, default=Path(".pentest_session.json"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init", help="create a new state file")
    add_path_argument(init_parser)
    init_parser.add_argument("--engagement-id", required=True)
    init_parser.add_argument("--objective", required=True)
    init_parser.add_argument("--domain", default="unclassified")
    init_parser.add_argument("--scope-status", choices=sorted(SCOPE_STATUSES), default="draft")
    init_parser.add_argument(
        "--authorization-ref",
        help="ticket / authorization letter / email id; required when --scope-status confirmed",
    )
    init_parser.add_argument(
        "--scope-root",
        help="optional subtree that owns this state; markers outside it are ignored",
    )
    init_parser.add_argument("--autonomous-levels", help="comma-separated L0,L1,L2 override")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=cmd_init)
    validate_parser = subparsers.add_parser("validate", help="validate a state file")
    add_path_argument(validate_parser)
    validate_parser.set_defaults(func=cmd_validate)
    summary_parser = subparsers.add_parser("summary", help="print a compact state summary")
    add_path_argument(summary_parser)
    summary_parser.set_defaults(func=cmd_summary)
    authorize_parser = subparsers.add_parser("authorize", help="update bounded autonomy settings")
    add_path_argument(authorize_parser)
    authorize_parser.add_argument("--levels", help="comma-separated L0,L1,L2")
    authorize_parser.add_argument("--approve-action", action="append", default=[])
    authorize_parser.add_argument("--exclude-action", action="append", default=[])
    authorize_parser.add_argument("--stop-condition", action="append", default=[])
    authorize_parser.add_argument("--backup", action="store_true")
    authorize_parser.set_defaults(func=cmd_authorize)
    push_parser = subparsers.add_parser("push-module", help="push a continuity frame")
    add_path_argument(push_parser)
    push_parser.add_argument("--module-id", required=True)
    push_parser.add_argument("--parent-path", required=True)
    push_parser.add_argument("--objective", required=True)
    push_parser.add_argument("--return-target", required=True)
    push_parser.add_argument("--supporting-domain")
    push_parser.add_argument("--backup", action="store_true")
    push_parser.set_defaults(func=cmd_push_module)
    pop_parser = subparsers.add_parser("pop-module", help="pop the current continuity frame")
    add_path_argument(pop_parser)
    pop_parser.add_argument("--module-id")
    pop_parser.add_argument("--backup", action="store_true")
    pop_parser.set_defaults(func=cmd_pop_module)
    checkpoint_parser = subparsers.add_parser("checkpoint", help="validate and refresh timestamp")
    add_path_argument(checkpoint_parser)
    checkpoint_parser.add_argument("--backup", action="store_true")
    checkpoint_parser.set_defaults(func=cmd_checkpoint)

    for alias, func, helptext in (
        ("position", cmd_summary, "alias of summary: show current position"),
        ("check", cmd_validate, "alias of validate: check the state schema"),
    ):
        alias_parser = subparsers.add_parser(alias, help=helptext)
        add_path_argument(alias_parser)
        alias_parser.set_defaults(func=func)

    fact_parser = subparsers.add_parser("fact", help="record an observation")
    add_path_argument(fact_parser)
    fact_parser.add_argument("--statement", required=True)
    fact_parser.add_argument("--source", required=True)
    fact_parser.add_argument(
        "--class", dest="observation_class", required=True, choices=sorted(OBSERVATION_KEYS),
    )
    fact_parser.add_argument("--confidence", choices=CONFIDENCE_LEVELS, default="medium")
    fact_parser.add_argument("--asset", action="append", default=[])
    fact_parser.add_argument("--backup", action="store_true")
    fact_parser.set_defaults(func=cmd_fact)

    path_parser = subparsers.add_parser("path", help="create or update an attack path")
    add_path_argument(path_parser)
    path_parser.add_argument("--id", required=True)
    path_parser.add_argument("--title", required=True)
    path_parser.add_argument("--status", required=True, choices=sorted(PATH_STATUSES))
    path_parser.add_argument("--next-action", required=True)
    path_parser.add_argument("--parent-path")
    path_parser.add_argument("--value")
    path_parser.add_argument("--backup", action="store_true")
    path_parser.set_defaults(func=cmd_path)

    park_parser = subparsers.add_parser("park", help="park a path with a reactivation condition")
    add_path_argument(park_parser)
    park_parser.add_argument("--id", required=True)
    park_parser.add_argument("--reactivation-condition", required=True)
    park_parser.add_argument("--backup", action="store_true")
    park_parser.set_defaults(func=cmd_park)

    promote_parser = subparsers.add_parser("promote", help="reactivate or deepen a parked path")
    add_path_argument(promote_parser)
    promote_parser.add_argument("--id", required=True)
    promote_parser.add_argument("--trigger-evidence", required=True)
    promote_parser.add_argument("--status", choices=["active", "deep_dive"], default="active")
    promote_parser.add_argument("--backup", action="store_true")
    promote_parser.set_defaults(func=cmd_promote)

    report_parser = subparsers.add_parser("report", help="render a report summary from state")
    add_path_argument(report_parser)
    report_parser.add_argument("--out", type=Path)
    report_parser.set_defaults(func=cmd_report)
    return parser


def main() -> int:
    for stream, kwargs in (
        (sys.stdout, {"encoding": "utf-8"}),
        (sys.stderr, {"encoding": "utf-8", "errors": "replace"}),
    ):
        try:
            stream.reconfigure(**kwargs)
        except Exception:
            pass
    args = build_parser().parse_args()
    try:
        return args.func(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
