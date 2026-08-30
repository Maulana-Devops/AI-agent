import os
from pathlib import Path

from dotenv import load_dotenv

from app.agent import LaptopAgent
from app.local_router import LocalRouter
from app.offline_responder import OfflineResponder


def load_api_key() -> str:
    """
    Load GOOGLE_API_KEY dari file .env project.
    """
    env_file = Path.cwd() / ".env"
    load_dotenv(env_file)

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY belum diset di .env"
        )

    return api_key


def try_load_api_key() -> str | None:
    """
    Coba mengambil API key tanpa membuat CLI gagal.

    Jika .env atau API key tidak tersedia, return None.
    """
    try:
        return load_api_key()
    except RuntimeError:
        return None


def run_local_router(router: LocalRouter, message: str) -> bool:
    """
    Jalankan Local Router jika intent dikenali.

    Return:
        True  -> intent berhasil dikenali dan diproses
        False -> intent tidak dikenali
    """
    result = router.run(message)

    if result is None:
        return False

    tool_name, execution = result

    print(f"\n[LOCAL TOOL] {tool_name}")

    if execution.output:
        print(execution.output)

    if execution.message:
        print(execution.message)

    print()

    return True


def main():
    print("=== LAPTOP AI ===")
    print("AI Assistant untuk laptop dan project development.")
    print("Ketik 'exit' atau 'quit' untuk keluar.")
    print()

    # Local Router selalu tersedia, bahkan tanpa Gemini API.
    local_router = LocalRouter()

    # Gemini bersifat optional.
    api_key = try_load_api_key()

    agent = None

    if api_key:
        try:
            agent = LaptopAgent(api_key)
            print("[SYSTEM] Gemini AI: READY")
        except Exception as exc:
            print(f"[SYSTEM] Gemini AI tidak tersedia: {exc}")
    else:
        print("[SYSTEM] Gemini AI: OFFLINE")
        print("[SYSTEM] Local Router tetap tersedia.")

    print()

    while True:
        try:
            message = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

        if not message:
            continue

        if message.lower() in {"exit", "quit"}:
            print("Bye.")
            break

        # ---------------------------------------------------------
        # ROUTE 1: LOCAL ROUTER
        # ---------------------------------------------------------
        #
        # Tugas sederhana seperti:
        #   cek status git
        #   cek directory
        #   lihat branch
        #   lihat perubahan
        #
        # tidak perlu memanggil Gemini.
        #
        try:
            if run_local_router(local_router, message):
                continue
        except Exception as exc:
            print(f"\n[LOCAL ERROR] {exc}\n")

        # ---------------------------------------------------------
        # ROUTE 2: OFFLINE RESPONDER
        # ---------------------------------------------------------
        #
        # Jika Local Router tidak mengenali intent,
        # coba jawab dengan lokal knowledge terlebih dahulu.
        #
        try:
            offline_answer = OfflineResponder().resolve(message)

            if offline_answer is not None:
                print(f"\nAI: {offline_answer}\n")
                continue
        except Exception as exc:
            print(f"\n[OFFLINE ERROR] {exc}\n")

        # ---------------------------------------------------------
        # ROUTE 3: GEMINI
        # ---------------------------------------------------------

        if agent is None:
            print(
                "\nAI: Gemini tidak tersedia dan "
                "Local Router serta Offline Responder "
                "tidak mengenali perintah tersebut.\n"
            )
            continue

        try:
            response = agent.ask(
                message,
                confirm_tool=confirm_tool_execution,
            )

            print(f"\nAI: {response}\n")

        except Exception as exc:
            # -----------------------------------------------------
            # ROUTE 4: GEMINI FAILED -> LOCAL FALLBACK
            # -----------------------------------------------------

            print(f"\n[GEMINI ERROR] {exc}")

            try:
                if run_local_router(local_router, message):
                    print("[FALLBACK] Local Router berhasil menangani perintah.")
                    continue
            except Exception as local_exc:
                print(f"[LOCAL FALLBACK ERROR] {local_exc}")

            print(
                "\nAI: Gemini gagal memproses permintaan dan "
                "Local Router juga tidak mengenali perintah tersebut.\n"
            )


if __name__ == "__main__":
    main()


def confirm_tool_execution(
    tool_name: str,
    arguments: dict,
) -> bool:
    """
    Minta konfirmasi pengguna sebelum menjalankan tool modify.
    """

    print()
    print("=" * 60)
    print("[CONFIRMATION REQUIRED]")
    print("=" * 60)
    print(f"Tool : {tool_name}")
    print("Risk : MODIFY")

    print("\nArguments:")
    if arguments:
        for key, value in arguments.items():
            print(f"  {key}: {value}")
    else:
        print("  (none)")

    print()
    print("Tool ini dapat mengubah file, data, atau sistem.")
    print()

    try:
        answer = input("Lanjutkan? [y/N]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nOperasi dibatalkan.")
        return False

    approved = answer in {"y", "yes"}

    if approved:
        print("[CONFIRMATION] Disetujui.")
    else:
        print("[CONFIRMATION] Ditolak.")

    print()

    return approved
