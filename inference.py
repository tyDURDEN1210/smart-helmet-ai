from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from env.environment import SmartHelmetEnv

app = FastAPI()

env = SmartHelmetEnv()


# ✅ Allowed actions
class Action(BaseModel):
    action: Literal[
        "handle_call",
        "open_maps",
        "play_music",
        "ignore",
        "trigger_emergency",
        "wait",
        "send_message",
        "decline_call",
        "alert_rider"
    ]


# ✅ RESET (must return ONLY observation)
@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs
    }


# ✅ STEP (STRICT FORMAT)
@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)

    # Convert reward if needed
    if hasattr(reward, "value"):
        reward = reward.value

    return {
        "observation": obs,   # MUST be dict
        "reward": float(reward),  # MUST be float
        "done": bool(done),   # MUST be bool
        "info": info if isinstance(info, dict) else {}
    }