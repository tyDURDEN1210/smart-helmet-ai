from openai import OpenAI
import os
import time
from dotenv import load_dotenv

from env.environment import SmartHelmetEnv
from env.models import Action
from env.tasks import TASK_REGISTRY

# Load environment variables
load_dotenv()

# Optional OpenAI client (not required)
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("API_BASE_URL")
    )


# 🧠 Decision logic
def choose_action(obs):

    # 🚨 Crash handling
    if getattr(obs, "impact_detected", False):
        if getattr(obs, "time_since_impact", 0) < 10:
            return Action.wait()

        if getattr(obs, "user_response", None) is False:
            return Action.trigger_emergency(
                reason="No response after crash"
            )

    # 📞 Incoming call safety
    if getattr(obs, "incoming_call", False) and getattr(obs, "speed", 0) > 40:
        return Action.ignore(reason="Avoid distraction while riding")

    # 🎤 Voice commands
    if getattr(obs, "voice_command", None):
        cmd = obs.voice_command.lower()

        if "music" in cmd:
            return Action.play_music()

        if "map" in cmd or "navigate" in cmd:
            return Action.open_maps(destination="nearest location")

        if "message" in cmd:
            return Action.send_message(
                content="I am riding, will reply later"
            )

    # 🚦 Smart alerts
    if getattr(obs, "obstacle_ahead", False):
        return Action.alert("Obstacle ahead, slow down")

    if getattr(obs, "traffic_signal", "") == "red":
        return Action.alert("Red signal ahead, please stop")

    # Default action
    return Action.wait()


# 🔁 Run simulation
def run(task_name):
    print(f"\n[START]\ntask: {task_name}")

    env = SmartHelmetEnv()

    # ✅ FULL SAFE CONFIG (prevents all crashes)
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

        result = env.step(action)
        obs = result.observation

        print("[STEP]")
        print("action:", action.action_type)
        print("reward:", result.reward.value)

        total_reward += result.reward.value
        done = result.done

    print("[END]")
    print("score:", round(total_reward, 4))


# 🚀 Main
if __name__ == "__main__":

    print("===== SMART HELMET AI STARTING =====")

    for task in TASK_REGISTRY:
        run(task)

    print("\n===== RUN COMPLETE =====")

    # 🔥 Keep container alive (IMPORTANT for Hugging Face)
    while True:
        time.sleep(60)