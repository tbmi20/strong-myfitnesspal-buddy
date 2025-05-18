import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

from parsers.base_parser import BaseParser
from data_models.nutrition_models import DailyNutritionData, WeightData

class MFPNutritionParser(BaseParser[DailyNutritionData]):
    """
    Parser for MyFitnessPal nutrition data exports
    """
    
    def parse(self, file_path: str) -> List[DailyNutritionData]:
        """
        Parse MyFitnessPal nutrition CSV export and convert to DailyNutritionData objects
        
        Args:
            file_path: Path to the nutrition CSV export file
            
        Returns:
            List of DailyNutritionData objects
        """
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert date strings to datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Group by date and sum nutrients for each day
        daily_totals = {}
        
        for _, row in df.iterrows():
            date_obj = row['Date'].date()
            
            # Get or create the daily total entry
            if date_obj not in daily_totals:
                daily_totals[date_obj] = {
                    'calories': 0.0,
                    'protein': 0.0,
                    'carbs': 0.0,
                    'fat': 0.0,
                    'fiber': 0.0,
                    'sugar': 0.0,
                    'sodium': 0.0,
                    'cholesterol': 0.0,
                }
            
            # Add this meal's nutrients to the daily total
            daily_totals[date_obj]['calories'] += float(row.get('Calories', 0) or 0)
            daily_totals[date_obj]['protein'] += float(row.get('Protein (g)', 0) or 0)
            daily_totals[date_obj]['carbs'] += float(row.get('Carbohydrates (g)', 0) or 0)
            daily_totals[date_obj]['fat'] += float(row.get('Fat (g)', 0) or 0)
            
            # Add optional nutrients if available
            daily_totals[date_obj]['fiber'] += float(row.get('Fiber', 0) or 0)
            daily_totals[date_obj]['sugar'] += float(row.get('Sugar', 0) or 0)
            daily_totals[date_obj]['sodium'] += float(row.get('Sodium (mg)', 0) or 0)
            daily_totals[date_obj]['cholesterol'] += float(row.get('Cholesterol', 0) or 0)
        
        # Convert the daily totals to DailyNutritionData objects
        result = []
        for date_obj, nutrients in daily_totals.items():
            nutrition_data = DailyNutritionData(
                date=date_obj,
                calories_kcal=nutrients['calories'],
                protein_g=nutrients['protein'],
                carbs_g=nutrients['carbs'],
                fat_g=nutrients['fat'],
                fiber_g=nutrients['fiber'],
                sugar_g=nutrients['sugar'],
                sodium_mg=nutrients['sodium'],
                cholesterol_mg=nutrients['cholesterol']
            )
            result.append(nutrition_data)
        
        return result


class MFPWeightParser(BaseParser[WeightData]):
    """
    Parser for MyFitnessPal weight data exports
    """
    
    def parse(self, file_path: str) -> List[WeightData]:
        """
        Parse MyFitnessPal weight CSV export and convert to WeightData objects
        
        Args:
            file_path: Path to the weight measurements CSV export file
            
        Returns:
            List of WeightData objects
        """
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert date strings to datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Convert the rows to WeightData objects
        result = []
        for _, row in df.iterrows():
            date_obj = row['Date'].date()
            weight_kg = float(row['Weight'])
            
            # Body fat percentage may not be present in the export
            body_fat = None
            if 'Body Fat %' in df.columns and pd.notna(row.get('Body Fat %')):
                body_fat = float(row['Body Fat %'])
            
            weight_data = WeightData(
                date=date_obj,
                weight_kg=weight_kg,
                body_fat_percentage=body_fat
            )
            result.append(weight_data)
        
        return result


def parse_mfp_csv_nutrition(file_path: str) -> List[DailyNutritionData]:
    """
    Helper function to parse MyFitnessPal nutrition CSV export
    
    Args:
        file_path: Path to the nutrition CSV export file
        
    Returns:
        List of DailyNutritionData objects
    """
    parser = MFPNutritionParser()
    return parser.parse(file_path)


def parse_mfp_csv_weight(file_path: str) -> List[WeightData]:
    """
    Helper function to parse MyFitnessPal weight CSV export
    
    Args:
        file_path: Path to the weight measurements CSV export file
        
    Returns:
        List of WeightData objects
    """
    parser = MFPWeightParser()
    return parser.parse(file_path)