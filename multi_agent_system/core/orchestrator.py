from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

from multi_agent_system.agents.analyst import AnalystAgent
from multi_agent_system.agents.executor import ExecutorAgent
from multi_agent_system.agents.planner import PlannerAgent
from multi_agent_system.agents.reviewer import ReviewerAgent
from multi_agent_system.models import Event, RunResult, StepStatus
from multi_agent_system.policies import MAX_RETRY, QUALITY_THRESHOLD


class Orchestrator:
    def __init__(self, output_dir: str = "outputs") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.reviewer = ReviewerAgent()
        self.analyst = AnalystAgent()

    def run(self, goal: str) -> RunResult:
        run_id = uuid.uuid4().hex[:8]
        started_at = datetime.utcnow()
        events: list[Event] = []
        steps = self.planner.run(goal)

        for step in steps:
            while step.retries <= MAX_RETRY:
                step.status = StepStatus.running
                events.append(Event(agent="orchestrator", step_id=step.id, message="step_started"))

                exec_output = self.executor.run(step.name, step.input_data)
                events.append(Event(agent="executor", step_id=step.id, message="step_executed", payload=exec_output))

                review = self.reviewer.run(step.name, exec_output)
                events.append(Event(agent="reviewer", step_id=step.id, message="step_reviewed", payload=review))

                if review["score"] >= QUALITY_THRESHOLD:
                    step.status = StepStatus.done
                    step.output_data = {**exec_output, "review": review}
                    break
                step.retries += 1

            if step.status != StepStatus.done:
                step.status = StepStatus.failed
                events.append(Event(agent="orchestrator", step_id=step.id, message="step_failed"))

        summary = self.analyst.run(steps, events)
        result = RunResult(run_id, goal, started_at, datetime.utcnow(), steps, events, summary)
        self._persist(result)
        return result

    def _persist(self, result: RunResult) -> None:
        json_path = self.output_dir / f"run_{result.run_id}.json"
        report_path = self.output_dir / f"report_{result.run_id}.md"
        json_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

        lines = [
            f"# 运营自动化报告 - {result.run_id}",
            "",
            f"目标: {result.goal}",
            f"开始: {result.started_at.isoformat()} UTC",
            f"结束: {result.ended_at.isoformat()} UTC",
            "",
            "## KPI",
            f"- 总步骤: {result.summary['total_steps']}",
            f"- 完成率: {result.summary['done_rate']:.0%}",
            f"- 事件数: {result.summary['event_count']}",
            "",
            "## 步骤明细",
        ]
        lines.extend([f"- {s.id} | {s.name} | {s.status.value} | retries={s.retries}" for s in result.steps])
        report_path.write_text("\n".join(lines), encoding="utf-8")
