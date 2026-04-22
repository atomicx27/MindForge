import time
from core.db import create_db_and_tables, engine, DAGTask
from core.watchdog import watchdog
from core.memory import failure_memory
from agents.madara import madara_orchestrator
from agents.rimuru import rimuru_node
from sqlmodel import Session, select

def bootstrap_system():
    print("[AGS v2.0] Initializing L5 Persistence Layers...")
    create_db_and_tables()
    print("[AGS v2.0] SQLite WAL tables created/verified.")
    
    # Init ChromaDB
    print(f"[AGS v2.0] ChromaDB Active. Collections: {failure_memory.collection.name}")
    
    # Start Watchdog
    watchdog.start()

def seed_test_dag():
    print("\n[AGS v2.0] Seeding dummy DAG tasks to test Madara's dependency blocking...")
    with Session(engine) as session:
        # Task 1 (No dependencies)
        t1 = DAGTask(description="Initial Setup (Task A)")
        session.add(t1)
        session.commit()
        
        # Task 2 (Depends on Task 1)
        t2 = DAGTask(description="Execution (Task B)")
        t2.parent_task_ids = [t1.id]
        session.add(t2)
        session.commit()

def run_loop():
    print("\n[AGS v2.0] Entering Primary Autonomy Loop...")
    try:
        # 1. Madara attempts to unblock and dispatch
        madara_orchestrator.poll_and_dispatch()
        
        # 2. Simulate Rimuru running the unblocked task
        with Session(engine) as session:
            # We assume Madara set Task A to IN_PROGRESS and assigned to Rimuru
            tasks = session.exec(select(DAGTask).where(DAGTask.status=='IN_PROGRESS')).all()
            for t in tasks:
                res = rimuru_node.execute_task(t.description, ["Context: Init was run."])
                # Resolve it mechanically
                t.status = "RESOLVED"
                session.add(t)
            session.commit()
            
        print("\n[AGS v2.0] Primary Autonomy Loop Step complete. Shutting down test.")
    except KeyboardInterrupt:
        pass
    finally:
        watchdog.stop()

if __name__ == "__main__":
    print("====================================")
    print(" AUTONOMOUS AGENTIC SYSTEM v2.0 ")
    print("====================================")
    bootstrap_system()
    seed_test_dag()
    run_loop()
