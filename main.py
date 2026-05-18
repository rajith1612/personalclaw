import subprocess
import sys
from youropenclaw.config import load_config, run_setup
from youropenclaw.llm_client import LLMClient
from youropenclaw.agent import Agent


def start_agent(config):
    llm = LLMClient(config["provider"], config["api_key"], config["model"])
    agent = Agent(llm)

    print(f"\nAgent ready. Provider: {config['provider']}, Model: {config['model']}")
    print("Commands: 'quit' to exit, 'reset' to clear history, 'config' to reconfigure.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            break
        if user_input.lower() == "reset":
            agent.reset()
            print("Conversation history cleared.\n")
            continue
        if user_input.lower() == "config":
            config = run_setup(force=True)
            llm = LLMClient(config["provider"], config["api_key"], config["model"])
            agent = Agent(llm)
            print(f"\nReconfigured. Provider: {config['provider']}, Model: {config['model']}\n")
            continue

        try:
            response = agent.run(user_input)
            print(f"\nAgent: {response}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


def start_web():
    from pathlib import Path
    app_path = Path(__file__).parent / "youropenclaw" / "web" / "app.py"
    print("\nLaunching web interface...\n")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])


def main():
    print("\n🦞 Your OpenClaw\n")

    config = load_config()

    if not config:
        print("No configuration found. Starting setup...\n")
        config = run_setup(force=True)

    print("  1. Start Agent (CLI)")
    print("  2. Start Agent (Web)")
    print("  3. Configure")

    choice = ""
    while choice not in ("1", "2", "3"):
        choice = input("\nSelect an option (1/2/3): ").strip()

    if choice == "1":
        config = load_config()
        if not config:
            print("\nNo LLM settings found. Please configure first.\n")
            config = run_setup(force=True)
        else:
            print(f"\nUsing: {config['provider']} / {config['model']}")
        start_agent(config)
    elif choice == "2":
        config = load_config()
        if not config:
            print("\nNo LLM settings found. Please configure first.\n")
            run_setup(force=True)
        start_web()
    else:
        config = run_setup(force=True)
        print("\nConfiguration saved. Run again to start the agent.\n")


if __name__ == "__main__":
    main()

