import pandas as pd
from datetime import datetime
from typing import List, Dict, Set

from parsers.base_parser import BaseParser
from data_models.workout_models import WorkoutData, ExerciseData, SetData

class StrongParser(BaseParser[WorkoutData]):
    """
    Parser for Strong app CSV exports
    """
    
    def parse(self, file_path: str) -> List[WorkoutData]:
        """
        Parse Strong CSV export file and convert to WorkoutData objects
        
        Args:
            file_path: Path to the Strong CSV export file
            
        Returns:
            List of WorkoutData objects
        """
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert date strings to datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Group by date and workout name
        workouts = {}
        workout_exercises = {}
        
        for _, row in df.iterrows():
            # Create a unique key for each workout
            date_obj = row['Date'].date()
            workout_key = (date_obj, row['Workout Name'])
            
            # Create or get the workout data object
            if workout_key not in workouts:
                workouts[workout_key] = WorkoutData(
                    date=date_obj,
                    routine_name=row['Workout Name'],
                    exercises=[],
                    sets=[]
                )
                workout_exercises[workout_key] = set()
            
            # Add the exercise if it doesn't exist yet
            exercise_name = row['Exercise Name']
            if exercise_name not in workout_exercises[workout_key]:
                workout_exercises[workout_key].add(exercise_name)
                workouts[workout_key].exercises.append(
                    ExerciseData(name=exercise_name)
                )
            
            # Create and add the set data
            # Handle potential missing or NaN values
            weight = row.get('Weight', None)
            weight = float(weight) if pd.notna(weight) else None
            
            reps = row.get('Reps', None)
            reps = int(reps) if pd.notna(reps) else None
            
            distance = row.get('Distance', None)
            distance = float(distance) if pd.notna(distance) else None
            
            seconds = row.get('Seconds', None)
            seconds = int(seconds) if pd.notna(seconds) else None
            
            set_data = SetData(
                exercise_name=exercise_name,
                weight_kg=weight,
                reps=reps,
                distance_km=distance,
                duration_seconds=seconds,
                is_completed=True  # Assume completed since it's in the export
            )
            
            workouts[workout_key].sets.append(set_data)
        
        # Return as list of WorkoutData objects
        return list(workouts.values())

def parse_strong_csv(file_path: str) -> List[WorkoutData]:
    """
    Helper function to parse Strong CSV export
    
    Args:
        file_path: Path to the Strong CSV export file
        
    Returns:
        List of WorkoutData objects
    """
    parser = StrongParser()
    return parser.parse(file_path)