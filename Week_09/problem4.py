from dataclasses import dataclass, field

@dataclass
class TrainingSession:
    trainee: str
    descipline: str
    scores: list[int] = field(default_factory=list)
    