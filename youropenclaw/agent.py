from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from youropenclaw.tools import TOOL_DEFINITIONS, execute_tool


SYSTEM_PROMPT = """You are Your OpenClaw, a personal AI assistant inspired by the OpenClaw project. You have access to tools for interacting with the local file system and running shell commands.

Your capabilities:
- **Tools**: read_file, write_file, list_directory, run_shell — use them when the user's request requires file or system operations.
- **Heartbeat**: You have a heartbeat system that runs in the background on a configurable schedule. When active, it periodically executes enabled skills automatically. Users can start/stop the heartbeat from the web interface sidebar.
- **Skills**: Reusable instruction sets stored as markdown files in ~/.youropenclaw/skills/. Each skill has a name, description, schedule interval (in minutes), and an enabled/disabled toggle. When the heartbeat is running, it executes enabled skills at their configured intervals. Users can create, enable, disable, and delete skills from the web interface.
- **Configuration**: Your LLM provider, model, and API key are stored in ~/.youropenclaw/config.json in the user's home directory.

Provide clear, direct answers. When you use a tool, explain what you did and share the relevant results."""

MAX_ITERATIONS = 10


class Agent:

    def __init__(self, llm_client):
        self.llm = llm_client
        self.llm.bind_tools(TOOL_DEFINITIONS)
        self.messages = [SystemMessage(content=SYSTEM_PROMPT)]

    def reset(self):
        self.messages = [SystemMessage(content=SYSTEM_PROMPT)]

    def run(self, user_input, status_callback=None):
        self.messages.append(HumanMessage(content=user_input))

        for i in range(MAX_ITERATIONS):
            if status_callback:
                status_callback(f"Calling LLM (step {i + 1})...")

            try:
                response = self.llm.invoke(self.messages)
            except Exception as e:
                error_msg = f"LLM error: {e}"
                if status_callback:
                    status_callback(error_msg)
                return error_msg

            self.messages.append(response)

            if not response.tool_calls:
                return self._extract_text(response.content)

            for tc in response.tool_calls:
                tool_name = tc["name"]
                if status_callback:
                    status_callback(f"Running tool: {tool_name}...")

                try:
                    result = execute_tool(tool_name, tc["args"])
                except Exception as e:
                    result = f"Tool error: {e}"

                self.messages.append(ToolMessage(
                    content=result,
                    tool_call_id=tc["id"],
                ))

        return "Reached maximum iterations. Please try a simpler request."

    @staticmethod
    def _extract_text(content):
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, str):
                    parts.append(block)
                elif isinstance(block, dict) and "text" in block:
                    parts.append(block["text"])
            return "\n".join(parts)
        return str(content)

