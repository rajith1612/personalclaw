import json
from pathlib import Path


CONFIG_DIR = Path.home() / ".youropenclaw"
CONFIG_FILE = CONFIG_DIR / "config.json"

PROVIDERS = {
    "1": "openai",
    "2": "anthropic",
    "3": "google",
    "4": "ollama",
}

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-sonnet-4-20250514",
    "google": "gemini-2.0-flash",
    "ollama": "llama3.2",
}

LOCAL_PROVIDERS = {"ollama"}


def load_config():
    if not CONFIG_FILE.exists():
        return None
    try:
        data = json.loads(CONFIG_FILE.read_text())
        provider = data.get("provider")
        api_key = data.get("api_key", "")
        model = data.get("model")
        if provider and model and (api_key or provider in LOCAL_PROVIDERS):
            return {"provider": provider, "api_key": api_key, "model": model}
    except (json.JSONDecodeError, OSError):
        pass
    return None


def save_config(provider, api_key, model):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = {"provider": provider, "api_key": api_key, "model": model}
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def run_setup(force=False):
    existing = load_config()
    if existing and not force:
        return existing

    current_provider = existing.get("provider") if existing else None
    current_api_key = existing.get("api_key") if existing else None
    current_model = existing.get("model") if existing else None

    print("\n--- Agent Setup ---\n")
    print("Select LLM provider:")
    print("  1. OpenAI")
    print("  2. Anthropic")
    print("  3. Google Gemini")
    print("  4. Ollama (local)")

    if current_provider:
        reverse_map = {v: k for k, v in PROVIDERS.items()}
        current_choice = reverse_map.get(current_provider, "")
        prompt = f"\nEnter choice (1/2/3/4) [{current_provider}]: "
    else:
        current_choice = ""
        prompt = "\nEnter choice (1/2/3/4): "

    choice = ""
    while True:
        choice = input(prompt).strip()
        if not choice and current_choice:
            choice = current_choice
        if choice in PROVIDERS:
            break

    provider = PROVIDERS[choice]

    if provider == current_provider and current_model:
        default_model = current_model
    else:
        default_model = DEFAULT_MODELS.get(provider, "")
    model_input = input(f"Enter model name [{default_model}]: ").strip()
    model = model_input if model_input else default_model

    if provider in LOCAL_PROVIDERS:
        api_key = "ollama"
        print("(No API key needed for local provider)")
    elif current_api_key and current_api_key != "ollama":
        masked = current_api_key[:4] + "****" + current_api_key[-4:]
        api_key_input = input(f"Enter API key [{masked}]: ").strip()
        api_key = api_key_input if api_key_input else current_api_key
    else:
        api_key = input("Enter API key: ").strip()

    save_config(provider, api_key, model)

    return {"provider": provider, "api_key": api_key, "model": model}
