from multi_agent_system.core.orchestrator import Orchestrator


def test_orchestrator_end_to_end(tmp_path):
    orchestrator = Orchestrator(output_dir=str(tmp_path))
    result = orchestrator.run("测试目标")

    assert result.summary["total_steps"] == 5
    assert result.summary["done_rate"] == 1.0
    assert (tmp_path / f"run_{result.run_id}.json").exists()
    assert (tmp_path / f"report_{result.run_id}.md").exists()
