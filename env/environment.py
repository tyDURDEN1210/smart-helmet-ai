class SmartHelmetEnv:

    def __init__(self):
        self._done = False
        self.step_count = 0

    def reset(self, config=None):
        self._done = False
        self.step_count = 0

        # Observation = environment state
        obs = {
            "speed": 0,
            "traffic": "low",
            "call": False
        }

        return obs

    def step(self, action):
        if self._done:
            return self.reset(), 0, True, {}

        self.step_count += 1

        # Dummy logic for demo
        reward = 0

        if action.action == "wait":
            reward = -0.15
        elif action.action == "alert_rider":
            reward = 1
        elif action.action == "play_music":
            reward = 0.2
        else:
            reward = -0.5

        # End episode after 20 steps
        if self.step_count >= 20:
            self._done = True

        obs = {
            "speed": 20,
            "traffic": "medium",
            "call": False
        }

        return obs, float(reward), bool(self._done), {}