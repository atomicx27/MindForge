import pytest
from core.proxy import LLMProviderProxy, ProviderTier
from unittest.mock import patch, MagicMock

def test_proxy_failover():
    proxy = LLMProviderProxy()

    # Mocking completion to fail once and succeed on the second try
    with patch("core.proxy.completion") as mock_completion:
        mock_completion.side_effect = [Exception("Mocked error"), MagicMock()]

        response = proxy.route_completion("mock_model", [{"role": "user", "content": "hi"}], estimated_tokens=100)

        # It should have called completion twice (fail on OLLAMA_LOCAL, succeed on OLLAMA_COLAB)
        assert mock_completion.call_count == 2
        assert response is not None

def test_proxy_all_fail():
    proxy = LLMProviderProxy()

    with patch("core.proxy.completion") as mock_completion:
        mock_completion.side_effect = Exception("Mocked error")

        with pytest.raises(Exception, match="All LLM Provider buckets exhausted or unavailable."):
            proxy.route_completion("mock_model", [{"role": "user", "content": "hi"}], estimated_tokens=100)

        assert mock_completion.call_count == 4
