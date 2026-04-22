from core.db import engine, DAGTask, create_db_and_tables
from sqlmodel import Session, select
import pytest

@pytest.fixture(autouse=True)
def setup_database():
    create_db_and_tables()
    yield

def test_db_operations():
    with Session(engine) as session:
        t1 = DAGTask(description="Test 1")
        session.add(t1)
        session.commit()
        session.refresh(t1)

        t2 = DAGTask(description="Test 2")
        t2.parent_task_ids = [t1.id]
        session.add(t2)
        session.commit()
        session.refresh(t2)

        assert len(t2.parent_task_ids) == 1
        assert t2.parent_task_ids[0] == t1.id

        statement = select(DAGTask)
        tasks = session.exec(statement).all()
        assert len(tasks) >= 2
