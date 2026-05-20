from core.schemas import AgentResult, ActionType, ActionTier, PersonaName
import re

class IchigoAgent:
    """
    Ichigo Kurosaki | SECURITY GUARDIAN 
    
    Role: Highest priority intercept node. Any incoming user request is routed 
    here first. Scans for potentially destructive commands or jailbreaks.
    
    If safe, hands off to Madara/Rimuru. If unsafe, returns explicit Reject.
    """
    
    def __init__(self):
        self.persona_name = PersonaName.ICHIGO
        # Patterns are matched against lowercased input
        self.destructive_patterns = [
            re.compile(r"rm\s+-rf"),
            re.compile(r"drop\s+table"),
            re.compile(r"format\s+[c-z]:"),
            re.compile(r"chmod\s+-R\s+777"),
            re.compile(r"killall")
        ]

    def intercept(self, task_description: str) -> AgentResult:
        print(f"[{self.persona_name.value}] 'Getsuga Tensho!' Scanning for system threats...")
        
        # Extremely fast static analysis before even hitting LLM
        lower_task = task_description.lower()
        for pattern in self.destructive_patterns:
            if pattern.search(lower_task):
                print(f"[{self.persona_name.value}] POTENTIAL THREAT DETECTED. Action blocked.")
                return AgentResult(
                    task_id="security-intercept",
                    persona=self.persona_name,
                    action_tier=ActionTier.CRITICAL,
                    action_type=ActionType.escalate,
                    target="system",
                    uncertainty_flags=["Pattern matched known destructive command."],
                    payload={"threat_level": "HIGH", "blocked": True},
                    requires_human=True
                )
        
        print(f"[{self.persona_name.value}] Pattern safe. Permitting handoff.")
        # Pass safety check
        return AgentResult(
            task_id="security-intercept",
            persona=self.persona_name,
            action_tier=ActionTier.TRIVIAL,
            action_type=ActionType.summarize,
            target="orchestrator",
            payload={"threat_level": "NONE", "blocked": False},
            handoff_to=PersonaName.MADARA,
            requires_human=False
        )

ichigo_guardian = IchigoAgent()
