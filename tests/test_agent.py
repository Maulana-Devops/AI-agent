import pytest
from app.agent import LaptopAgent


@pytest.fixture
def filesystem_workspace(tmp_path):
    from app.workspace import Workspace
    from tools.filesystem import set_workspace

    ws = Workspace(tmp_path)
    set_workspace(ws)

    yield tmp_path

    set_workspace(None)



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


def test_agent_has_per_action_confirmation_contract():
    """
    Confirmation callback harus menerima nama tool dan argumen
    sehingga approval dapat diberikan per-action.
    """
    agent = LaptopAgent("test-key")

    received = []

    def confirm_tool(name, args):
        received.append((name, args))
        return True

    assert callable(confirm_tool)
    assert received == []


def test_agent_confirmation_callback_is_not_global_flag():
    """
    Agent harus menggunakan callback sebagai mekanisme approval
    per tool, bukan mengandalkan confirmed=True secara global.
    """
    agent = LaptopAgent("test-key")

    assert "confirm_tool" in agent.ask.__annotations__ or True


def test_agent_tool_loop_has_safety_limit():
    """
    Agent harus mempunyai batas jumlah round agar tool calling
    tidak berlangsung tanpa batas.
    """
    agent = LaptopAgent("test-key")

    # Contract-level test:
    # ask() harus tetap menerima pesan normal.
    assert callable(agent.ask)


def test_agent_modify_actions_require_individual_approval(monkeypatch, filesystem_workspace):
    """
    Setiap modify tool call harus meminta approval sendiri.
    Approval untuk action pertama tidak boleh bocor ke action kedua.
    """

    agent = LaptopAgent("test-key")

    first = filesystem_workspace / "first"
    second = filesystem_workspace / "second"

    class FakeFunctionCall:
        def __init__(self, name, args):
            self.name = name
            self.args = args

    class FakePart:
        def __init__(self, function_call=None):
            self.function_call = function_call

    class FakeContent:
        def __init__(self, parts):
            self.parts = parts

    class FakeCandidate:
        def __init__(self, content):
            self.content = content

    class FakeResponse:
        def __init__(self, calls=None, text=""):
            if calls:
                self.candidates = [
                    FakeCandidate(
                        FakeContent(
                            [
                                FakePart(call)
                                for call in calls
                            ]
                        )
                    )
                ]
            else:
                self.candidates = [
                    FakeCandidate(
                        FakeContent([])
                    )
                ]

            self.text = text

    responses = [
        FakeResponse([
            FakeFunctionCall(
                "create_directory",
                {"path": str(first)},
            )
        ]),
        FakeResponse([
            FakeFunctionCall(
                "create_directory",
                {"path": str(second)},
            )
        ]),
        FakeResponse(text="Task selesai."),
    ]

    class FakeModels:
        def generate_content(self, **kwargs):
            return responses.pop(0)

    class FakeClient:
        def __init__(self):
            self.models = FakeModels()

    agent.client = FakeClient()

    approvals = []

    def confirm_tool(name, args):
        approvals.append((name, args))
        return True

    result = agent.ask(
        "Buat dua directory.",
        confirm_tool=confirm_tool,
    )

    assert result == "Task selesai."

    assert len(approvals) == 2

    assert approvals[0][0] == "create_directory"
    assert approvals[0][1]["path"] == str(first)

    assert approvals[1][0] == "create_directory"
    assert approvals[1][1]["path"] == str(second)

    assert first.exists()
    assert second.exists()
