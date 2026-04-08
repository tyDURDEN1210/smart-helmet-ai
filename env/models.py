from __future__ import annotations
from typing import Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class Observation(BaseModel):
    speed: int = Field(..., ge=0, le=300)
    is_moving: bool
    incoming_call: bool
    voice_command: Optional[str]

    incoming_message: Optional[str] = None
    caller_type: Optional[str] = None

    impact_detected: bool
    impact_confidence: float = Field(..., ge=0.0, le=1.0)
    false_impact: bool = False

    time_since_impact: int = Field(..., ge=0)
    user_response: Optional[bool]

    hazard_type: Optional[str] = None
    hazard_distance: Optional[int] = None

    location: str
    current_task: str
    step_count: int = Field(..., ge=0)

    class Config:
        extra = "forbid"


ActionType = Literal[
    "handle_call",
    "open_maps",
    "play_music",
    "ignore",
    "trigger_emergency",
    "wait",
    "send_message",
    "decline_call",
    "alert_rider",
]


class Action(BaseModel):
    action_type: ActionType
    parameters: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "forbid"


class RewardSignal(BaseModel):
    value: float
    reason: str
    safety_violation: bool = False
    components: Dict[str, float] = Field(default_factory=dict)

    class Config:
        extra = "forbid"