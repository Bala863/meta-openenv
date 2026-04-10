"""
EmailOps-Env: FastAPI server exposing the environment via HTTP/WebSocket endpoints.
Implements the OpenEnv server contract.
"""

import json
import uuid
import asyncio
from dataclasses import asdict
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from emailops_env.models import EmailAction, EmailObservation, EmailState
from emailops_env.server.email_environment import EmailEnvironment


# ── Pydantic models for HTTP endpoints ───────────────────────────────────────

class ResetRequest(BaseModel):
    email_id: Optional[str] = None


class ActionRequest(BaseModel):
    intent: str = ""
    order_id: str = ""
    customer_name: str = ""
    issue_description: str = ""
    product_name: str = ""
    requested_resolution: str = ""
    urgency_level: str = ""
    email_address: str = ""
    response_text: str = ""


class StepResult(BaseModel):
    observation: dict
    reward: float
    done: bool
    info: dict


# ── Session management ───────────────────────────────────────────────────────

_sessions: dict[str, EmailEnvironment] = {}


def _get_or_create_session(session_id: str | None = None) -> tuple[str, EmailEnvironment]:
    if session_id and session_id in _sessions:
        return session_id, _sessions[session_id]
    new_id = str(uuid.uuid4())[:12]
    env = EmailEnvironment()
    _sessions[new_id] = env
    return new_id, env


# ── FastAPI Application ──────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    print("🚀 EmailOps-Env server starting...")
    yield
    print("🛑 EmailOps-Env server shutting down...")
    _sessions.clear()


app = FastAPI(
    title="EmailOps-Env",
    description="OpenEnv-compliant email operations environment for AI agent evaluation",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ─────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": "EmailOps-Env",
        "version": "1.0.0",
        "active_sessions": len(_sessions),
    }


@app.get("/")
async def root():
    return {
        "message": "📧 Welcome to EmailOps-Env (OpenEnv)",
        "status": "running",
        "endpoints": {
            "health": "GET /health",
            "emails": "GET /emails",
            "reset": "POST /reset",
            "step": "POST /step/{session_id}",
            "state": "GET /state/{session_id}",
            "websocket": "WS /ws"
        },
        "docs": "GET /docs"
    }

# ── HTTP Endpoints ───────────────────────────────────────────────────────────

@app.post("/reset")
async def reset(request: ResetRequest = ResetRequest()):
    session_id, env = _get_or_create_session()
    obs = env.reset(email_id=request.email_id)
    return {
        "session_id": session_id,
        "observation": asdict(obs),
    }


@app.post("/step/{session_id}")
async def step(session_id: str, action: ActionRequest):
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found. Call /reset first.")

    env = _sessions[session_id]
    email_action = EmailAction(
        intent=action.intent,
        order_id=action.order_id,
        customer_name=action.customer_name,
        issue_description=action.issue_description,
        product_name=action.product_name,
        requested_resolution=action.requested_resolution,
        urgency_level=action.urgency_level,
        email_address=action.email_address,
        response_text=action.response_text,
    )

    result = env.step(email_action)
    return {
        "observation": asdict(result["observation"]),
        "reward": result["reward"],
        "done": result["done"],
        "info": result["info"],
    }


@app.get("/state/{session_id}")
async def get_state(session_id: str):
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    env = _sessions[session_id]
    state = env.state()
    if state is None:
        return {"state": None}
    return {"state": asdict(state)}


@app.get("/emails")
async def list_emails():
    """List available email IDs for targeted evaluation."""
    from emailops_env.server.email_data import get_all_email_ids
    return {"email_ids": get_all_email_ids(), "count": len(get_all_email_ids())}


# ── WebSocket Endpoint (OpenEnv standard) ────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    session_id = None
    env = None

    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            method = msg.get("method", "")

            if method == "reset":
                session_id, env = _get_or_create_session(session_id)
                email_id = msg.get("params", {}).get("email_id")
                obs = env.reset(email_id=email_id)
                await ws.send_json({
                    "type": "reset_result",
                    "session_id": session_id,
                    "observation": asdict(obs),
                })

            elif method == "step":
                if env is None:
                    await ws.send_json({"type": "error", "message": "Call reset first."})
                    continue

                params = msg.get("params", {})
                action = EmailAction(
                    intent=params.get("intent", ""),
                    order_id=params.get("order_id", ""),
                    customer_name=params.get("customer_name", ""),
                    issue_description=params.get("issue_description", ""),
                    product_name=params.get("product_name", ""),
                    requested_resolution=params.get("requested_resolution", ""),
                    urgency_level=params.get("urgency_level", ""),
                    email_address=params.get("email_address", ""),
                    response_text=params.get("response_text", ""),
                )

                result = env.step(action)
                await ws.send_json({
                    "type": "step_result",
                    "observation": asdict(result["observation"]),
                    "reward": result["reward"],
                    "done": result["done"],
                    "info": result["info"],
                })

            elif method == "state":
                if env is None:
                    await ws.send_json({"type": "state_result", "state": None})
                    continue

                state = env.state()
                await ws.send_json({
                    "type": "state_result",
                    "state": asdict(state) if state else None,
                })

            else:
                await ws.send_json({
                    "type": "error",
                    "message": f"Unknown method: {method}. Use 'reset', 'step', or 'state'.",
                })

    except WebSocketDisconnect:
        if session_id and session_id in _sessions:
            del _sessions[session_id]
    except Exception as e:
        await ws.send_json({"type": "error", "message": str(e)})


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
