from dotenv import load_dotenv
from google import genai
import os


def main():
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("ERROR: GOOGLE_API_KEY belum diset.")
        return

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Perkenalkan dirimu sebagai AI Assistant untuk membantu pekerjaan laptop dan project development."
    )

    print(response.text)


if __name__ == "__main__":
    main()
