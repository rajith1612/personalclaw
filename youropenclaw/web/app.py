import streamlit as st
from youropenclaw.config import load_config, save_config, DEFAULT_MODELS
from youropenclaw.llm_client import LLMClient
from youropenclaw.agent import Agent
from youropenclaw.skills import list_skills, create_skill, toggle_skill, delete_skill, get_enabled_skills
from youropenclaw.heartbeat import Heartbeat


st.set_page_config(
    page_title="Your OpenClaw",
    page_icon="🦞",
    layout="wide",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .main .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }

    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #ffffff !important;
    }

    .skill-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
    }

    .heartbeat-active {
        color: #00e676 !important;
        font-weight: 600;
    }

    .heartbeat-inactive {
        color: #ff5252 !important;
        font-weight: 600;
    }

    .header-logo {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stStatusWidget"] { display: none; }
</style>
""", unsafe_allow_html=True)


def init_agent():
    config = load_config()
    if not config:
        return None, None
    llm = LLMClient(config["provider"], config["api_key"], config["model"])
    agent = Agent(llm)
    return config, agent


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🦞 Your OpenClaw")
        st.markdown("---")

        config = load_config()

        st.markdown("### ⚙️ LLM Configuration")
        if config:
            st.markdown(f"**Provider:** {config['provider']}")
            st.markdown(f"**Model:** {config['model']}")
            masked_key = config['api_key'][:4] + "****" + config['api_key'][-4:]
            st.markdown(f"**API Key:** `{masked_key}`")
        else:
            st.warning("Not configured yet.")

        with st.expander("Change Configuration", expanded=not bool(config)):
            provider_names = {"openai": "OpenAI", "anthropic": "Anthropic", "google": "Google Gemini", "ollama": "Ollama (local)"}
            provider_list = list(provider_names.keys())
            current_idx = provider_list.index(config["provider"]) if config and config["provider"] in provider_list else 0

            provider = st.selectbox("Provider", provider_list, index=current_idx, format_func=lambda x: provider_names[x])
            model = st.text_input("Model", value=config["model"] if config else DEFAULT_MODELS.get(provider, ""))

            local_providers = {"ollama"}
            if provider in local_providers:
                api_key = "ollama"
                st.caption("No API key needed for local provider.")
            else:
                api_key = st.text_input("API Key", value=config["api_key"] if config and config.get("api_key", "") != "ollama" else "", type="password")

            if st.button("Save Configuration", use_container_width=True):
                if provider and model and (api_key or provider in local_providers):
                    save_config(provider, api_key or "ollama", model)
                    st.success("Configuration saved!")
                    st.rerun()
                else:
                    st.error("All fields are required.")

        st.markdown("---")
        render_skills_sidebar()
        st.markdown("---")
        render_heartbeat_sidebar()


def render_skills_sidebar():
    st.markdown("### 🛠️ Skills")

    skills = list_skills()

    if skills:
        for skill in skills:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                status = "🟢" if skill.get("enabled") else "🔴"
                st.markdown(f"{status} **{skill['name']}**")
                st.caption(skill.get("description", ""))
            with col2:
                if skill.get("enabled"):
                    if st.button("Off", key=f"disable_{skill['file']}", help="Disable skill"):
                        toggle_skill(skill["file"], False)
                        st.rerun()
                else:
                    if st.button("On", key=f"enable_{skill['file']}", help="Enable skill"):
                        toggle_skill(skill["file"], True)
                        st.rerun()
            with col3:
                if st.button("🗑️", key=f"delete_{skill['file']}", help="Delete skill"):
                    delete_skill(skill["file"])
                    st.rerun()
    else:
        st.caption("No skills created yet.")

    with st.expander("Create New Skill"):
        skill_name = st.text_input("Skill name", key="new_skill_name")
        skill_desc = st.text_input("Description", key="new_skill_desc")
        skill_prompt = st.text_area("Instructions (what the agent should do)", key="new_skill_prompt", height=100)
        skill_schedule = st.number_input("Schedule (minutes)", min_value=1, value=60, key="new_skill_schedule")

        if st.button("Create Skill", use_container_width=True):
            if skill_name and skill_prompt:
                create_skill(skill_name, skill_desc, skill_prompt, schedule=skill_schedule)
                st.success(f"Skill '{skill_name}' created!")
                st.rerun()
            else:
                st.error("Name and instructions are required.")


def render_heartbeat_sidebar():
    st.markdown("### 💓 Heartbeat")

    if "heartbeat" not in st.session_state:
        st.session_state.heartbeat = None

    hb = st.session_state.heartbeat

    if hb and hb.running:
        st.markdown('<span class="heartbeat-active">● Running</span>', unsafe_allow_html=True)
        if st.button("Stop Heartbeat", use_container_width=True):
            hb.stop()
            st.rerun()
    else:
        st.markdown('<span class="heartbeat-inactive">● Stopped</span>', unsafe_allow_html=True)
        if st.button("Start Heartbeat", use_container_width=True):
            if "agent" in st.session_state and st.session_state.agent:
                hb = Heartbeat(st.session_state.agent, get_enabled_skills)
                hb.start()
                st.session_state.heartbeat = hb
                st.rerun()
            else:
                st.error("Configure LLM settings first.")

    enabled = get_enabled_skills()
    if enabled:
        st.caption(f"{len(enabled)} active skill(s)")
        for s in enabled:
            st.caption(f"  • {s['name']} (every {s['schedule']}m)")

    if hb and hb.logs:
        with st.expander("Heartbeat Log"):
            for log in reversed(hb.logs[-20:]):
                st.text(log)


def ensure_agent():
    config = load_config()
    if not config:
        return None

    if "agent" not in st.session_state or st.session_state.agent is None:
        with st.spinner("Initializing agent..."):
            _, agent = init_agent()
            st.session_state.agent = agent
            st.session_state.config_snapshot = config

    if st.session_state.get("config_snapshot") != config:
        with st.spinner("Reinitializing agent..."):
            _, agent = init_agent()
            st.session_state.agent = agent
            st.session_state.config_snapshot = config

    return st.session_state.agent


def render_chat():
    config = load_config()
    if not config:
        st.info("👈 Please configure your LLM settings in the sidebar to start chatting.")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask your agent anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        agent = ensure_agent()
        if not agent:
            st.error("Failed to initialize agent. Check your configuration.")
            return

        with st.chat_message("assistant"):
            status_container = st.status("Thinking...", expanded=True)

            def update_status(msg):
                status_container.update(label=msg)
                status_container.write(msg)

            try:
                response = agent.run(prompt, status_callback=update_status)
            except Exception as e:
                response = f"Error: {e}"

            status_container.update(label="Done", state="complete", expanded=False)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    render_sidebar()

    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("# 🦞 Your OpenClaw")
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            if "agent" in st.session_state and st.session_state.agent:
                st.session_state.agent.reset()
            st.rerun()

    config = load_config()
    if config:
        st.caption(f"Connected to **{config['provider']}** / `{config['model']}`")

    st.markdown("---")
    render_chat()


if __name__ == "__main__":
    main()
