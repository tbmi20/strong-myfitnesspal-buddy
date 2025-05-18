#!/usr/bin/env python3
# Main script for fitness analysis tool

import os
import pandas as pd
import numpy as np
import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

# Define file paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
STRONG_CSV = os.path.join(DATA_DIR, "strong.csv")
NUTRITION_CSV = os.path.join(DATA_DIR, "Nutrition-Summary-2025-04-15-to-2025-05-15.csv")
EXERCISE_CSV = os.path.join(DATA_DIR, "Exercise-Summary-2025-04-15-to-2025-05-15.csv")
MEASUREMENT_CSV = os.path.join(DATA_DIR, "Measurement-Summary-2025-04-15-to-2025-05-15.csv")

def load_strong_data() -> pd.DataFrame:
    """
    Load and parse Strong workout data
    """
    print("Loading Strong workout data...")
    df = pd.read_csv(STRONG_CSV, parse_dates=["Date"])
    print(f"Loaded {len(df)} rows of workout data")
    return df

def load_nutrition_data() -> pd.DataFrame:
    """
    Load and parse MyFitnessPal nutrition data
    """
    print("Loading nutrition data...")
    df = pd.read_csv(NUTRITION_CSV, parse_dates=["Date"])
    print(f"Loaded {len(df)} rows of nutrition data")
    return df

def load_exercise_data() -> pd.DataFrame:
    """
    Load and parse MyFitnessPal exercise data
    """
    print("Loading exercise data...")
    df = pd.read_csv(EXERCISE_CSV, parse_dates=["Date"])
    print(f"Loaded {len(df)} rows of exercise data")
    return df

def load_measurement_data() -> pd.DataFrame:
    """
    Load and parse MyFitnessPal measurement (weight) data
    """
    print("Loading measurement data...")
    df = pd.read_csv(MEASUREMENT_CSV, parse_dates=["Date"])
    print(f"Loaded {len(df)} rows of measurement data")
    return df

def explore_data():
    """
    Print basic information about each dataset to understand its structure
    """
    print("\n=== Exploring Data ===\n")
    
    # Strong data
    strong_df = load_strong_data()
    print("\nStrong Data Sample:")
    print(strong_df.head())
    print("\nStrong Data Columns:")
    print(strong_df.columns.tolist())
    
    # Nutrition data
    nutrition_df = load_nutrition_data()
    print("\nNutrition Data Sample:")
    print(nutrition_df.head())
    print("\nNutrition Data Columns:")
    print(nutrition_df.columns.tolist())
    
    # Exercise data
    exercise_df = load_exercise_data()
    print("\nExercise Data Sample:")
    print(exercise_df.head())
    print("\nExercise Data Columns:")
    print(exercise_df.columns.tolist())
    
    # Measurement data
    measurement_df = load_measurement_data()
    print("\nMeasurement Data Sample:")
    print(measurement_df.head())
    print("\nMeasurement Data Columns:")
    print(measurement_df.columns.tolist())

if __name__ == "__main__":
    print("Fitness Analyzer - Data Exploration")
    explore_data()