from pydantic import BaseModel
from typing import Literal
from env.environment import SmartHelmetEnv


# ✅ Allowed actions (VERY IMPORTANT)
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


# ✅ Decision logic
def choose_action(obs):

    if obs.get("call"):
        return Action(action="handle_call")

    if obs.get("traffic") == "high":
        return Action(action="alert_rider")

    if obs.get("speed", 0) > 60:
        return Action(action="alert_rider")

    return Action(action="wait")


# ✅ Main runner
def run(task_name="task_voice_assistant"):

    print("===== SMART HELMET AI STARTING =====")

    env = SmartHelmetEnv()

    obs = env.reset()
    total_reward = 0

    for step in range(20):

        print(f"\n[STEP {step}]")

        action = choose_action(obs)
        print("action:", action.action)

        result = env.step(action)

        # ✅ FIX tuple unpacking
        obs, reward, done, info = result

        print("reward:", reward)

        # ✅ FIX reward type
        if hasattr(reward, "value"):
            reward = reward.value

        total_reward += reward

        if done:
            print("\n[END] Episode finished early")
            break

    print("\n===== RUN COMPLETE =====")
    print("Total reward:", total_reward)


# ✅ Entry point (IMPORTANT for HuggingFace)
if __name__ == "__main__":
    run()