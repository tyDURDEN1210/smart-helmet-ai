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

        # 🔥 Simulated real-world inputs
        simulated_obs = {
            "speed": 70 if step % 5 == 0 else 30,
            "obstacle": True if step == 3 else False,
            "traffic_signal": "red" if step == 6 else "green",
            "incoming_call": True if step == 8 else False,
            "incoming_message": "Hey bro" if step == 10 else None,
            "idle": True if step == 15 else False
        }

        # Convert dict → object
        class Obj:
            def __init__(self, d):
                self.__dict__ = d

        obs = Obj(simulated_obs)

        action = choose_action(obs)
        print("action:", action.action_type)

        result = env.step(action)

        # ✅ Handle tuple returns properly
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

        # ✅ Safe reward extraction
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