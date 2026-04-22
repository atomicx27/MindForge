from core.schemas import AgentResult, PersonaName, ActionTier, ActionType
from core.proxy import llm_proxy

class DoraemonAgent:
    """
    Doraemon | EXTERNAL TOOL COMPOSITOR
    
    Role: Receives requests for specific non-standard MCP operations (e.g. GitHub integrations,
    external 3rd party APIs). Acts as the interface translation layer.
    """
    def __init__(self):
        self.persona_name = PersonaName.DORAEMON
        self.allowlist_tools = ["mcp_connect", "mcp_execute"]
        
    def equip_tool(self, tool_name: str, args: dict) -> AgentResult:
        print(f"[{self.persona_name.value}] Deploying Gadget: {tool_name}!")
        return AgentResult(
            task_id="mcp-ops",
            persona=self.persona_name,
            action_tier=ActionTier.STANDARD,
            action_type=ActionType.api_call,
            target=tool_name,
            payload=args,
            handoff_to=PersonaName.MADARA
        )

class Ben10Agent:
    """
    Ben 10 | WEB SEARCH AND SCRAPER
    
    Role: Transforms into a high-utility browser navigator. Evaluates domain trust 
    diversity, prevents crawling explicitly blocked or highly unreliable sources.
    """
    def __init__(self):
        self.persona_name = PersonaName.BEN_10
        self.allowlist_tools = ["web_search", "browser_scrape", "diversity_check"]

    def perform_search(self, query: str) -> AgentResult:
        print(f"[{self.persona_name.value}] 'It's Hero Time!' Scraping data for {query}...")
        return AgentResult(
            task_id="web-search",
            persona=self.persona_name,
            action_tier=ActionTier.STANDARD,
            action_type=ActionType.research,
            target="web",
            payload={"query": query},
            handoff_to=PersonaName.MADARA
        )

doraemon_compositor = DoraemonAgent()
ben10_scraper = Ben10Agent()
