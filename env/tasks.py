class BaseTask:
    name = "base"

    def config(self):
        return {}

    def grade(self, env):
        return 0.0


class TaskVoiceAssistant(BaseTask):
    name = "task_voice_assistant"

    def config(self):
        return {
            "speed": 0,
            "is_moving": False,
            "voice_command": "play music",
            "incoming_call": False,
            "current_task": self.name,
        }

    def grade(self, env):
        return 1.0 if env._history[0]["action"]["action_type"] == "play_music" else 0.0


class TaskContextAware(BaseTask):
    name = "task_context_aware"

    def config(self):
        return {
            "speed": 80,
            "is_moving": True,
            "incoming_call": True,
            "voice_command": "play music",
            "current_task": self.name,
        }

    def grade(self, env):
        return 1.0 if env._history[0]["action"]["action_type"] == "wait" else 0.0


class TaskCrashEmergency(BaseTask):
    name = "task_crash_emergency"

    def config(self):
        return {
            "impact_detected": True,
            "false_impact": False,
            "time_since_impact": 0,
            "user_response": None,
            "current_task": self.name,
        }

    def grade(self, env):
        for step in env._history:
            if step["action"]["action_type"] == "trigger_emergency":
                return 1.0
        return 0.0


class TaskMessaging(BaseTask):
    name = "task_messaging"

    def config(self):
        return {
            "speed": 50,
            "is_moving": True,
            "incoming_message": "Where are you?",
            "current_task": self.name,
        }

    def grade(self, env):
        action = env._history[0]["action"]
        if action["action_type"] != "send_message":
            return 0.0
        msg = action["parameters"].get("message", "").lower()
        return 1.0 if "driving" in msg else 0.5


class TaskSpamCall(BaseTask):
    name = "task_spam_call"

    def config(self):
        return {
            "incoming_call": True,
            "caller_type": "spam",
            "is_moving": True,
            "speed": 60,
            "current_task": self.name,
        }

    def grade(self, env):
        return 1.0 if env._history[0]["action"]["action_type"] == "decline_call" else 0.0


class TaskHazardAlert(BaseTask):
    name = "task_hazard_alert"

    def config(self):
        return {
            "speed": 70,
            "is_moving": True,
            "hazard_type": "obstacle",
            "hazard_distance": 30,
            "current_task": self.name,
        }

    def grade(self, env):
        action = env._history[0]["action"]
        if action["action_type"] != "alert_rider":
            return 0.0
        msg = action["parameters"].get("message", "").lower()
        return 1.0 if "slow" in msg or "obstacle" in msg else 0.5


TASK_REGISTRY = {
    t.name: t()
    for t in [
        TaskVoiceAssistant,
        TaskContextAware,
        TaskCrashEmergency,
        TaskMessaging,
        TaskSpamCall,
        TaskHazardAlert,
    ]
}