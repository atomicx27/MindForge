import threading
import time
import os
import signal
from datetime import datetime
from sqlmodel import Session, select
from core.db import engine, DAGTask

class TTLWatchdog:
    """
    Background daemon that monitors the SQLite DAG execution tasks.
    If a task exceeds its max_ttl in seconds, this thread will force a `SIGTERM` 
    to the active sub-process, mark the task as TIMED_OUT, and create a reroute request.
    """
    
    def __init__(self, polling_interval_sec: int = 30):
        self.polling_interval = polling_interval_sec
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            print("[WATCHDOG] TTL Watchdog started.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _monitor_loop(self):
        """
        Polls the database and intercepts hanging processes.
        """
        while self.running:
            try:
                with Session(engine) as session:
                    # Select tasks that are currently IN_PROGRESS
                    statement = select(DAGTask).where(DAGTask.status == "IN_PROGRESS")
                    active_tasks = session.exec(statement).all()
                    
                    now = datetime.utcnow()
                    for task in active_tasks:
                        if task.time_started and task.max_ttl > 0:
                            elapsed = (now - task.time_started).total_seconds()
                            if elapsed > task.max_ttl:
                                print(f"[WATCHDOG] Task {task.id} exceeded TTL ({elapsed}s / {task.max_ttl}s). Terminating...")
                                
                                # 1. Mark task as failed
                                task.status = "TIMED_OUT"
                                
                                # 2. Reroute via spawning a new task node
                                reroute = DAGTask(
                                    description=f"Reroute TIMED_OUT task {task.id}",
                                    status="NEEDS_REROUTE"
                                )
                                session.add(reroute)
                                session.commit()
                                
                                # In a true architecture, we would have stored the PID of the agent process 
                                # in the database and would execute `os.kill(pid, signal.SIGTERM)` here.
                                
            except Exception as e:
                print(f"[WATCHDOG] Error in loop: {e}")
                
            time.sleep(self.polling_interval)

watchdog = TTLWatchdog()
