from typing import List, Dict, Any, Optional, Tuple
from datetime import date, timedelta
import pandas as pd

from data_models.workout_models import WorkoutData
from data_models.nutrition_models import DailyNutritionData, WeightData
from analysis.workout_analysis import WorkoutAnalyzer
from analysis.nutrition_analysis import NutritionAnalyzer
from utils.formulas import calculate_bmr, calculate_tdee

class InsightGenerator:
    """
    Combines workout and nutrition analyses to generate actionable insights
    """
    
    def __init__(self, workout_data: List[WorkoutData], 
                 nutrition_data: List[DailyNutritionData], 
                 weight_data: List[WeightData]):
        """
        Initialize with all fitness data
        
        Args:
            workout_data: List of WorkoutData objects
            nutrition_data: List of DailyNutritionData objects
            weight_data: List of WeightData objects
        """
        self.workout_analyzer = WorkoutAnalyzer(workout_data)
        self.nutrition_analyzer = NutritionAnalyzer(nutrition_data, weight_data)
    
    def get_training_recommendations(self) -> List[Dict[str, Any]]:
        """
        Generate training recommendations based on workout analysis
        
        Returns:
            List of recommendation dictionaries with 'type', 'message', and 'priority'
        """
        recommendations = []
        
        # Check for stalled exercises
        stalled_exercises = self.workout_analyzer.identify_stalled_exercises(weeks=8)
        if stalled_exercises:
            for exercise in stalled_exercises:
                recommendations.append({
                    'type': 'training',
                    'message': f"Progress for {exercise} has stalled. Consider varying rep ranges, adding volume, or applying progressive overload techniques.",
                    'priority': 'high'
                })
        
        # Check workout frequency
        workout_frequency = self.workout_analyzer.get_workout_frequency(weeks=4)
        total_workouts = sum(workout_frequency.values())
        if total_workouts < 8:  # Less than 2 workouts per week
            recommendations.append({
                'type': 'training',
                'message': f"Your workout frequency is below optimal levels ({total_workouts} workouts in the last 4 weeks). Aim for at least 3-4 workouts per week for better results.",
                'priority': 'medium'
            })
        
        return recommendations
    
    def get_nutrition_recommendations(self, height_cm: float, age_years: int, sex: str) -> List[Dict[str, Any]]:
        """
        Generate nutrition recommendations based on nutrition and weight analysis
        
        Args:
            height_cm: Height in centimeters
            age_years: Age in years
            sex: 'M' for male, 'F' for female
            
        Returns:
            List of recommendation dictionaries with 'type', 'message', and 'priority'
        """
        recommendations = []
        
        # Get weight trend
        weight_change, is_losing = self.nutrition_analyzer.get_weight_trend(weeks=4)
        
        # Get macronutrient ratios
        macro_ratios = self.nutrition_analyzer.get_macronutrient_ratios(days=14)
        
        # Check protein intake
        if macro_ratios['protein_pct'] < 25:
            recommendations.append({
                'type': 'nutrition',
                'message': f"Your protein intake is low at {macro_ratios['protein_pct']}% of calories. For optimal muscle growth and recovery, aim for 30-35% of calories from protein.",
                'priority': 'high'
            })
        
        # Get latest weight
        latest_weight = None
        if self.nutrition_analyzer.weight_df is not None and not self.nutrition_analyzer.weight_df.empty:
            latest_weight = self.nutrition_analyzer.weight_df.iloc[-1]['weight']
        
        # Estimate TDEE if we have enough data
        if latest_weight:
            estimated_tdee = self.nutrition_analyzer.estimate_tdee(
                height_cm=height_cm,
                age_years=age_years,
                sex=sex
            )
            
            if estimated_tdee:
                # Calculate theoretical TDEE based on formulas
                theoretical_bmr = calculate_bmr(latest_weight, height_cm, age_years, sex)
                theoretical_tdee = calculate_tdee(theoretical_bmr, 1.55)  # Moderate activity level
                
                # Compare estimated vs theoretical
                difference = abs(estimated_tdee - theoretical_tdee)
                if difference > (theoretical_tdee * 0.15):  # More than 15% difference
                    recommendations.append({
                        'type': 'nutrition',
                        'message': f"Your estimated energy expenditure ({int(estimated_tdee)} kcal) differs significantly from theoretical calculations ({int(theoretical_tdee)} kcal). This could indicate inaccurate calorie tracking or an unusually high/low activity level.",
                        'priority': 'medium'
                    })
        
        return recommendations
    
    def get_combined_insights(self, height_cm: float, age_years: int, sex: str, 
                             goal: str = 'muscle_gain') -> Dict[str, Any]:
        """
        Generate combined insights and recommendations
        
        Args:
            height_cm: Height in centimeters
            age_years: Age in years
            sex: 'M' for male, 'F' for female
            goal: Fitness goal - 'muscle_gain', 'fat_loss', or 'maintenance'
            
        Returns:
            Dictionary with insights and recommendations
        """
        # Get all recommendations
        training_recommendations = self.get_training_recommendations()
        nutrition_recommendations = self.get_nutrition_recommendations(height_cm, age_years, sex)
        
        # Get weight trend
        weight_change, is_losing = self.nutrition_analyzer.get_weight_trend(weeks=4)
        
        # Get macronutrient ratios
        macro_ratios = self.nutrition_analyzer.get_macronutrient_ratios(days=14)
        
        # Get calorie target based on goal and current TDEE estimate
        latest_weight = None
        estimated_tdee = None
        
        if self.nutrition_analyzer.weight_df is not None and not self.nutrition_analyzer.weight_df.empty:
            latest_weight = self.nutrition_analyzer.weight_df.iloc[-1]['weight']
            
            if latest_weight:
                estimated_tdee = self.nutrition_analyzer.estimate_tdee(
                    height_cm=height_cm,
                    age_years=age_years,
                    sex=sex
                )
        
        if not estimated_tdee and latest_weight:
            # Use theoretical calculation if estimation fails
            bmr = calculate_bmr(latest_weight, height_cm, age_years, sex)
            estimated_tdee = calculate_tdee(bmr, 1.55)  # Moderate activity level
        
        calorie_target = None
        if estimated_tdee:
            if goal == 'muscle_gain':
                calorie_target = estimated_tdee + 300  # Slight surplus
            elif goal == 'fat_loss':
                calorie_target = estimated_tdee - 500  # Moderate deficit
            else:  # maintenance
                calorie_target = estimated_tdee
        
        # Build the insights object
        insights = {
            'recommendations': {
                'training': training_recommendations,
                'nutrition': nutrition_recommendations
            },
            'stats': {
                'weight_change_kg': round(weight_change, 1) if weight_change is not None else None,
                'macro_ratios': macro_ratios,
                'estimated_tdee': int(estimated_tdee) if estimated_tdee else None,
                'suggested_calorie_target': int(calorie_target) if calorie_target else None
            },
            'goal_alignment': {}
        }
        
        # Check goal alignment
        if goal == 'muscle_gain':
            if weight_change is not None:
                if weight_change > 0 and weight_change < 1:
                    insights['goal_alignment']['weight'] = 'good'  # Gaining, but not too fast
                elif weight_change >= 1:
                    insights['goal_alignment']['weight'] = 'too_fast'  # Gaining too fast (likely adding fat)
                else:
                    insights['goal_alignment']['weight'] = 'insufficient'  # Not gaining
            
            if macro_ratios['protein_pct'] >= 25:
                insights['goal_alignment']['protein'] = 'good'
            else:
                insights['goal_alignment']['protein'] = 'low'
        
        elif goal == 'fat_loss':
            if weight_change is not None:
                if weight_change < 0 and weight_change > -1:
                    insights['goal_alignment']['weight'] = 'good'  # Losing, but not too fast
                elif weight_change <= -1:
                    insights['goal_alignment']['weight'] = 'too_fast'  # Losing too fast (likely losing muscle)
                else:
                    insights['goal_alignment']['weight'] = 'insufficient'  # Not losing
            
            if macro_ratios['protein_pct'] >= 30:
                insights['goal_alignment']['protein'] = 'good'  # Higher protein for fat loss
            else:
                insights['goal_alignment']['protein'] = 'low'
        
        return insights