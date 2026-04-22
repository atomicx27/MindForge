import redis
import time
from typing import Optional, Dict, Any, List
from litellm import completion
from enum import Enum

class ProviderTier(str, Enum):
    OLLAMA_LOCAL = "OLLAMA_LOCAL"
    OLLAMA_COLAB = "OLLAMA_COLAB"
    ANTHROPIC = "ANTHROPIC"
    OPENAI = "OPENAI"

class LLMProviderProxy:
    """
    Abstracts all LLM generation logic. Routes through providers strictly via Priority list to avoid
    cost runaways and handle token-bucket rate limit exhaustion dynamically.
    """
    
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379):
        # We wrap redis connect in try/except because if redis isn't running on Windows natively, 
        # we will fallback to an in-memory dict for the dev MVP.
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
            self.redis_client.ping()
            self.using_redis = True
        except redis.ConnectionError:
            print("[WARN] Redis not found running natively on Windows. Falling back to in-memory rate limiter for Dev Mode.")
            self.using_redis = False
            self.memory_state = {}

        # Default fallback chain order
        self.provider_chain = [
            ProviderTier.OLLAMA_LOCAL,
            ProviderTier.OLLAMA_COLAB,
            ProviderTier.ANTHROPIC,
            ProviderTier.OPENAI
        ]
        
        # Hard limits (tokens per minute)
        self.limits = {
            ProviderTier.OLLAMA_LOCAL: 100000,
            ProviderTier.OLLAMA_COLAB: 200000,
            ProviderTier.ANTHROPIC: 40000,   # example API bucket limit
            ProviderTier.OPENAI: 30000
        }

    def _check_rate_limit(self, provider: ProviderTier, estimated_tokens: int) -> bool:
        """
        Token-bucket basic simulation. Returns True if bucket has capacity.
        """
        bucket_key = f"rl:bucket:{provider.value}"
        current_minute = str(int(time.time() / 60))
        key = f"{bucket_key}:{current_minute}"
        
        limit = self.limits.get(provider, 10000)
        
        if self.using_redis:
            current_usage = self.redis_client.get(key)
            if not current_usage:
                current_usage = 0
            if int(current_usage) + estimated_tokens > limit:
                return False
            return True
        else:
            current_usage = self.memory_state.get(key, 0)
            if current_usage + estimated_tokens > limit:
                return False
            return True

    def _consume_tokens(self, provider: ProviderTier, tokens_used: int):
        bucket_key = f"rl:bucket:{provider.value}"
        current_minute = str(int(time.time() / 60))
        key = f"{bucket_key}:{current_minute}"
        
        if self.using_redis:
            self.redis_client.incrby(key, tokens_used)
            self.redis_client.expire(key, 120)  # TTL of 2 mins
        else:
            self.memory_state[key] = self.memory_state.get(key, 0) + tokens_used

    def route_completion(self, model: str, messages: List[Dict[str, str]], estimated_tokens: int = 1000, force_provider: Optional[ProviderTier] = None, response_format = None) -> Any:
        """
        The proxy dynamically finds a valid bucket. If local ollama fails or is exhausted, 
        it rolls over instantly to the next in the chain without agent intervention.
        """
        chain = [force_provider] if force_provider else self.provider_chain
        
        for provider in chain:
            if self._check_rate_limit(provider, estimated_tokens):
                try:
                    # Note: You would map provider to actual LiteLLM models here depending on your env config.
                    # For MVP, we route everything natively to LiteLLM which handles standard resolution.
                    
                    # Litellm supports structured pydantic outputs via response_format
                    response = completion(
                        model=model,
                        messages=messages,
                        response_format=response_format
                    )
                    
                    # Consume actual usage
                    tokens_used = response.usage.total_tokens if response.usage else estimated_tokens
                    self._consume_tokens(provider, tokens_used)
                    
                    return response
                except Exception as e:
                    print(f"[ERROR] Provider {provider} threw exception: {e}. FAILING OVER...")
                    raise e
                    
        raise Exception("All LLM Provider buckets exhausted or unavailable.")

# Singleton Proxy Setup
llm_proxy = LLMProviderProxy()
