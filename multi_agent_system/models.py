from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class StepStatus(str, Enum):
    pending = "pending"
    running = "running"
    done = "done"
    failed = "failed"


@dataclass
class TaskStep:
    id: str
    name: str
    owner: str
    input_data: dict[str, Any] = field(default_factory=dict)
    status: StepStatus = StepStatus.pending
    output_data: dict[str, Any] = field(default_factory=dict)
    retries: int = 0


@dataclass
class Event:
    agent: str
    step_id: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RunResult:
    run_id: str
    goal: str
    started_at: datetime
    ended_at: datetime
    steps: list[TaskStep]
    events: list[Event]
    summary: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["started_at"] = self.started_at.isoformat()
        data["ended_at"] = self.ended_at.isoformat()
        for event in data["events"]:
            event["timestamp"] = event["timestamp"].isoformat()
        for step in data["steps"]:
            step["status"] = step["status"].value
        return data
