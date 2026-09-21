"""Repo-root paths. Override with LAYA_FILTER_ROOT if needed."""
import os

ROOT = os.environ.get(
    "LAYA_FILTER_ROOT",
    os.path.abspath(os.path.dirname(__file__)),
)
AGENT = os.path.join(ROOT, "agent")
DEPLOY = os.path.join(ROOT, "deploy")
DATA = os.path.join(AGENT, "data")
OUT = os.path.join(AGENT, "out")
QUIZ = os.path.join(AGENT, "quiz")
STATE = os.path.join(DEPLOY, "state")
MODELS = os.environ.get("LAYA_MODELS", os.path.join(ROOT, "models", "laya-large"))
