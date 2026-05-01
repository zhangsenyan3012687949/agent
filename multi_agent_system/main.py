from __future__ import annotations

import argparse

from multi_agent_system.core.orchestrator import Orchestrator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-Agent 协同运营自动化系统")
    parser.add_argument("--goal", required=True, help="运营目标描述")
    parser.add_argument("--output", default="outputs", help="输出目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = Orchestrator(output_dir=args.output).run(args.goal)
    print(f"Run completed: {result.run_id}")
    print(f"Summary: {result.summary}")


if __name__ == "__main__":
    main()
