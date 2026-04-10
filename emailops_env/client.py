"""
EmailOps-Env: OpenEnv client for connecting to the EmailOps environment server.
"""

import json
import asyncio
from dataclasses import asdict
from typing import Optional

try:
    import websockets
except ImportError:
    websockets = None

try:
    import httpx
except ImportError:
    httpx = None

from emailops_env.models import EmailAction, EmailObservation, EmailState


class EmailOpsEnv:
    """
    Async client for the EmailOps-Env environment.
    Connects via WebSocket to an OpenEnv-compliant server.
    """

    def __init__(self, base_url: str = "http://localhost:7860"):
        self.base_url = base_url.rstrip("/")
        self.ws_url = self.base_url.replace("http://", "ws://").replace("https://", "wss://") + "/ws"
        self._ws = None
        self._session_id = None

    async def __aenter__(self):
        if websockets is None:
            raise ImportError("Install websockets: pip install websockets")
        self._ws = await websockets.connect(self.ws_url)
        return self

    async def __aexit__(self, *args):
        if self._ws:
            await self._ws.close()

    async def reset(self, email_id: str | None = None) -> EmailObservation:
        """Reset the environment and return the initial observation."""
        params = {}
        if email_id:
            params["email_id"] = email_id

        await self._ws.send(json.dumps({"method": "reset", "params": params}))
        response = json.loads(await self._ws.recv())

        if response.get("type") == "error":
            raise RuntimeError(response["message"])

        self._session_id = response.get("session_id")
        return EmailObservation(**response["observation"])

    async def step(self, action: EmailAction) -> dict:
        """Submit an action and return the step result."""
        await self._ws.send(json.dumps({
            "method": "step",
            "params": asdict(action),
        }))
        response = json.loads(await self._ws.recv())

        if response.get("type") == "error":
            raise RuntimeError(response["message"])

        return {
            "observation": EmailObservation(**response["observation"]),
            "reward": response["reward"],
            "done": response["done"],
            "info": response["info"],
        }

    async def state(self) -> EmailState | None:
        """Get the current environment state."""
        await self._ws.send(json.dumps({"method": "state"}))
        response = json.loads(await self._ws.recv())

        if response.get("type") == "error":
            raise RuntimeError(response["message"])

        state_data = response.get("state")
        if state_data is None:
            return None
        return EmailState(**state_data)

    def sync(self):
        """Return a synchronous wrapper around this client."""
        return SyncEmailOpsEnv(self)


class SyncEmailOpsEnv:
    """Synchronous wrapper around EmailOpsEnv."""

    def __init__(self, async_client: EmailOpsEnv):
        self._async = async_client
        self._loop = None

    def __enter__(self):
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self._async.__aenter__())
        return self

    def __exit__(self, *args):
        if self._loop:
            self._loop.run_until_complete(self._async.__aexit__(*args))
            self._loop.close()

    def reset(self, email_id: str | None = None) -> EmailObservation:
        return self._loop.run_until_complete(self._async.reset(email_id))

    def step(self, action: EmailAction) -> dict:
        return self._loop.run_until_complete(self._async.step(action))

    def state(self) -> EmailState | None:
        return self._loop.run_until_complete(self._async.state())


class EmailOpsHTTPClient:
    """
    Simple HTTP client for environments not using WebSocket.
    Uses httpx for HTTP requests.
    """

    def __init__(self, base_url: str = "http://localhost:7860"):
        if httpx is None:
            raise ImportError("Install httpx: pip install httpx")
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=60.0)
        self._session_id = None

    def reset(self, email_id: str | None = None) -> dict:
        payload = {}
        if email_id:
            payload["email_id"] = email_id
        resp = self._client.post(f"{self.base_url}/reset", json=payload)
        resp.raise_for_status()
        data = resp.json()
        self._session_id = data["session_id"]
        return data

    def step(self, action: dict) -> dict:
        if not self._session_id:
            raise RuntimeError("Call reset() first.")
        resp = self._client.post(f"{self.base_url}/step/{self._session_id}", json=action)
        resp.raise_for_status()
        return resp.json()

    def state(self) -> dict:
        if not self._session_id:
            raise RuntimeError("Call reset() first.")
        resp = self._client.get(f"{self.base_url}/state/{self._session_id}")
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self._client.close()
