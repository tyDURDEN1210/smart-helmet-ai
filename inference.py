from env.environment import SmartHelmetEnv
from env.models import Action
from env.tasks import TASK_REGISTRY


def choose_action(obs):

    # 🚧 Hazard alerts
    if obs.hazard_type and obs.hazard_distance and obs.hazard_distance < 50:
        if obs.hazard_type == "obstacle":
            return Action("alert_rider", {"message": "Slow down, obstacle ahead"})
        if obs.hazard_type == "red_signal":
            return Action("alert_rider", {"message": "Red signal ahead, slow down"})

    # 🚨 Crash logic
    if obs.impact_detected:
        if obs.false_impact:
            return Action("wait", {})
        if obs.time_since_impact >= 10 or obs.user_response is False:
            return Action("trigger_emergency", {})
        return Action("wait", {})

    # 📩 Messaging
    if obs.incoming_message:
        if obs.is_moving:
            return Action("send_message", {"message": "I'm driving, will reply later."})
        return Action("send_message", {"message": "Okay, I’ll respond shortly."})

    # 📞 Spam call
    if obs.incoming_call and obs.caller_type == "spam":
        return Action("decline_call", {})

    # ⚡ Speed safety
    if obs.is_moving and obs.speed > 40:
        return Action("wait", {})

    # 🎵 Voice commands
    if obs.voice_command == "play music":
        return Action("play_music", {})
    if obs.voice_command == "open maps":
        return Action("open_maps", {})

    if obs.incoming_call:
        return Action("handle_call", {"accept": False})

    return Action("wait", {})


def run(task):
    env = SmartHelmetEnv()
    obs = env.reset(task.config())

    print("[START]")
    print(f"task: {task.name}")

    done = False

    while not done:
        action = choose_action(obs)
        obs, reward, done, _ = env.step(action)

        print("[STEP]")
        print(f"action: {action.action_type}")
        print(f"reward: {reward.value:.2f}")

    score = env.grade()

    print("[END]")
    print(f"score: {score:.4f}")


if __name__ == "__main__":
    for task in TASK_REGISTRY.values():
        run(task)