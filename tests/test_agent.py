from app.agent import LaptopAgent


def test_agent_model():
    agent = LaptopAgent("test-key")

    assert agent.model == "gemini-3.6-flash"
    assert agent.client is not None


def test_agent_ask_accepts_confirmation_flag():
    agent = LaptopAgent("test-key")

    assert agent.ask.__name__ == "ask"
