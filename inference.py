from openai import OpenAI
import os
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

    if obs.impact_detected:
        if obs.time_since_impact < 10:
            return Action.wait()
        if obs.user_response is False:
            return Action.trigger_emergency("No response after crash")

    if obs.incoming_call and obs.speed > 40:
        return Action.ignore("Avoid distraction")

    if obs.voice_command:
        cmd = obs.voice_command.lower()

        if "music" in cmd:
            return Action.play_music()

        if "map" in cmd:
            return Action.open_maps("nearest destination")

    return Action.wait()


def run(task_name):
    print(f"[START]\ntask: {task_name}")

    # 🔥 FIXED HERE
    env = SmartHelmetEnv()
    env.set_task(task_name)

    obs = env.reset()

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


if __name__ == "__main__":
    for task in TASK_REGISTRY:
        run(task)


# keep container alive
import time
while True:
    time.sleep(60)