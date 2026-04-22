from sqlmodel import Field, SQLModel, create_engine, Session, JSON, Column
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import uuid

class Anchor(SQLModel, table=True):
    """Hard Memory Anchors that cannot be deleted during context rolling."""
    id: Optional[int] = Field(default=None, primary_key=True)
    directive: str = Field(index=True)
    added_at: datetime = Field(default_factory=datetime.utcnow)

class DAGTask(SQLModel, table=True):
    """The directed acyclic graph task node."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    description: str
    status: str = Field(default="PENDING")  # PENDING, IN_PROGRESS, RESOLVED, BLOCKED, FAILED, TIMED_OUT, NEEDS_REROUTE
    assigned_persona: Optional[str] = None
    time_started: Optional[datetime] = None
    max_ttl: int = Field(default=600)  # Time to live in seconds
    
    # Store JSON list of parent task UUIDs that must be RESOLVED before this is unblocked
    parent_task_ids_json: str = Field(default="[]") 
    
    checkpoint_hash: Optional[str] = None

    @property
    def parent_task_ids(self) -> List[str]:
        return json.loads(self.parent_task_ids_json)

    @parent_task_ids.setter
    def parent_task_ids(self, value: List[str]):
        self.parent_task_ids_json = json.dumps(value)

class ExecutionSnapshot(SQLModel, table=True):
    """Two-Phase commit Checksum snapshot."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    task_id: str = Field(index=True)
    pre_execution_checksum: str
    paths_monitored_json: str = Field(default="[]")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ExecutionLog(SQLModel, table=True):
    """Receipt mapping of a fully executed task."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    task_id: str = Field(index=True)
    action_type: str
    pre_checksum: str
    post_checksum: str
    duration_ms: int
    persona_executed: str
    rollback_status: str = Field(default="NONE") # NONE, TRIGGERED, SUCCESS, FAILED
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Configure SQLite DB with WAL (Write-Ahead Logging) for crash safety
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    # Enable WAL mode safely
    SQLModel.metadata.create_all(engine)
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA journal_mode=WAL;")

def get_session():
    with Session(engine) as session:
        yield session
