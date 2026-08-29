from app.agent import LaptopAgent


def test_agent_model():
    agent = LaptopAgent("test-key")

    assert agent.model == "gemini-3.6-flash"
    assert agent.client is not None
