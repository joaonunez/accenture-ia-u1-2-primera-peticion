import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_data_tst(pregunta: str) -> dict:
    api_key = os.getenv("API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("No se encontro API_KEY ni GEMINI_API_KEY en el archivo .env")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-flash-latest:generateContent"
    )
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": pregunta,
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)
    if not response.ok:
        raise RuntimeError(
            f"Gemini respondio HTTP {response.status_code}: {response.text}"
        )
    return response.json()


if __name__ == "__main__":
    try:
        respuesta = get_data_tst("Hola, ¿cómo estás?")
        print(respuesta["candidates"][0]["content"]["parts"][0]["text"])
    except requests.exceptions.Timeout:
        print("Gemini no respondió a tiempo. Intenta nuevamente más tarde.")
    except requests.exceptions.RequestException as error:
        print(f"No se pudo conectar con Gemini: {error}")
    except RuntimeError as error:
        print(f"Error de Gemini: {error}")
