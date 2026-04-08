from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from env.environment import SmartHelmetEnv

app = FastAPI()

env = SmartHelmetEnv()


# ✅ Action schema
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


# ✅ Reset endpoint (VERY IMPORTANT)
@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs}


# ✅ Step endpoint (VERY IMPORTANT)
@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)

    # Fix reward if needed
    if hasattr(reward, "value"):
        reward = reward.value

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }