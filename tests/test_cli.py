from unittest.mock import MagicMock, patch

from io import StringIO

from app.cli import (
    load_api_key,
    try_load_api_key,
    run_local_router,
)
from app.local_router import LocalRouter
from app.offline_responder import OfflineResponder


def test_cli_module_imports():
    assert callable(load_api_key)
    assert callable(try_load_api_key)
    assert callable(run_local_router)


def test_local_router_can_handle_directory():
    router = LocalRouter()

    assert router.resolve("cek directory") == "get_current_directory"


def test_local_router_unknown_intent():
    router = LocalRouter()

    assert router.resolve("buatkan laporan ekonomi") is None


# ---- OfflineResponder routing tests ----

def test_cli_routing_git_via_offline():
    """A. Input 'apa itu git' -> OfflineResponder digunakan, Gemini tidak dipanggil."""
    with patch("app.cli.OfflineResponder.resolve", return_value="Git adalah sistem version control yang digunakan untuk melacak perubahan kode source selama pengembangan perangkat lunak. Ia memungkinkan tim bekerja bersama, melacak riwayat perubahan, dan bisa kembali ke versi sebelumnya.") as mock_resolve:
        with patch("app.cli.LaptopAgent") as mock_agent_cls:
            mock_agent = MagicMock()
            mock_agent.ask.return_value = "Gemini response"
            mock_agent_cls.return_value = mock_agent

            with patch("builtins.input", side_effect=["apa itu git", "exit"]):
                old_stdout = StringIO()
                with patch("sys.stdout", old_stdout):
                    from app.cli import main
                    try:
                        main()
                    except SystemExit:
                        pass

                    output = old_stdout.getvalue()

                    assert "Git adalah sistem version control" in output
                    mock_resolve.assert_called_once_with("apa itu git")
                    mock_agent.ask.assert_not_called()


def test_cli_routing_pytest_via_offline():
    """B. Input 'apa itu pytest' -> OfflineResponder digunakan, Gemini tidak dipanggil."""
    with patch("app.cli.OfflineResponder.resolve", return_value="Pytest adalah framework testing untuk Python yang mudah digunakan untuk menulis dan menjalankan uji coba (test). Ia mendukung fixture, parameterisasi, dan discovery otomatis test function.") as mock_resolve:
        with patch("app.cli.LaptopAgent") as mock_agent_cls:
            mock_agent = MagicMock()
            mock_agent.ask.return_value = "Gemini response"
            mock_agent_cls.return_value = mock_agent

            with patch("builtins.input", side_effect=["apa itu pytest", "exit"]):
                old_stdout = StringIO()
                with patch("sys.stdout", old_stdout):
                    from app.cli import main
                    try:
                        main()
                    except SystemExit:
                        pass

                    output = old_stdout.getvalue()

                    assert "Pytest adalah framework testing" in output
                    mock_resolve.assert_called_once_with("apa itu pytest")
                    mock_agent.ask.assert_not_called()


def test_cli_routing_docker_via_offline():
    """C. Input 'apa itu docker' -> OfflineResponder digunakan, Gemini tidak dipanggil."""
    with patch("app.cli.OfflineResponder.resolve", return_value="Docker adalah platform untuk membundel aplikasi beserta dependensinya menjadi container. Container berjalan secara terisolasi dan bisa dijalankan di mana saja yang mendukung Docker, memudahkan deployment dan menjaga konsistensi environment.") as mock_resolve:
        with patch("app.cli.LaptopAgent") as mock_agent_cls:
            mock_agent = MagicMock()
            mock_agent.ask.return_value = "Gemini response"
            mock_agent_cls.return_value = mock_agent

            with patch("builtins.input", side_effect=["apa itu docker", "exit"]):
                old_stdout = StringIO()
                with patch("sys.stdout", old_stdout):
                    from app.cli import main
                    try:
                        main()
                    except SystemExit:
                        pass

                    output = old_stdout.getvalue()

                    assert "Docker adalah platform" in output
                    mock_resolve.assert_called_once_with("apa itu docker")
                    mock_agent.ask.assert_not_called()


def test_cli_unknown_query_to_gemini():
    """D. Input unknown yang tidak dikenali OfflineResponder -> diteruskan ke Gemini."""
    with patch("app.cli.OfflineResponder.resolve", return_value=None) as mock_resolve:
        with patch("app.cli.LaptopAgent") as mock_agent_cls:
            mock_agent = MagicMock()
            mock_agent.ask.return_value = "Gemini answer for unknown query"
            mock_agent_cls.return_value = mock_agent

            with patch("builtins.input", side_effect=["some random unknown query", "exit"]):
                old_stdout = StringIO()
                with patch("sys.stdout", old_stdout):
                    from app.cli import main
                    try:
                        main()
                    except SystemExit:
                        pass

                    output = old_stdout.getvalue()

                    assert "Gemini answer for unknown query" in output
                    mock_resolve.assert_called_once_with("some random unknown query")
                    mock_agent.ask.assert_called_once()


def test_cli_local_router_prioritized_before_offline():
    """E. LocalRouter intent diprioritaskan sebelum OfflineResponder."""
    with patch("app.cli.run_local_router", return_value=True):
        with patch("app.cli.OfflineResponder.resolve") as mock_resolve:
            with patch("app.cli.LaptopAgent") as mock_agent_cls:
                mock_agent = MagicMock()
                mock_agent_cls.return_value = mock_agent

                with patch("builtins.input", side_effect=["apa itu git", "exit"]):
                    old_stdout = StringIO()
                    with patch("sys.stdout", old_stdout):
                        from app.cli import main
                        try:
                            main()
                        except SystemExit:
                            pass

                        # OfflineResponder should NOT be called because LocalRouter took priority
                        mock_resolve.assert_not_called()
                        mock_agent.ask.assert_not_called()