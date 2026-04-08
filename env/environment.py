from __future__ import annotations
import copy, random
from typing import Any, Dict, Optional, Tuple
from env.models import Action, Observation, RewardSignal

HIGH_SPEED_THRESHOLD = 40
EMERGENCY_COUNTDOWN_LIMIT = 10
USELESS_ACTION_PENALTY = -0.1
TIME_PENALTY = -0.05

class SmartHelmetEnv:
    def reset(self, task_config: Optional[Dict[str, Any]] = None) -> Observation:
        cfg = task_config or {}

        self._speed = cfg.get("speed", 0)
        self._is_moving = cfg.get("is_moving", False)
        self._incoming_call = cfg.get("incoming_call", False)
        self._voice_command = cfg.get("voice_command", None)
        self._impact_detected = cfg.get("impact_detected", False)
        self._time_since_impact = cfg.get("time_since_impact", 0)
        self._user_response = cfg.get("user_response", None)
        self._location = cfg.get("location", "Unknown")
        self._current_task = cfg.get("current_task", "default")

        self._impact_confidence = cfg.get("impact_confidence", random.uniform(0.6, 0.95))
        self._is_false_impact = cfg.get("false_impact", False)

        self._step_count = 0
        self._max_steps = cfg.get("max_steps", 20)
        self._done = False
        self._episode_reward = 0.0
        self._history = []
        self._emergency_triggered = False
        self._scenario_flags = cfg.get("scenario_flags", {})

        return self._build_observation()

    def step(self, action: Action):
        if self._done:
            raise RuntimeError("Episode finished")

        self._step_count += 1

        if self._impact_detected and self._user_response is None:
            if random.random() < 0.2:
                self._user_response = True

        reward = self._compute_reward(action)
        reward.value += TIME_PENALTY

        self._apply_action(action)

        if (
            self._impact_detected
            and self._time_since_impact >= EMERGENCY_COUNTDOWN_LIMIT
            and not self._emergency_triggered
            and self._user_response is not True
        ):
            reward.value -= 5.0
            self._trigger_emergency(True)

        if self._impact_detected and not self._emergency_triggered:
            self._time_since_impact += 1

        self._episode_reward += reward.value
        obs = self._build_observation()

        if self._step_count >= self._max_steps or self._emergency_triggered:
            self._done = True

        self._history.append({
            "step": self._step_count,
            "action": action.model_dump(),
            "reward": reward.model_dump()
        })

        return obs, reward, self._done, {}

    def _compute_reward(self, action: Action) -> RewardSignal:
        atype = action.action_type

        if self._impact_detected:
            if atype == "trigger_emergency":
                if self._is_false_impact:
                    return RewardSignal(value=-3.0, reason="false crash")
                if self._time_since_impact >= EMERGENCY_COUNTDOWN_LIMIT or self._user_response is False:
                    return RewardSignal(value=3.0, reason="correct emergency")
                return RewardSignal(value=-1.0, reason="too early")

            if atype == "wait":
                return RewardSignal(value=1.0 if self._time_since_impact < 10 else -3.0, reason="wait logic")

            if atype == "ignore":
                return RewardSignal(value=-5.0, reason="ignored crash")

            return RewardSignal(value=-2.0, reason="irrelevant action")

        if atype == "trigger_emergency":
            return RewardSignal(value=-2.0, reason="false emergency")

        if self._speed > HIGH_SPEED_THRESHOLD and self._is_moving:
            if atype == "handle_call":
                return RewardSignal(value=-2.0, reason="call at speed")
            if atype == "play_music":
                return RewardSignal(value=-1.0, reason="music distraction")
            if atype == "open_maps":
                return RewardSignal(value=0.5, reason="maps ok")
            if atype in ("wait", "ignore"):
                return RewardSignal(value=1.0, reason="safe")

        if atype == "play_music" and self._voice_command == "play music":
            return RewardSignal(value=1.0, reason="correct")
        if atype == "open_maps" and self._voice_command == "open maps":
            return RewardSignal(value=1.0, reason="correct")

        return RewardSignal(value=USELESS_ACTION_PENALTY, reason="useless")

    def _apply_action(self, action: Action):
        if action.action_type == "trigger_emergency":
            self._trigger_emergency(False)

    def _trigger_emergency(self, auto=False):
        self._emergency_triggered = True

    def _build_observation(self):
        return Observation(
            speed=self._speed,
            is_moving=self._is_moving,
            incoming_call=self._incoming_call,
            voice_command=self._voice_command,
            impact_detected=self._impact_detected,
            impact_confidence=self._impact_confidence,
            false_impact=self._is_false_impact,
            time_since_impact=self._time_since_impact,
            user_response=self._user_response,
            location=self._location,
            current_task=self._current_task,
            step_count=self._step_count,
        )

    def grade(self):
        from env.tasks import TASK_REGISTRY
        return TASK_REGISTRY[self._current_task].grade(self)