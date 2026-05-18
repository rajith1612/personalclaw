from langchain.chat_models import init_chat_model


PROVIDER_MAP = {
    "openai": "openai",
    "anthropic": "anthropic",
    "google": "google_genai",
    "ollama": "ollama",
}

LOCAL_PROVIDERS = {"ollama"}


class LLMClient:

    def __init__(self, provider, api_key, model):
        langchain_provider = PROVIDER_MAP.get(provider, provider)

        if provider in LOCAL_PROVIDERS:
            self.llm = init_chat_model(
                model=model,
                model_provider=langchain_provider,
            )
        else:
            self.llm = init_chat_model(
                model=model,
                model_provider=langchain_provider,
                api_key=api_key,
            )

    def bind_tools(self, tools):
        self.llm_with_tools = self.llm.bind_tools(tools)

    def invoke(self, messages):
        return self.llm_with_tools.invoke(messages)

