from dataclasses import dataclass

from app.orchestrator import AgentOrchestrator


@dataclass
class LocalRoute:
    tool_name: str
    message: str


class LocalRouter:
    """
    Router lokal untuk tugas-tugas sederhana pada laptop.

    Router ini tidak menggunakan Gemini/API.
    Ia hanya mengenali intent sederhana dan meneruskannya
    ke AgentOrchestrator yang menangani permission dan execution.
    """

    def __init__(self):
        self.orchestrator = AgentOrchestrator()

        self.routes = {
            # Filesystem
            "get_current_directory": (
                "cek directory",
                "cek direktori",
                "lihat directory",
                "lihat direktori",
                "cek folder",
                "lihat folder",
                "current directory",
                "working directory",
                "dimana saya",
                "di mana saya",
                "pwd",
                "dir",
                "saya ada di folder mana",
            ),

            # Git status
            "git_status": (
                "cek status git",
                "lihat status git",
                "status git",
                "cek git status",
                "git status",
                "bagaimana status repository",
            ),

            # Git branch
            "git_branch": (
                "lihat branch",
                "cek branch",
                "lihat branches",
                "cek branches",
                "branch git",
                "git branch",
                "branch apa yang sedang aktif",
            ),

            # Git diff
            "git_diff": (
                "lihat perubahan",
                "cek perubahan",
                "lihat perubahan git",
                "cek perubahan git",
                "git diff",
                "lihat diff",
                "berubah",
            ),

            # Git log
            "git_log": (
                "lihat commit",
                "cek commit",
                "lihat commits",
                "cek commits",
                "lihat history git",
                "cek history git",
                "lihat riwayat git",
                "cek riwayat git",
                "git log",
            ),

            # Git remote
            "git_remote": (
                "cek remote",
                "lihat remote",
                "cek git remote",
                "lihat git remote",
                "git remote",
            ),
        }

    def resolve(self, message: str) -> str | None:
        """
        Resolve user message menjadi nama tool.

        Matching dilakukan secara sederhana dan konservatif.
        Jika intent tidak dikenali, return None.
        """
        normalized = " ".join(message.lower().strip().split())

        if not normalized:
            return None

        # Exact match terlebih dahulu.
        for tool_name, phrases in self.routes.items():
            if normalized in phrases:
                return tool_name

        # Kemudian partial match.
        for tool_name, phrases in self.routes.items():
            for phrase in phrases:
                if phrase in normalized and not (
                    tool_name == "git_diff" and "repository" in normalized.split()
                ):
                    return tool_name

        return None

    def run(self, message: str):
        """
        Resolve intent kemudian jalankan tool melalui orchestrator.
        """
        tool_name = self.resolve(message)

        if tool_name is None:
            return None

        result = self.orchestrator.run(
            self._tool_to_command(tool_name)
        )

        return tool_name, result

    @staticmethod
    def _tool_to_command(tool_name: str) -> str:
        """
        Mapping tool internal ke command yang dikenali
        oleh permission/orchestrator layer.
        """

        commands = {
            "get_current_directory": "pwd",
            "git_status": "git status",
            "git_branch": "git branch",
            "git_diff": "git diff",
            "git_log": "git log",
            "git_remote": "git remote -v",
        }

        try:
            return commands[tool_name]
        except KeyError:
            raise ValueError(
                f"Tool lokal tidak memiliki command mapping: {tool_name}"
            )


def main():
    router = LocalRouter()

    print("=== LOCAL ROUTER ===")
    print("Local fallback untuk tugas laptop sederhana.")
    print("Ketik 'exit' atau 'quit' untuk keluar.")

    while True:
        try:
            message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if message.lower() in {"exit", "quit"}:
            print("Bye.")
            break

        if not message:
            continue

        result = router.run(message)

        if result is None:
            print("Local Router: Intent belum dikenali.")
            continue

        tool_name, execution = result

        print(f"\n[LOCAL TOOL] {tool_name}")

        if execution.output:
            print(execution.output)

        if execution.message:
            print(execution.message)


if __name__ == "__main__":
    main()
