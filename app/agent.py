from pathlib import Path
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.tool_adapter import get_tool_declarations
from app.tool_runner import run_tool


class LaptopAgent:
    """
    Laptop AI Assistant.

    Gemini bertindak sebagai reasoning layer.
    Tool execution dilakukan oleh aplikasi Python.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key tidak boleh kosong.")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.6-flash"

    def _tools(self):
        """
        Return tools yang boleh diketahui Gemini.
        """

        return [
            types.Tool(
                function_declarations=get_tool_declarations()
            )
        ]

    def _config(self):
        """
        Configuration untuk Gemini.
        """

        return types.GenerateContentConfig(
            tools=self._tools(),
            system_instruction=(
                "Kamu adalah Laptop AI Assistant untuk membantu "
                "pekerjaan laptop dan project development.\n\n"

                "Tugas utama kamu adalah membantu pengguna "
                "memahami dan menyelesaikan pekerjaan di laptop.\n\n"

                "Gunakan tools jika informasi aktual dari laptop "
                "diperlukan.\n\n"

                "Jangan mengarang hasil tool.\n"
                "Gunakan hasil tool apa adanya.\n\n"

                "Untuk operasi yang mengubah file, Git, atau sistem, "
                "aplikasi Python akan melakukan pemeriksaan permission "
                "sebelum eksekusi.\n\n"

                "Jika tool menghasilkan error, jelaskan error tersebut "
                "kepada pengguna dengan bahasa yang sederhana."
            ),
        )

    def _extract_function_calls(self, response):
        """
        Mengambil semua function call dari response Gemini.
        """

        function_calls = []

        for candidate in response.candidates or []:

            if not candidate.content:
                continue

            for part in candidate.content.parts or []:

                if part.function_call:
                    function_calls.append(part.function_call)

        return function_calls

    def _build_function_response(self, name: str, result):
        """
        Membuat response dari hasil tool untuk dikirim kembali
        kepada Gemini.

        google-genai versi yang digunakan project ini tidak
        menggunakan parameter id pada from_function_response().
        """

        return types.Part.from_function_response(
            name=name,
            response={
                "result": result,
            },
        )

    def ask(
        self,
        message: str,
        *,
        confirmed: bool = False,
    ) -> str:
        """
        Memproses pesan pengguna.

        Gemini dapat melakukan beberapa putaran tool calling
        sebelum menghasilkan jawaban akhir.

        Tool read-only dapat dijalankan langsung.
        Tool modify hanya dijalankan jika confirmed=True.
        """

        if not message or not message.strip():
            return "Pesan tidak boleh kosong."

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=message.strip()
                    )
                ],
            )
        ]

        # Batas keamanan agar Gemini tidak melakukan tool
        # calling tanpa henti.
        max_rounds = 10

        for round_number in range(1, max_rounds + 1):

            print(f"[ROUND {round_number}]")

            # =====================================================
            # 1. Kirim conversation ke Gemini
            # =====================================================

            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=self._config(),
            )

            # =====================================================
            # 2. Periksa apakah Gemini meminta tool
            # =====================================================

            function_calls = self._extract_function_calls(
                response
            )

            # Tidak ada function call.
            # Berarti Gemini sudah selesai menjawab.
            if not function_calls:

                text = response.text or ""

                if text.strip():
                    return text.strip()

                return (
                    "Gemini tidak menghasilkan jawaban teks."
                )

            # =====================================================
            # 3. Simpan response Gemini yang berisi function call
            # =====================================================

            if not response.candidates:

                return (
                    "Gemini tidak mengembalikan candidate response."
                )

            assistant_content = response.candidates[0].content

            if assistant_content:
                contents.append(assistant_content)

            # =====================================================
            # 4. Jalankan semua tool yang diminta Gemini
            # =====================================================

            function_response_parts = []

            for call in function_calls:

                name = call.name
                args = dict(call.args or {})

                print(f"[TOOL] {name}")
                print(f"[ARGS] {args}")

                # -------------------------------------------------
                # Jalankan tool
                # -------------------------------------------------

                try:

                    result = run_tool(
                        name,
                        args,
                        confirmed=confirmed,
                    )

                    print(f"[RESULT] {result}")

                    tool_result = {
                        "success": True,
                        "result": result,
                    }

                except Exception as exc:

                    error_message = str(exc)

                    print(
                        f"[TOOL ERROR] {error_message}"
                    )

                    tool_result = {
                        "success": False,
                        "error": error_message,
                    }

                # -------------------------------------------------
                # Buat function response
                # -------------------------------------------------

                function_response_parts.append(
                    self._build_function_response(
                        name=name,
                        result=tool_result,
                    )
                )

            # =====================================================
            # 5. Kirim hasil tool kembali ke Gemini
            # =====================================================

            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts,
                )
            )

        # =========================================================
        # 6. Safety limit
        # =========================================================

        return (
            "Saya menghentikan proses karena agent mencapai "
            f"batas maksimum {max_rounds} putaran tool calling."
        )


def main():
    """
    Entry point untuk menjalankan Laptop AI dari terminal.
    """

    # Gunakan path eksplisit agar tidak terkena masalah
    # find_dotenv() ketika dijalankan melalui stdin.
    env_file = Path.cwd() / ".env"

    load_dotenv(env_file)

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY belum diset.\n"
            f"Pastikan file tersedia: {env_file}"
        )

    agent = LaptopAgent(api_key)

    print("=== LAPTOP AI ===")

    result = agent.ask(
        "Cek status Git project saya dan jelaskan secara singkat."
    )

    print()
    print("=== RESPONSE ===")
    print(result)


if __name__ == "__main__":
    main()
