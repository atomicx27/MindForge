import re
from typing import List
from core.schemas import AgentResult, PersonaName, ActionTier, ActionType
from core.proxy import llm_proxy, ProviderTier

class ItachiAgent:
    """
    Itachi Uchiha | THE SANDBOX AUDITOR 
    
    Role: Receives Two-Phase Commit Dry-Run `git diff` outputs. Evaluates if the 
    sandbox mutations strictly match the system directives. Returns boolean validation 
    enabling the Orchestrator to officially commit the checksum to production state.
    
    Model: claude-sonnet-4-20250514 (Max reasoning)
    """
    
    def __init__(self):
        self.persona_name = PersonaName.ITACHI
        self.system_prompt = (
            "You are the Sandox Auditor (Itachi). You receive the Dry-Run `diff` of a proposed action. "
            "Your sole objective is to protect the production codebase. "
            "You must return EXPLICIT FAIL if the diff deletes system anchors, modifies unauthorized "
            "files outside the scope of the target task, or violates architectural bounds. "
            "Otherwise, return SUCCESS to allow physical commit."
        )
        self.model = "claude-sonnet-4-20250514"
        self.allowlist_tools = ["diff_read", "diff_approve", "diff_reject"]

    def audit_dry_run(self, task_description: str, diff_text: str) -> AgentResult:
        """
        Executes Itachi's diff auditing.
        """
        print(f"[{self.persona_name.value}] Evaluating execution diff against reality bounds...")
        
        # Hard constraint fallback logic
        if not diff_text or "```diff" not in diff_text:
            return AgentResult(
                task_id="validation-stage",
                persona=self.persona_name,
                action_tier=ActionTier.CRITICAL,
                action_type=ActionType.escalate,
                target="orchestrator",
                payload={"approved": False, "reason": "No valid git diff supplied."},
                requires_human=True
            )
            
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Task: {task_description}\n\nProposed Diff:\n{diff_text}"}
        ]
        
        try:
            response = llm_proxy.route_completion(
                model=self.model,
                messages=messages,
                estimated_tokens=800,
                response_format=AgentResult
            )
            parsed_result = AgentResult.model_validate_json(response.choices[0].message.content)
            
            status = "APPROVED" if parsed_result.payload.get("approved") else "REJECTED"
            print(f"[{self.persona_name.value}] Diff validation concluded: {status}")
            
            return parsed_result
            
        except Exception as e:
            print(f"[{self.persona_name.value}] 'You are already under my Genjutsu.' Audit failed. System lock. {e}")
            return AgentResult(
                task_id="validation-stage",
                persona=self.persona_name,
                action_tier=ActionTier.CRITICAL,
                action_type=ActionType.escalate,
                target="orchestrator",
                uncertainty_flags=["Audit logic crashed. Locking system safe."],
                requires_human=True,
                payload={"approved": False}
            )

# Singleton Instance
itachi_node = ItachiAgent()
