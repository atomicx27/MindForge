from typing import List, Optional, Any, Dict
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
import uuid

class ActionTier(str, Enum):
    TRIVIAL = "TRIVIAL"
    STANDARD = "STANDARD"
    CRITICAL = "CRITICAL"

class ActionType(str, Enum):
    file_write = "file_write"
    file_delete = "file_delete"
    shell_exec = "shell_exec"
    api_call = "api_call"
    research = "research"
    summarize = "summarize"
    escalate = "escalate"

class PersonaName(str, Enum):
    ITACHI = "Itachi"
    MADARA = "Madara"
    CHHOTA_BHEEM = "Chhota Bheem"
    DORAEMON = "Doraemon"
    RIMURU = "Rimuru"
    GOKU = "Goku"
    NARUTO = "Naruto"
    ICHIGO = "Ichigo"
    NATSU = "Natsu"
    BEN_10 = "Ben_10"

class AgentResult(BaseModel):
    """
    Standard schema all Personas MUST adhere to before returning payload over to the logic Orchestrator. 
    This entirely replaces arbitrary 'Confidence Mapping'.
    """
    model_config = ConfigDict(strict=True)

    task_id: str = Field(..., description="UUID of the DAG Task")
    persona: PersonaName
    action_tier: ActionTier
    action_type: ActionType
    target: str = Field(..., description="File path, URL, or shell command.")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Action-specific typed body")
    
    # Explicit uncertainty enumeration replaces confident hallucination
    uncertainty_flags: List[str] = Field(default_factory=list, description="List of concrete uncertainties e.g. ['path may not exist']")
    
    requires_human: bool = Field(default=False)
    handoff_to: Optional[PersonaName] = Field(default=None, description="Next persona node if chaining")

class HandoffPayload(BaseModel):
    """
    Contract schema for when Agent A passes results to Agent B.
    """
    task_id: str
    files_modified: List[str]
    context_notes: str
    pass_fail_status: bool
    suggestions_for_next_agent: List[str]
