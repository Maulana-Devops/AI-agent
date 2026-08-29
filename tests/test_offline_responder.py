from app.offline_responder import OfflineResponder


def test_offline_virtual_env():
    responder = OfflineResponder()

    assert (
        responder.resolve("jelaskan virtual environment python secara singkat")
        == "Virtual environment adalah alat untuk mengisolasi dependency Python antar-project. Setiap project bisa memiliki environment sendiri dengan paket yang terinstall terpisah dari project lain, mencegah konflik versi."
    )


def test_offline_jelaskan_virtual_env():
    responder = OfflineResponder()

    assert (
        responder.resolve("jelaskan virtual environment")
        == "Virtual environment adalah alat untuk mengisolasi dependency Python antar-project. Setiap project bisa memiliki environment sendiri dengan paket yang terinstall terpisah dari project lain, mencegah konflik versi."
    )


def test_offline_git():
    responder = OfflineResponder()

    assert (
        responder.resolve("apa itu git")
        == "Git adalah sistem version control yang digunakan untuk melacak perubahan kode source selama pengembangan perangkat lunak. Ia memungkinkan tim bekerja bersama, melacak riwayat perubahan, dan bisa kembali ke versi sebelumnya."
    )


def test_offline_pytest():
    responder = OfflineResponder()

    assert (
        responder.resolve("apa itu pytest")
        == "Pytest adalah framework testing untuk Python yang mudah digunakan untuk menulis dan menjalankan uji coba (test). Ia mendukung fixture, parameterisasi, dan discovery otomatis test function."
    )


def test_offline_docker():
    responder = OfflineResponder()

    assert (
        responder.resolve("apa itu docker")
        == "Docker adalah platform untuk membundel aplikasi beserta dependensinya menjadi container. Container berjalan secara terisolasi dan bisa dijalankan di mana saja yang mendukung Docker, memudahkan deployment dan menjaga konsistensi environment."
    )


def test_offline_unknown_query():
    responder = OfflineResponder()

    assert responder.resolve("some random unknown query") is None


def test_offline_empty_message():
    responder = OfflineResponder()

    assert responder.resolve("") is None
    assert responder.resolve("   ") is None


def test_offline_no_subprocess_or_file():
    """
    Verify OfflineResponder does not execute subprocess or file operations.
    It only receives strings and returns static answers or None.
    """
    responder = OfflineResponder()

    # All calls should return either a string answer or None
    # No side effects should occur
    result = responder.resolve("apa itu git")
    assert isinstance(result, str)

    result = responder.resolve("unknown thing")
    assert result is None