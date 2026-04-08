from openai import OpenAI
import os
import time
from dotenv import load_dotenv

from env.environment import SmartHelmetEnv
from env.models import Action
from env.tasks import TASK_REGISTRY

# Load env variables
load_dotenv()

# Optional OpenAI client (not required)
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("API_BASE_URL")
    )


# 🔥 Decision Logic (your AI brain)
def choose_action(obs):

    # 🚨 Crash handling
    if getattr(obs, "impact_detected", False):
        if getattr(obs, "time_since_impact", 0) < 10:
            return Action.wait()

        if getattr(obs, "user_response", None) is False:
            return Action.trigger_emergency(
                reason="No response after crash"
            )

    # 📞 Incoming call while riding fast
    if getattr(obs, "incoming_call", False) and getattr(obs, "speed", 0) > 40:
        return Action.ignore(reason="Avoid distraction while riding")

    # 🎤 Voice assistant
    if getattr(obs, "voice_command", None):
        cmd = obs.voice_command.lower()

        if "music" in cmd:
            return Action.play_music()

        if "map" in cmd or "navigate" in cmd:
            return Action.open_maps(destination="nearest location")

        if "message" in cmd:
            return Action.send_message(
                content="I am currently riding, will reply later"
            )

    # 🚦 Smart alerts (NEW FEATURE)
    if getattr(obs, "obstacle_ahead", False):
        return Action.alert("Obstacle ahead, slow down")

    if getattr(obs, "traffic_signal", "") == "red":
        return Action.alert("Red signal ahead, please stop")

    # 😴 Default
    return Action.wait()


# 🔁 Run a single task
def run(task_name):
    print(f"\n[START]\ntask: {task_name}")

    env = SmartHelmetEnv()

    # ✅ CORRECT WAY
    obs = env.reset(task_name)

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


# 🚀 Main entry (runs all tasks)
if __name__ == "__main__":

    print("===== SMART HELMET AI STARTING =====")

    for task in TASK_REGISTRY:
        run(task)

    print("\n===== RUN COMPLETE =====")

    # 🔥 Keep container alive (IMPORTANT for HuggingFace)
    while True:
        time.sleep(60)