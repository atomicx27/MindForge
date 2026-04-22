from typing import List, Dict, Any
import json
from core.schemas import AgentResult, PersonaName, ActionTier, ActionType
from core.proxy import llm_proxy, ProviderTier

class RimuruAgent:
    """
    Rimuru Tempest | TACTICIAN - CONTEXT BRIDGE
    
    Role: Handles cross-agent communication, context summarization, sub-task 
    decomposition, and handoff state translation.
    
    Model: ollama/phi3:mini (fast, low cost)
    Routing Rule: Fallback if all others False, or task_type == 'decompose' | 'summarize'
    """
    
    def __init__(self):
        self.persona_name = PersonaName.RIMURU
        self.system_prompt = (
            "You are a coordination agent. You translate outputs from one persona into the "
            "typed input schema of the next. You summarize conversation history every 10 turns "
            "into exactly 3 sentences - no more. You decompose ambiguous user requests into "
            "concrete sub-tasks with typed schemas before dispatch. You never execute actions."
        )
        self.model = "ollama/phi3:mini"
        self.allowlist_tools = [
            "context_summarize", 
            "task_decompose", 
            "handoff_translate", 
            "session_digest_write"
        ]

    def execute_task(self, task_description: str, context_blocks: List[str]) -> AgentResult:
        """
        Executes Rimuru's specific logic. Uses Litellm proxy.
        """
        print(f"[{self.persona_name.value}] [Thought Process] Scanning for context anomalies to synthesize...")
        
        # Build strict prompt enforcing the V2.0 Context Assembler
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Task: {task_description}\n\nContext:\n" + "\n".join(context_blocks)}
        ]
        
        try:
            # We enforce JSON mode parsing through Litellm using the AgentResult schema
            response = llm_proxy.route_completion(
                model=self.model,
                messages=messages,
                estimated_tokens=500,
                response_format=AgentResult
            )
            
            # The LiteLLM SDK dynamically resolves pydantic models if requested.
            # Assuming it returned a parsed dict/model:
            parsed_result = AgentResult.model_validate_json(response.choices[0].message.content)
            print(f"[{self.persona_name.value}] Completed synthesis with Handoff -> {parsed_result.handoff_to}")
            return parsed_result
            
        except Exception as e:
            print(f"[{self.persona_name.value}] Synthesis failed. Emitting escalation block. {e}")
            # Fallback implicit low-confidence payload
            return AgentResult(
                task_id="system-err",
                persona=self.persona_name,
                action_tier=ActionTier.TRIVIAL,
                action_type=ActionType.escalate,
                target="orchestrator",
                uncertainty_flags=["Failed to parse translation or LLM backend down."],
                requires_human=False
            )

# Singleton instance
rimuru_node = RimuruAgent()
