from openai import OpenAI
import os
import time
from dotenv import load_dotenv

from env.environment import SmartHelmetEnv
from env.models import Action
from env.tasks import TASK_REGISTRY

load_dotenv()

client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("API_BASE_URL")
    )


def choose_action(obs):

    if getattr(obs, "impact_detected", False):
        if getattr(obs, "time_since_impact", 0) < 10:
            return Action(action_type="wait")

        if getattr(obs, "user_response", None) is False:
            return Action(
                action_type="trigger_emergency",
                reason="No response after crash"
            )

    if getattr(obs, "incoming_call", False) and getattr(obs, "speed", 0) > 40:
        return Action(
            action_type="ignore",
            reason="Avoid distraction"
        )

    if getattr(obs, "voice_command", None):
        cmd = obs.voice_command.lower()

        if "music" in cmd:
            return Action(action_type="play_music")

        if "map" in cmd or "navigate" in cmd:
            return Action(
                action_type="open_maps",
                destination="nearest location"
            )

        if "message" in cmd:
            return Action(
                action_type="send_message",
                content="I am riding, will reply later"
            )

    if getattr(obs, "obstacle_ahead", False):
        return Action(
            action_type="alert",
            message="Obstacle ahead, slow down"
        )

    if getattr(obs, "traffic_signal", "") == "red":
        return Action(
            action_type="alert",
            message="Red signal ahead, stop"
        )

    return Action(action_type="wait")


def run(task_name):
    print(f"\n[START]\ntask: {task_name}")

    env = SmartHelmetEnv()

    config = {
        "task": task_name,
        "speed": 0,
        "incoming_call": False,
        "impact_detected": False,
        "time_since_impact": 0,
        "user_response": None,
        "voice_command": None,
        "obstacle_ahead": False,
        "traffic_signal": "green"
    }

    obs = env.reset(config)

    done = False
    total_reward = 0

    while not done:
        action = choose_action(obs)

        obs, reward, done, info = env.step(action)

        print("[STEP]")
        print("action:", action.action_type)
        print("reward:", reward.value)

        # ✅ FIXED HERE
        total_reward += reward.value

    print("[END]")
    print("score:", round(total_reward, 4))


if __name__ == "__main__":
    print("===== SMART HELMET AI STARTING =====")

    for task in TASK_REGISTRY:
        run(task)

    print("\n===== RUN COMPLETE =====")

    while True:
        time.sleep(60)