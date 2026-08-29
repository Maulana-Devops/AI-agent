from app.local_router import LocalRouter


def test_router_git_status():
    router = LocalRouter()

    assert router.resolve("cek status git") == "git_status"
    assert router.resolve("lihat status git") == "git_status"


def test_router_git_branch():
    router = LocalRouter()

    assert router.resolve("lihat branch") == "git_branch"


def test_router_git_diff():
    router = LocalRouter()

    assert router.resolve("lihat perubahan") == "git_diff"


def test_router_git_log():
    router = LocalRouter()

    assert router.resolve("lihat commit") == "git_log"


def test_router_git_remote():
    router = LocalRouter()

    assert router.resolve("cek remote") == "git_remote"


def test_router_directory():
    router = LocalRouter()

    assert router.resolve("cek directory") == "get_current_directory"
    assert router.resolve("cek folder") == "get_current_directory"


def test_router_unknown_intent():
    router = LocalRouter()

    assert router.resolve("jelaskan virtual environment") is None


def test_router_cek_remote_repository():
    router = LocalRouter()

    assert router.resolve("cek remote repository") == "git_remote"


def test_router_bagaimana_status_repository():
    router = LocalRouter()

    assert router.resolve("bagaimana status repository") == "git_status"


def test_router_lihat_perubahan_repository():
    router = LocalRouter()

    assert router.resolve("lihat perubahan repository") is None


def test_router_jelaskan_virtual_environment():
    router = LocalRouter()

    assert router.resolve("jelaskan virtual environment") is None


def test_router_apa_yang_berubah():
    router = LocalRouter()

    assert router.resolve("apa yang berubah") == "git_diff"


def test_router_branch_apa_yang_sedang_aktif():
    router = LocalRouter()

    assert router.resolve("branch apa yang sedang aktif") == "git_branch"


def test_router_saya_ada_di_folder_mana():
    router = LocalRouter()

    assert router.resolve("saya ada di folder mana") == "get_current_directory"


def test_router_empty_message():
    router = LocalRouter()

    assert router.resolve("") is None
    assert router.resolve("   ") is None
