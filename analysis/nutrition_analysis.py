import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import date, timedelta
from collections import defaultdict

from data_models.nutrition_models import DailyNutritionData, WeightData
from utils.formulas import calculate_bmr, calculate_tdee

class NutritionAnalyzer:
    """
    Analyzes nutrition and weight data to track progress and generate insights
    """
    
    def __init__(self, nutrition_data: List[DailyNutritionData], weight_data: List[WeightData]):
        """
        Initialize with lists of nutrition and weight data
        
        Args:
            nutrition_data: List of DailyNutritionData objects
            weight_data: List of WeightData objects
        """
        self.nutrition_data = sorted(nutrition_data, key=lambda x: x.date)
        self.weight_data = sorted(weight_data, key=lambda x: x.date)
        self._process_data()
    
    def _process_data(self):
        """Process the data for analysis"""
        # Create DataFrames for easier analysis
        nutrition_records = [
            {
                'date': data.date,
                'calories': data.calories_kcal,
                'protein': data.protein_g,
                'carbs': data.carbs_g,
                'fat': data.fat_g,
                'fiber': data.fiber_g,
                'sugar': data.sugar_g
            }
            for data in self.nutrition_data
        ]
        self.nutrition_df = pd.DataFrame(nutrition_records)
        
        weight_records = [
            {
                'date': data.date,
                'weight': data.weight_kg,
                'body_fat': data.body_fat_percentage
            }
            for data in self.weight_data
        ]
        self.weight_df = pd.DataFrame(weight_records)
    
    def get_weight_trend(self, weeks: int = 4) -> Tuple[float, bool]:
        """
        Calculate the trend in body weight over the specified period
        
        Args:
            weeks: Number of weeks to analyze (default: 4)
            
        Returns:
            Tuple of (weight_change_kg, is_losing)
        """
        if self.weight_df.empty:
            return (0.0, False)
        
        # Define time period
        end_date = self.weight_df['date'].max()
        start_date = end_date - timedelta(weeks=weeks)
        
        # Filter data to the time period
        filtered_df = self.weight_df[
            (self.weight_df['date'] >= start_date) & 
            (self.weight_df['date'] <= end_date)
        ]
        
        if len(filtered_df) < 2:
            return (0.0, False)
        
        # Get first and last weight in the period
        first_weight = filtered_df.iloc[0]['weight']
        last_weight = filtered_df.iloc[-1]['weight']
        
        weight_change = last_weight - first_weight
        is_losing = weight_change < 0
        
        return (weight_change, is_losing)
    
    def get_calorie_adherence(self, target_calories: float, days: int = 14) -> float:
        """
        Calculate adherence to calorie targets over the specified period
        
        Args:
            target_calories: Target daily calorie intake
            days: Number of days to analyze (default: 14)
            
        Returns:
            Adherence percentage (0-100)
        """
        if self.nutrition_df.empty:
            return 0.0
        
        # Define time period
        end_date = self.nutrition_df['date'].max()
        start_date = end_date - timedelta(days=days)
        
        # Filter data to the time period
        filtered_df = self.nutrition_df[
            (self.nutrition_df['date'] >= start_date) & 
            (self.nutrition_df['date'] <= end_date)
        ]
        
        if filtered_df.empty:
            return 0.0
        
        # Calculate difference from target for each day
        filtered_df['diff_from_target'] = abs(filtered_df['calories'] - target_calories)
        filtered_df['within_range'] = filtered_df['diff_from_target'] <= (target_calories * 0.1)  # 10% margin
        
        # Calculate adherence percentage
        adherence = filtered_df['within_range'].mean() * 100
        
        return adherence
    
    def get_macronutrient_ratios(self, days: int = 14) -> Dict[str, float]:
        """
        Calculate average macronutrient ratios over the specified period
        
        Args:
            days: Number of days to analyze (default: 14)
            
        Returns:
            Dictionary with protein_pct, carbs_pct, and fat_pct
        """
        if self.nutrition_df.empty:
            return {'protein_pct': 0, 'carbs_pct': 0, 'fat_pct': 0}
        
        # Define time period
        end_date = self.nutrition_df['date'].max()
        start_date = end_date - timedelta(days=days)
        
        # Filter data to the time period
        filtered_df = self.nutrition_df[
            (self.nutrition_df['date'] >= start_date) & 
            (self.nutrition_df['date'] <= end_date)
        ]
        
        if filtered_df.empty:
            return {'protein_pct': 0, 'carbs_pct': 0, 'fat_pct': 0}
        
        # Calculate average macronutrient intake
        avg_protein = filtered_df['protein'].mean()
        avg_carbs = filtered_df['carbs'].mean()
        avg_fat = filtered_df['fat'].mean()
        
        # Convert to calories
        protein_cals = avg_protein * 4  # 4 calories per gram
        carbs_cals = avg_carbs * 4  # 4 calories per gram
        fat_cals = avg_fat * 9  # 9 calories per gram
        
        total_cals = protein_cals + carbs_cals + fat_cals
        
        if total_cals == 0:
            return {'protein_pct': 0, 'carbs_pct': 0, 'fat_pct': 0}
        
        # Calculate percentages
        protein_pct = (protein_cals / total_cals) * 100
        carbs_pct = (carbs_cals / total_cals) * 100
        fat_pct = (fat_cals / total_cals) * 100
        
        return {
            'protein_pct': round(protein_pct, 1),
            'carbs_pct': round(carbs_pct, 1),
            'fat_pct': round(fat_pct, 1)
        }
    
    def estimate_tdee(self, height_cm: float, age_years: int, sex: str, 
                      activity_multiplier: float = 1.55, days: int = 14) -> Optional[float]:
        """
        Estimate TDEE based on nutrition and weight data
        
        Args:
            height_cm: Height in centimeters
            age_years: Age in years
            sex: 'M' for male, 'F' for female
            activity_multiplier: Activity level multiplier (default: 1.55 - moderate)
            days: Number of days to analyze (default: 14)
            
        Returns:
            Estimated TDEE or None if insufficient data
        """
        if self.nutrition_df.empty or self.weight_df.empty:
            return None
        
        # Define time period
        end_date = min(self.nutrition_df['date'].max(), self.weight_df['date'].max())
        start_date = end_date - timedelta(days=days)
        
        # Filter nutrition data to the time period
        filtered_nutrition = self.nutrition_df[
            (self.nutrition_df['date'] >= start_date) & 
            (self.nutrition_df['date'] <= end_date)
        ]
        
        # Get weight data closest to the end of the period
        latest_weight = self.weight_df[self.weight_df['date'] <= end_date]
        if latest_weight.empty:
            return None
        
        weight_kg = latest_weight.iloc[-1]['weight']
        
        # Calculate average calorie intake
        avg_calories = filtered_nutrition['calories'].mean()
        
        # Calculate BMR
        bmr = calculate_bmr(weight_kg, height_cm, age_years, sex)
        
        # Get weight change during the period
        weight_change, _ = self.get_weight_trend(weeks=int(days/7))
        
        # Each kg of weight change represents about 7700 calories
        calorie_surplus_per_day = (weight_change * 7700) / days
        
        # Estimated TDEE is the average calorie intake adjusted for weight change
        estimated_tdee = avg_calories - calorie_surplus_per_day
        
        return max(0, estimated_tdee)  # Ensure positive value