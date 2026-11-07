import os
import httpx


class JaxoClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("MODEL", "openai/gpt-4o-mini")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is missing. Copy .env.example to .env and add your key.")
        self.http = httpx.Client(timeout=90.0)

    def chat(self, messages, tools=None):
        payload = {"model": self.model, "messages": messages, "temperature": 0.4}
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        response = self.http.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]

    def close(self):
        self.http.close()
