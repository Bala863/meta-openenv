"""
EmailOps-Env: An OpenEnv-compliant email operations environment for AI agent evaluation.
"""

from emailops_env.models import EmailAction, EmailObservation, EmailState
from emailops_env.client import EmailOpsEnv, SyncEmailOpsEnv, EmailOpsHTTPClient

__all__ = [
    "EmailAction",
    "EmailObservation",
    "EmailState",
    "EmailOpsEnv",
    "SyncEmailOpsEnv",
    "EmailOpsHTTPClient",
]

__version__ = "1.0.0"
