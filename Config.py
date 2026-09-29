"""
Configuración central del LLM.
Cambia de proveedor editando PROVIDER en tu archivo .env, sin tocar el código.

Ejemplos en .env:
    PROVIDER=groq                -> usa solo Groq
    PROVIDER=gemini              -> usa solo Gemini
    PROVIDER=groq,gemini         -> usa Groq y, si falla (ej. cuota agotada), pasa a Gemini
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Proveedores disponibles: variable de la key, modelo por defecto y URL
PROVIDERS = {
    "groq": {
        "key_env": "GROQ_API_KEY",
        "model": "llama-3.3-70b-versatile",
        "base_url": "https://api.groq.com/openai/v1",
    },
    "gemini": {
        "key_env": "GEMINI_API_KEY",
        "model": "gemini-3.8-flash",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
    },
    "openai": {
        "key_env": "OPENAI_API_KEY",
        "model": "gpt-4.1-mini",
        "base_url": None,  # OpenAI usa su URL por defecto
    },
}


def build_config(name):
    """Arma la configuración de un proveedor. Devuelve None si no hay key en el .env."""
    provider = PROVIDERS[name]
    api_key = os.getenv(provider["key_env"])
    if not api_key:
        return None

    # El modelo se puede cambiar desde el .env, ej: GROQ_MODEL=otro-modelo
    model = os.getenv(f"{name.upper()}_MODEL", provider["model"])

    config = {"model": model, "api_key": api_key}
    if provider["base_url"]:
        config["base_url"] = provider["base_url"]
        config["price"] = [0, 0]  # Evita el warning de costo desconocido
    return config


# Orden de proveedores a usar (el primero es el principal, los demás son respaldo)
order = [p.strip().lower() for p in os.getenv("PROVIDER", "groq").split(",")]

unknown = [p for p in order if p not in PROVIDERS]
if unknown:
    raise ValueError(f"Proveedor desconocido en PROVIDER: {unknown}. Opciones: {list(PROVIDERS)}")

config_list = [cfg for cfg in (build_config(p) for p in order) if cfg]
if not config_list:
    raise ValueError(f"No se encontró ninguna API key para: {order}. Revisa tu archivo .env")

print("🔌 Usando:", ", ".join(f"{c['model']}" for c in config_list))

llm_config = {"config_list": config_list}