"""Adaptive signal controller for a multi-arm junction.
Decides which phase gets green next and for how long, from vehicle counts per arm."""

from dataclasses import dataclass, field


@dataclass
class JunctionConfig:
    arms: list = field(default_factory=lambda: ["Arm A (N)", "Arm B (E)", "Arm C (S)", "Arm D (W)"])
    phases: list = field(default_factory=lambda: [[0, 2], [1, 3]])   # arm indices per phase
    discharge_per_sec: float = 0.4     # vehicles leaving an arm per second on green (assumed)
    min_green: int = 10
    max_green: int = 60
    yellow: int = 3
    fixed_green: int = 25


class JunctionController:
    def __init__(self, config=None):
        self.cfg = config or JunctionConfig()
        self.current = -1              # index of the phase that last had green

    def next_phase(self, counts):
        """counts: vehicles waiting per arm, e.g. [12, 3, 9, 1].
        Returns (phase_index, green_seconds). Phases are served in order,
        so no arm is ever skipped."""
        c = self.cfg
        self.current = (self.current + 1) % len(c.phases)
        longest = max(counts[a] for a in c.phases[self.current])
        green = round(longest / c.discharge_per_sec)
        return self.current, max(c.min_green, min(c.max_green, green))

    def fixed_phase(self):
        """Fallback: fixed-time plan, ignores counts."""
        c = self.cfg
        self.current = (self.current + 1) % len(c.phases)
        return self.current, c.fixed_green
