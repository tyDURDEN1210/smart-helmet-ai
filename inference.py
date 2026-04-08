from env.environment import SmartHelmetEnv
from env.models import Action


def choose_action(obs):
    """
    Decide what action to take based on observation
    """

    # 🛑 Obstacle detection
    if getattr(obs, "obstacle", False):
        return Action(
            action_type="alert",
            message="Obstacle ahead! Slow down immediately"
        )

    # 🚦 Traffic signal
    if getattr(obs, "traffic_signal", "") == "red":
        return Action(
            action_type="alert",
            message="Red light! Please stop"
        )

    # 🚀 Overspeed warning
    if getattr(obs, "speed", 0) > 60:
        return Action(
            action_type="alert",
            message="You are overspeeding! Slow down"
        )

    # 📩 Incoming message → auto reply
    if getattr(obs, "incoming_message", None):
        return Action(
            action_type="auto_reply",
            message="I'm riding right now, will reply later"
        )

    # 📞 Incoming call → reject
    if getattr(obs, "incoming_call", False):
        return Action(
            action_type="reject_call"
        )

    # 🎵 Play music if idle
    if getattr(obs, "idle", False):
        return Action(
            action_type="play_music"
        )

    # 🧠 Default smart behavior
    if getattr(obs, "speed", 0) > 0:
        return Action(
            action_type="alert",
            message="Stay focused and ride safe"
        )

    return Action(action_type="wait")


def run(task_name):
    print("===== SMART HELMET AI STARTING =====")

    env = SmartHelmetEnv()

    obs = env.reset()
    total_reward = 0

    for step in range(20):
        print(f"\n[STEP {step}]")

        action = choose_action(obs)

        print("action:", action.action_type)

        # 🔥 Step execution
        result = env.step(action)

        # ✅ FIX: unpack tuple properly
        if isinstance(result, tuple):
            if len(result) == 4:
                obs, reward, done, info = result
            elif len(result) == 3:
                obs, reward, done = result
                info = {}
            else:
                raise ValueError("Unexpected env.step() return format")
        else:
            raise ValueError("env.step() must return a tuple")

        # ✅ FIX: handle reward object safely
        try:
            reward_value = reward.value if hasattr(reward, "value") else float(reward)
        except:
            reward_value = 0

        print("reward:", reward_value)

        total_reward += reward_value

        if done:
            print("\n[END] Episode finished early")
            break

    print("\n===== RUN COMPLETE =====")
    print("Total reward:", total_reward)


if __name__ == "__main__":
    task = "task_voice_assistant"
    run(task)