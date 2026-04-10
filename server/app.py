# server/app.py
# A wrapper to satisfy the automated hackathon validation structure checker.
# It simply routes execution to our actual EmailOps-Env FastAPI application.

from emailops_env.server.app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
