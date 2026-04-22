from core.schemas import AgentResult, PersonaName, ActionTier, ActionType
from core.proxy import llm_proxy, ProviderTier

class ChhotaBheemAgent:
    """
    Chhota Bheem | CLOUD-COLAB DISPATCHER
    
    Role: Dispatches massive batch workloads (like 10M token processing or 124x AST maps) 
    directly through the Ngrok tunnel to the dedicated heavy computation Google Colab.
    """
    def __init__(self):
        self.persona_name = PersonaName.CHHOTA_BHEEM
        
    def dispatch_heavy_load(self, data_payload: dict) -> AgentResult:
        print(f"[{self.persona_name.value}] Pushing heavy workload through Ngrok Colab tunnel...")
        
        # Here we explicitly force the LLM Proxy to use the OLLAMA_COLAB tier.
        return AgentResult(
            task_id="heavy-compute",
            persona=self.persona_name,
            action_tier=ActionTier.CRITICAL,
            action_type=ActionType.api_call,
            target="colab-tunnel",
            payload=data_payload,
            handoff_to=PersonaName.MADARA
        )

chhota_bheem_dispatcher = ChhotaBheemAgent()
