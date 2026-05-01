from __future__ import annotations

from multi_agent_system.agents.base import BaseAgent


class ExecutorAgent(BaseAgent):
    name = "executor"

    def run(self, step_name: str, context: dict) -> dict:
        return {
            "result": f"已完成: {step_name}",
            "artifacts": [f"{step_name}_输出文档.md"],
            "context_echo": context,
        }
