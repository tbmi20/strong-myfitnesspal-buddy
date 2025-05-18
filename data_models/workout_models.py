from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional, Dict, Any

@dataclass
class ExerciseData:
    name: str
    category: Optional[str] = None

@dataclass
class SetData:
    exercise_name: str
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_km: Optional[float] = None
    duration_seconds: Optional[int] = None
    is_completed: bool = True

@dataclass
class WorkoutData:
    date: date
    routine_name: Optional[str] = None
    exercises: List[ExerciseData] = field(default_factory=list)
    sets: List[SetData] = field(default_factory=list)