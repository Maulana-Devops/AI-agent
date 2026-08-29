class OfflineResponder:
    """
    Offline Response Layer untuk knowledge sederhana.

    Ketika Gemini tidak tersedia (misal quota 429),
    komponen ini dapat menjawab pertanyaan pengetahuan umum
    tentang Python, Git, testing, dan Docker tanpa API.
    """

    def resolve(self, message: str) -> str | None:
        """
        Resolve message menjadi jawaban singkat atau None.

        Jika pesan tidak dikenali, return None sehingga
        bisa diteruskan ke Gemini.
        """
        if not message or not message.strip():
            return None

        normalized = " ".join(message.strip().lower().split())

        # Pertanyaan tentang virtual environment Python
        if "jelaskan virtual environment" in normalized:
            return (
                "Virtual environment adalah alat untuk mengisolasi "
                "dependency Python antar-project. Setiap project "
                "bisa memiliki environment sendiri dengan paket "
                "yang terinstall terpisah dari project lain, "
                "mencegah konflik versi."
            )

        # Pertanyaan tentang Git
        if normalized == "apa itu git" or normalized.startswith("apa itu git"):
            return (
                "Git adalah sistem version control yang digunakan "
                "untuk melacak perubahan kode source selama "
                "pengembangan perangkat lunak. Ia memungkinkan "
                "tim bekerja bersama, melacak riwayat perubahan, "
                "dan bisa kembali ke versi sebelumnya."
            )

        # Pertanyaan tentang pytest
        if normalized == "apa itu pytest" or normalized.startswith("apa itu pytest"):
            return (
                "Pytest adalah framework testing untuk Python yang "
                "mudah digunakan untuk menulis dan menjalankan "
                "uji coba (test). Ia mendukung fixture, parameterisasi, "
                "dan discovery otomatis test function."
            )

        # Pertanyaan tentang Docker
        if normalized == "apa itu docker" or normalized.startswith("apa itu docker"):
            return (
                "Docker adalah platform untuk membundel aplikasi "
                "beserta dependensinya menjadi container. Container "
                "berjalan secara terisolasi dan bisa dijalankan "
                "di mana saja yang mendukung Docker, memudahkan "
                "deployment dan menjaga konsistensi environment."
            )

        return None