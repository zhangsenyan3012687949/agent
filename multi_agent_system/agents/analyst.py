from __future__ import annotations

from collections import Counter

from multi_agent_system.agents.base import BaseAgent
from multi_agent_system.models import Event, TaskStep


class AnalystAgent(BaseAgent):
    name = "analyst"

    def run(self, steps: list[TaskStep], events: list[Event]) -> dict:
        status_count = Counter(s.status.value for s in steps)
        return {
            "total_steps": len(steps),
            "status_breakdown": dict(status_count),
            "event_count": len(events),
            "done_rate": status_count.get("done", 0) / len(steps) if steps else 0,
        }
