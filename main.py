#!/usr/bin/env python3
# Main script for fitness analysis tool

import os
import pandas as pd
import numpy as np
import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# Import parsers
from parsers.strong_parser import parse_strong_csv
from parsers.mfp_parser import parse_mfp_csv_nutrition, parse_mfp_csv_weight

# Import analysis modules
from analysis.workout_analysis import WorkoutAnalyzer
from analysis.nutrition_analysis import NutritionAnalyzer
from analysis.insights import InsightGenerator

# Define file paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
STRONG_CSV = os.path.join(DATA_DIR, "strong.csv")
NUTRITION_CSV = os.path.join(DATA_DIR, "Nutrition-Summary-2025-04-15-to-2025-05-15.csv")
EXERCISE_CSV = os.path.join(DATA_DIR, "Exercise-Summary-2025-04-15-to-2025-05-15.csv")
MEASUREMENT_CSV = os.path.join(DATA_DIR, "Measurement-Summary-2025-04-15-to-2025-05-15.csv")

def load_strong_data():
    """
    Load and parse Strong workout data
    """
    print("Loading Strong workout data...")
    workout_data = parse_strong_csv(STRONG_CSV)
    print(f"Loaded {len(workout_data)} workouts")
    return workout_data

def load_nutrition_data():
    """
    Load and parse MyFitnessPal nutrition data
    """
    print("Loading nutrition data...")
    nutrition_data = parse_mfp_csv_nutrition(NUTRITION_CSV)
    print(f"Loaded data for {len(nutrition_data)} days")
    return nutrition_data

def load_weight_data():
    """
    Load and parse MyFitnessPal weight data
    """
    print("Loading weight data...")
    weight_data = parse_mfp_csv_weight(MEASUREMENT_CSV)
    print(f"Loaded {len(weight_data)} weight measurements")
    return weight_data

def explore_data():
    """
    Print basic information about each dataset and perform some analysis
    """
    print("\n=== Exploring Data ===\n")
    
    # Load the data
    workout_data = load_strong_data()
    nutrition_data = load_nutrition_data()
    weight_data = load_weight_data()
    
    # Show some information about the loaded data
    if workout_data:
        print(f"\nFirst workout date: {workout_data[0].date}")
        print(f"Last workout date: {workout_data[-1].date}")
        
        # Count unique exercises
        all_exercises = set()
        for workout in workout_data:
            for exercise in workout.exercises:
                all_exercises.add(exercise.name)
        print(f"Total unique exercises: {len(all_exercises)}")
        print("Sample exercises:", list(all_exercises)[:5])
    
    if nutrition_data:
        print(f"\nFirst nutrition date: {nutrition_data[0].date}")
        print(f"Last nutrition date: {nutrition_data[-1].date}")
        
        # Show average calorie and protein intake
        total_calories = sum(n.calories_kcal for n in nutrition_data)
        total_protein = sum(n.protein_g for n in nutrition_data)
        avg_calories = total_calories / len(nutrition_data)
        avg_protein = total_protein / len(nutrition_data)
        print(f"Average daily calories: {avg_calories:.1f} kcal")
        print(f"Average daily protein: {avg_protein:.1f} g")
    
    if weight_data:
        print(f"\nFirst weight measurement date: {weight_data[0].date}")
        print(f"Last weight measurement date: {weight_data[-1].date}")
        
        # Show weight change
        first_weight = weight_data[0].weight_kg
        last_weight = weight_data[-1].weight_kg
        weight_change = last_weight - first_weight
        print(f"Starting weight: {first_weight:.1f} kg")
        print(f"Current weight: {last_weight:.1f} kg")
        print(f"Weight change: {weight_change:.1f} kg")
    
    return workout_data, nutrition_data, weight_data

def generate_insights(workout_data, nutrition_data, weight_data):
    """
    Generate insights from the fitness data
    """
    print("\n=== Generating Insights ===\n")
    
    # Initialize the insight generator
    insight_generator = InsightGenerator(workout_data, nutrition_data, weight_data)
    
    # User information (example values)
    height_cm = 175
    age_years = 30
    sex = 'M'
    goal = 'muscle_gain'  # 'muscle_gain', 'fat_loss', or 'maintenance'
    
    # Generate insights
    insights = insight_generator.get_combined_insights(
        height_cm=height_cm,
        age_years=age_years,
        sex=sex,
        goal=goal
    )
    
    # Display insights
    print(f"Goal: {goal.replace('_', ' ').title()}")
    
    print("\nStats:")
    stats = insights['stats']
    if stats['weight_change_kg'] is not None:
        print(f"- Weight change (4 weeks): {stats['weight_change_kg']} kg")
    
    if stats['macro_ratios']:
        print(f"- Macronutrient ratios: Protein {stats['macro_ratios']['protein_pct']}%, "
              f"Carbs {stats['macro_ratios']['carbs_pct']}%, "
              f"Fat {stats['macro_ratios']['fat_pct']}%")
    
    if stats['estimated_tdee']:
        print(f"- Estimated TDEE: {stats['estimated_tdee']} kcal")
    
    if stats['suggested_calorie_target']:
        print(f"- Suggested calorie target: {stats['suggested_calorie_target']} kcal")
    
    print("\nRecommendations:")
    for rec_type, recommendations in insights['recommendations'].items():
        if recommendations:
            print(f"\n{rec_type.title()} Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. [{rec['priority'].upper()}] {rec['message']}")
    
    # Exercise progress example
    if workout_data:
        print("\nExercise Progress Examples:")
        # Find some common exercises to analyze
        all_exercises = set()
        for workout in workout_data:
            for exercise in workout.exercises:
                all_exercises.add(exercise.name)
        
        # Take the first few exercises as examples
        example_exercises = list(all_exercises)[:3]
        
        workout_analyzer = WorkoutAnalyzer(workout_data)
        for exercise_name in example_exercises:
            progress_df = workout_analyzer.get_exercise_progress(exercise_name)
            if not progress_df.empty:
                print(f"\n{exercise_name} Progress:")
                if len(progress_df) > 1:
                    first_entry = progress_df.iloc[0]
                    last_entry = progress_df.iloc[-1]
                    print(f"- First recorded: {first_entry['date']} - {first_entry['max_weight_kg']} kg x {first_entry['max_reps']} reps")
                    print(f"- Latest: {last_entry['date']} - {last_entry['max_weight_kg']} kg x {last_entry['max_reps']} reps")
                    print(f"- 1RM estimate: {last_entry['estimated_1rm_kg']:.1f} kg")
                else:
                    print("- Insufficient data for progress analysis")

if __name__ == "__main__":
    print("Fitness Analyzer - Data Exploration and Analysis")
    
    # Explore data
    workout_data, nutrition_data, weight_data = explore_data()
    
    # Generate insights if data is available
    if workout_data and nutrition_data and weight_data:
        generate_insights(workout_data, nutrition_data, weight_data)
    else:
        print("\nNot enough data for comprehensive analysis.")
        
    print("\nAnalysis complete!")