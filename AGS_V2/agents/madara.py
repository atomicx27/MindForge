from typing import List
from sqlmodel import Session, select
from core.db import engine, DAGTask
from core.schemas import AgentResult, PersonaName, ActionTier, ActionType
from core.proxy import llm_proxy

class MadaraAgent:
    """
    Madara Uchiha | DAG CONTROLLER
    
    Role: Orchestrator-level agent. Manages task dependency graphs, blocks premature 
    task execution, resolves DAG deadlocks.
    """
    
    def __init__(self):
        self.persona_name = PersonaName.MADARA
        self.system_prompt = (
            "You are the absolute authority on task execution order. You receive the full DAG state. "
            "You must identify all tasks whose parent_task_ids are not fully RESOLVED. Block them. "
            "Identify tasks ready to execute and dispatch them to the correct persona. "
            "You do not write code. You do not execute actions. You manage flow only."
        )
        self.model = "claude-sonnet-4-20250514"
        self.allowlist_tools = [
            "dag_read", "dag_write", "dag_block", "dag_unblock", "task_reroute", "persona_dispatch"
        ]

    def poll_and_dispatch(self):
        """
        Polls the SQLite DAG graph and finds the next unblocked task.
        In the real system, it uses Litellm to evaluate the array, but here goes the mechanical check:
        """
        print(f"[{self.persona_name.value}] 'Wake up to reality.' Parsing the DAG Graph...")
        
        with Session(engine) as session:
            # Get all pending tasks
            statement = select(DAGTask).where(DAGTask.status == "PENDING")
            pending_tasks = session.exec(statement).all()
            
            # Simple DAG resolution mechanic
            for task in pending_tasks:
                parents_resolved = True
                for parent_id in task.parent_task_ids:
                    # Check if parent is resolved
                    p_stat = select(DAGTask).where(DAGTask.id == parent_id)
                    ptask = session.exec(p_stat).first()
                    if not ptask or ptask.status != "RESOLVED":
                        parents_resolved = False
                        break
                
                if parents_resolved:
                    print(f"[{self.persona_name.value}] Task '{task.description}' is unblocked. Routing.")
                    task.status = "IN_PROGRESS"
                    # Here we would use the LLM to figure out the persona_dispatch tool.
                    # Hard-coding to Rimuru for the test MVP.
                    task.assigned_persona = "Rimuru"
                    session.add(task)
                else:
                    print(f"[{self.persona_name.value}] Task '{task.description}' BLOCKED by active dependencies.")
                    task.status = "BLOCKED"
                    session.add(task)
            
            session.commit()

# Singleton Orchestrator
madara_orchestrator = MadaraAgent()
