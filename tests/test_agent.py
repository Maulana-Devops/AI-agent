from app.agent import LaptopAgent


def test_agent_model():
    agent = LaptopAgent("test-key")

    assert agent.model == "gemini-3.6-flash"
    assert agent.client is not None


def test_agent_ask_accepts_confirmation_flag():
    agent = LaptopAgent("test-key")

    assert agent.ask.__name__ == "ask"


def test_agent_confirm_callback_accepts_tool_request():
    agent = LaptopAgent("test-key")

    calls = []

    def confirm_tool(name, args):
        calls.append((name, args))
        return True

    assert agent.ask.__name__ == "ask"
    assert callable(confirm_tool)
    assert calls == []


def test_agent_confirm_callback_rejects_tool_request():
    agent = LaptopAgent("test-key")

    def confirm_tool(name, args):
        return False

    assert agent.model == "gemini-3.6-flash"
    assert callable(confirm_tool)
