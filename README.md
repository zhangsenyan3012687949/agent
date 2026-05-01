# Multi-Agent 协同运营自动化系统

一个可扩展的多 Agent 协同运营自动化系统，支持：
- 任务分解（Planner Agent）
- 执行调度（Executor Agent）
- 质量审计（Reviewer Agent）
- 指标汇总与运营日报（Analyst Agent）
- 流程编排与重试机制（Orchestrator）

## 架构

```text
┌───────────────┐
│ Orchestrator  │
└──────┬────────┘
       │
┌──────▼────────┐
│ PlannerAgent  │  任务拆解
└──────┬────────┘
       │ steps
┌──────▼────────┐
│ ExecutorAgent │  任务执行 + 事件记录
└──────┬────────┘
       │ results
┌──────▼────────┐
│ ReviewerAgent │  质量打分 + 返工建议
└──────┬────────┘
       │
┌──────▼────────┐
│ AnalystAgent  │  KPI 汇总 + 报表
└───────────────┘
```

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m multi_agent_system.main --goal "本周完成新功能发布并输出运营复盘"
```

## 示例输出
- 控制台会输出每个 Agent 的执行日志。
- 结果会落盘到 `outputs/` 目录，包括：
  - `run_<id>.json`
  - `report_<id>.md`

## 可扩展点
- `agents/` 目录可新增专职 Agent（如增长、客服、风控）。
- `tools/` 目录可接入真实外部系统（Jira、Slack、邮件、CRM、BI）。
- `policies.py` 可配置 SLA、重试次数、审批规则。
