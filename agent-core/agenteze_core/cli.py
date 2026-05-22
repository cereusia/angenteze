from __future__ import annotations

import argparse
import json
import sys

from .contracts import AgentRequest
from .runtime import AgentRuntime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agenteze-core")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Process a prompt")
    run_parser.add_argument("--prompt", required=True)
    run_parser.add_argument("--source", default="macos")

    subparsers.add_parser("status", help="Return backend status")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    runtime = AgentRuntime()

    if args.command == "run":
        request = AgentRequest.from_prompt(prompt=args.prompt, source=args.source)
        response = runtime.handle(request)
        print(json.dumps(response.to_dict(), ensure_ascii=False))
        return 0

    if args.command == "status":
        print(json.dumps(runtime.status(), ensure_ascii=False))
        return 0

    parser.print_help(sys.stderr)
    return 2
