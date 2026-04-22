import pytest
from agents.rimuru import RimuruAgent
from agents.itachi import ItachiAgent
from agents.madara import madara_orchestrator
from core.schemas import AgentResult, PersonaName, ActionTier, ActionType
from unittest.mock import patch, MagicMock
from core.db import DAGTask, create_db_and_tables, engine
from sqlmodel import Session, select

@pytest.fixture(autouse=True)
def setup_database():
    create_db_and_tables()
    # clean up the tasks before each test so we have a clean state
    with Session(engine) as session:
        for task in session.exec(select(DAGTask)).all():
            session.delete(task)
        session.commit()
    yield

def test_rimuru_agent():
    agent = RimuruAgent()
    with patch("core.proxy.llm_proxy.route_completion") as mock_completion:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"task_id": "mock_task", "persona": "Rimuru", "action_tier": "TRIVIAL", "action_type": "summarize", "target": "mock_target", "payload": {}, "uncertainty_flags": [], "requires_human": false}'
        mock_completion.return_value = mock_response

        result = agent.execute_task("test", ["context"])

        assert isinstance(result, AgentResult)
        assert result.persona == PersonaName.RIMURU
        assert result.task_id == "mock_task"

def test_itachi_agent():
    agent = ItachiAgent()
    with patch("core.proxy.llm_proxy.route_completion") as mock_completion:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"task_id": "validation-stage", "persona": "Itachi", "action_tier": "CRITICAL", "action_type": "research", "target": "orchestrator", "payload": {"approved": true}, "uncertainty_flags": [], "requires_human": false}'
        mock_completion.return_value = mock_response

        result = agent.audit_dry_run("test", "```diff\n+ test\n```")

        assert isinstance(result, AgentResult)
        assert result.persona == PersonaName.ITACHI
        assert result.payload.get("approved") is True

def test_madara_orchestrator():
    # Setup test tasks
    with Session(engine) as session:
        t1 = DAGTask(description="Initial Setup (Task A)", status="PENDING")
        session.add(t1)
        session.commit()
        session.refresh(t1)

        t2 = DAGTask(description="Execution (Task B)", status="PENDING")
        t2.parent_task_ids = [t1.id]
        session.add(t2)
        session.commit()

    madara_orchestrator.poll_and_dispatch()

    with Session(engine) as session:
        # Task A should be IN_PROGRESS
        tasks_in_progress = session.exec(select(DAGTask).where(DAGTask.status == "IN_PROGRESS")).all()
        assert len(tasks_in_progress) == 1
        assert tasks_in_progress[0].description == "Initial Setup (Task A)"

        # Task B should be BLOCKED
        tasks_blocked = session.exec(select(DAGTask).where(DAGTask.status == "BLOCKED")).all()
        assert len(tasks_blocked) == 1
        assert tasks_blocked[0].description == "Execution (Task B)"
