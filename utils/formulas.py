from typing import Optional
from math import log10

def calculate_bmr(weight_kg: float, height_cm: float, age_years: int, sex: str, 
                  lean_body_mass_kg: Optional[float] = None) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using either Cunningham (if LBM is provided) 
    or Mifflin-St Jeor equation
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age_years: Age in years
        sex: 'M' for male or 'F' for female
        lean_body_mass_kg: Optional lean body mass in kilograms
        
    Returns:
        BMR value in calories per day
    """
    # Use Cunningham formula if lean body mass is provided
    if lean_body_mass_kg is not None:
        return 500 + (22 * lean_body_mass_kg)
    
    # Otherwise use Mifflin-St Jeor equation
    if sex.upper() == 'M':
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) + 5
    else:  # Female
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) - 161


def calculate_tdee(bmr: float, activity_multiplier: float) -> float:
    """
    Calculate Total Daily Energy Expenditure (TDEE) based on BMR and activity level
    
    Activity Multiplier Guidelines:
    - 1.2: Sedentary (little or no exercise)
    - 1.375: Lightly active (light exercise/sports 1-3 days/week)
    - 1.55: Moderately active (moderate exercise/sports 3-5 days/week)
    - 1.725: Very active (hard exercise/sports 6-7 days/week)
    - 1.9: Extremely active (very hard exercise & physical job or 2x training)
    
    Args:
        bmr: Basal Metabolic Rate in calories per day
        activity_multiplier: Activity level multiplier
        
    Returns:
        TDEE value in calories per day
    """
    return bmr * activity_multiplier


def estimate_one_rep_max(weight_kg: float, reps: int) -> float:
    """
    Estimate One Rep Max (1RM) using Epley formula
    
    Args:
        weight_kg: Weight lifted in kilograms
        reps: Number of repetitions performed
        
    Returns:
        Estimated 1RM in kilograms
    """
    if reps == 1:
        return weight_kg  # If it's already 1 rep, that's the 1RM
    
    # Epley formula
    return weight_kg * (1 + (reps / 30))


def calculate_body_fat_percentage(weight_kg: float, waist_cm: float, neck_cm: float, 
                                 height_cm: float, sex: str, hip_cm: Optional[float] = None) -> float:
    """
    Calculate body fat percentage using US Navy method
    
    Args:
        weight_kg: Weight in kilograms
        waist_cm: Waist circumference in centimeters
        neck_cm: Neck circumference in centimeters
        height_cm: Height in centimeters
        sex: 'M' for male, 'F' for female
        hip_cm: Hip circumference in centimeters (only needed for females)
        
    Returns:
        Body fat percentage (0-100)
    """
    if sex.upper() == 'M':
        # Men: Body Fat % = 495 / (1.0324 - 0.19077 * log10(waist - neck) + 0.15456 * log10(height)) - 450
        log10_term = (waist_cm - neck_cm) / height_cm
        body_fat = 86.010 * (log10(waist_cm - neck_cm)) - 70.041 * log10(height_cm) + 36.76
    else:  # Female
        if hip_cm is None:
            raise ValueError("Hip circumference is required for female body fat calculation")
        # Women: Body Fat % = 495 / (1.29579 - 0.35004 * log10(waist + hip - neck) + 0.22100 * log10(height)) - 450
        body_fat = 163.205 * log10(waist_cm + hip_cm - neck_cm) - 97.684 * log10(height_cm) - 104.912
    
    return max(0.0, min(body_fat, 100.0))  # Ensure result is within 0-100%