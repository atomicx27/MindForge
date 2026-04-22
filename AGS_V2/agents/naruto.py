from core.schemas import AgentResult, PersonaName, ActionTier, ActionType
from core.proxy import llm_proxy
from core.memory import failure_memory

class NarutoAgent:
    """
    Naruto Uzumaki | THE SELF-HEALER
    
    Role: Receives failed tasks and explicitly loops a Try-Rewrite-Retry 
    mechanism based on stack traces until the failure is resolved or max retries hit. 
    Never gives up immediately.
    """
    
    def __init__(self, max_retries: int = 3):
        self.persona_name = PersonaName.NARUTO
        self.max_retries = max_retries
        self.system_prompt = (
            "You are the self-healing retry engine. You receive a task that errored out, "
            "along with the Python stacktrace or CLI stderr. Analyze the mistake. "
            "Rewrite the code or command logic. You must output the corrected payload. "
            "If you hit a wall, query the ChromaDB failure_memory to see if we've solved this before."
        )
        self.model = "ollama/gemma:7b" # Strong coder model, or open-weights equivalent
        self.allowlist_tools = ["code_edit", "shell_exec", "failure_memory_read", "failure_memory_write"]

    def retry_loop(self, task_id: str, failed_action: str, error_trace: str) -> AgentResult:
        """
        Executes Naruto's Retry Logic Loop. Uses semantic memory to prevent looping on known issues.
        """
        print(f"[{self.persona_name.value}] 'I never go back on my word!' Initiating Rasengan Rewrite for Task {task_id}...")
        
        # 1. Ask ChromaDB if we already know this error
        memory_result = failure_memory.check_for_similar_failure(failed_action, error_trace)
        
        if memory_result["matched"]:
            print(f"[{self.persona_name.value}] Shadow Clone Jutsu! I remember this. Note: {memory_result['resolution_note']}")
            context_injection = f"WE HAVE FAILED THIS BEFORE. PREVIOUS SOLUTION NOTE: {memory_result['resolution_note']}"
        else:
            context_injection = "No previous memory of this exact failure."
            
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Failed Action: {failed_action}\nError: {error_trace}\nMemory: {context_injection}"}
        ]
        
        try:
            response = llm_proxy.route_completion(
                model=self.model,
                messages=messages,
                estimated_tokens=800,
                response_format=AgentResult
            )
            parsed_result = AgentResult.model_validate_json(response.choices[0].message.content)
            print(f"[{self.persona_name.value}] Retry payload generated. Emitting...")
            return parsed_result
            
        except Exception as e:
            print(f"[{self.persona_name.value}] Ran out of chakra: {e}")
            
            # Log the new unresolved failure permanently so we don't try it endlessly next time
            failure_memory.log_failure(task_id, failed_action, f"{error_trace}\nAdditional Model Fail: {e}")
            
            return AgentResult(
                task_id=task_id,
                persona=self.persona_name,
                action_tier=ActionTier.STANDARD,
                action_type=ActionType.escalate,
                target="orchestrator",
                uncertainty_flags=["Complete failure of try-rewrite-retry loop."],
                requires_human=True
            )

# Singleton Instance
naruto_healer = NarutoAgent()
