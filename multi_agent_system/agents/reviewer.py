from __future__ import annotations

from multi_agent_system.agents.base import BaseAgent


class ReviewerAgent(BaseAgent):
    name = "reviewer"

    def run(self, step_name: str, output: dict) -> dict:
        score = 0.9 if "完成" in output.get("result", "") else 0.6
        return {
            "score": score,
            "approved": score >= 0.75,
            "suggestion": "通过" if score >= 0.75 else f"{step_name} 需要补充验收标准",
        }
