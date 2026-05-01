from __future__ import annotations

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.models import TaskStep


class PlannerAgent(BaseAgent):
    name = "planner"

    def run(self, goal: str) -> list[TaskStep]:
        base_steps = [
            ("需求澄清", "product"),
            ("研发实现", "engineering"),
            ("测试验证", "qa"),
            ("上线发布", "ops"),
            ("数据复盘", "analyst"),
        ]
        return [
            TaskStep(id=f"S{i+1}", name=step, owner=owner, input_data={"goal": goal})
            for i, (step, owner) in enumerate(base_steps)
        ]
