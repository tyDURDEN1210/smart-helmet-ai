from env.environment import SmartHelmetEnv
from env.models import Action


def choose_action(obs):

    # 🛑 Obstacle
    if getattr(obs, "obstacle", False):
        return Action(
            action_type="alert_rider",
            message="Obstacle ahead! Slow down immediately"
        )

    # 🚦 Traffic signal
    if getattr(obs, "traffic_signal", "") == "red":
        return Action(
            action_type="alert_rider",
            message="Red light! Stop the vehicle"
        )

    # 🚀 Overspeed
    if getattr(obs, "speed", 0) > 60:
        return Action(
            action_type="alert_rider",
            message="You are overspeeding! Slow down"
        )

    # 📩 Message
    if getattr(obs, "incoming_message", None):
        return Action(
            action_type="send_message",
            message="I'm riding right now, will reply later"
        )

    # 📞 Call
    if getattr(obs, "incoming_call", False):
        return Action(
            action_type="decline_call"
        )

    # 🎵 Idle
    if getattr(obs, "idle", False):
        return Action(
            action_type="play_music"
        )

    # Default
    return Action(action_type="wait")


def run(task_name):
    print("===== SMART HELMET AI STARTING =====")

    env = SmartHelmetEnv()
    total_reward = 0

    for step in range(20):
        print(f"\n[STEP {step}]")

        # 🔥 Simulated inputs
        simulated_obs = {
            "speed": 70 if step % 5 == 0 else 30,
            "obstacle": True if step == 3 else False,
            "traffic_signal": "red" if step == 6 else "green",
            "incoming_call": True if step == 8 else False,
            "incoming_message": "Hey bro" if step == 10 else None,
            "idle": True if step == 15 else False
        }

        class Obj:
            def __init__(self, d):
                self.__dict__ = d

        obs = Obj(simulated_obs)

        action = choose_action(obs)
        print("action:", action.action_type)

        result = env.step(action)

        if isinstance(result, tuple):
            obs, reward, done, info = result
        else:
            raise ValueError("env.step() must return tuple")

        reward_value = getattr(reward, "value", reward)
        print("reward:", reward_value)

        total_reward += reward_value

        if done:
            print("\n[END] Episode finished early")
            break

    print("\n===== RUN COMPLETE =====")
    print("Total reward:", total_reward)


if __name__ == "__main__":
    run("task_voice_assistant")