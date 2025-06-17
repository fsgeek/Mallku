import asyncio

from mallku.governance.fire_circle_orchestrator import FireCircleOrchestrator


def test_plan_ceremony_structure():
    sample_diff = "// sample code diff"
    orc = FireCircleOrchestrator(providers=[])
    plan = orc.plan_ceremony(sample_diff)
    assert isinstance(plan.invocation, str)
    assert "Ayni" in plan.invocation
    assert len(plan.rounds) == 4
    for rnd in plan.rounds:
        assert rnd.name
        assert rnd.prompt
    assert isinstance(plan.closing, str)
    assert isinstance(plan.guide, dict)

def test_run_ceremony_no_providers_returns_empty_responses():
    sample_diff = "// sample code diff"
    orc = FireCircleOrchestrator(providers=[])
    # Run synchronously to avoid pytest-asyncio’s event-loop issues
    record = asyncio.run(orc.run_ceremony(sample_diff))
    assert record.ceremony_id is not None
    assert isinstance(record.responses, list)
    assert len(record.responses) == 0
