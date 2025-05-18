from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class DailyNutritionData:
    date: date
    calories_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float
    # Optional additional nutrients
    fiber_g: Optional[float] = None
    sugar_g: Optional[float] = None
    sodium_mg: Optional[float] = None
    cholesterol_mg: Optional[float] = None

@dataclass
class WeightData:
    date: date
    weight_kg: float
    body_fat_percentage: Optional[float] = None