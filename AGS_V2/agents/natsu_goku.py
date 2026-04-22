from core.schemas import AgentResult, PersonaName, ActionTier, ActionType
from core.proxy import llm_proxy

class NatsuAgent:
    """
    Natsu Dragneel | THE BUILDER
    
    Role: Receives physical execution targets. Generates precise logic/code.
    Passes directly to Itachi (Sandbox Auditor) for diff checking. Never commits directly.
    """
    def __init__(self):
        self.persona_name = PersonaName.NATSU
        self.system_prompt = (
            "You are the Builder (Natsu). You generate executable code or scripts to satisfy the task. "
            "You must output valid git diff formats wrapped in ```diff``` blocks so the Auditor can read them. "
            "You NEVER run commands. You produce the physical payload."
        )
        self.model = "ollama/codellama" # High proficiency code generation
        self.allowlist_tools = ["code_generate", "script_write"]

    def build_diff(self, task_description: str, context: str) -> AgentResult:
        print(f"[{self.persona_name.value}] 'I'm all fired up!' Generating code diff...")
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Task: {task_description}\nContext: {context}"}
        ]
        
        try:
            response = llm_proxy.route_completion(
                model=self.model,
                messages=messages,
                estimated_tokens=1500,
                response_format=AgentResult
            )
            parsed_result = AgentResult.model_validate_json(response.choices[0].message.content)
            # Route mechanically to Itachi
            parsed_result.handoff_to = PersonaName.ITACHI
            return parsed_result
        except Exception as e:
            return AgentResult(
                task_id="build",
                persona=self.persona_name,
                action_tier=ActionTier.CRITICAL,
                action_type=ActionType.escalate,
                target="orchestrator",
                uncertainty_flags=[str(e)],
                requires_human=True
            )

class GokuAgent:
    """
    Son Goku | AST OBSERVER / OPTIMIZER
    
    Role: Reads raw files, explores directories using AST matching or semantic searching.
    Passes optimal path findings to Natsu.
    """
    def __init__(self):
        self.persona_name = PersonaName.GOKU
        self.system_prompt = (
            "You are the AST Explorer (Goku). Search for functions, structure, and content. "
            "Do not write or modify code. Identify exact lines and file definitions."
        )
        self.model = "ollama/llama3"
        self.allowlist_tools = ["ast_read", "file_grep", "explore"]

    def explore(self, query: str) -> AgentResult:
        print(f"[{self.persona_name.value}] 'Hey, it's Goku!' Scanning for {query}...")
        # (Mock implementation for completeness)
        return AgentResult(
            task_id="explore",
            persona=self.persona_name,
            action_tier=ActionTier.STANDARD,
            action_type=ActionType.research,
            target="system",
            payload={"focus_elements": []},
            handoff_to=PersonaName.NATSU
        )

natsu_builder = NatsuAgent()
goku_explorer = GokuAgent()
