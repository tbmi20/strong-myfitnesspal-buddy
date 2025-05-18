import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import date, timedelta
from collections import defaultdict

from data_models.workout_models import WorkoutData, ExerciseData, SetData
from utils.formulas import estimate_one_rep_max

class WorkoutAnalyzer:
    """
    Analyzes workout data to track progress and generate insights
    """
    
    def __init__(self, workout_data: List[WorkoutData]):
        """
        Initialize with a list of workout data
        
        Args:
            workout_data: List of WorkoutData objects
        """
        self.workout_data = sorted(workout_data, key=lambda x: x.date)
        self._process_data()
    
    def _process_data(self):
        """Process the workout data for analysis"""
        # Group workouts by exercise name
        self.exercise_workouts = defaultdict(list)
        for workout in self.workout_data:
            for set_data in workout.sets:
                self.exercise_workouts[set_data.exercise_name].append((workout.date, set_data))
        
        # Calculate volume per exercise per workout
        self.exercise_volumes = defaultdict(lambda: defaultdict(float))
        for exercise, sets in self.exercise_workouts.items():
            for workout_date, set_data in sets:
                # Skip if missing weight or reps
                if set_data.weight_kg is None or set_data.reps is None:
                    continue
                
                # Add to total volume (weight * reps)
                self.exercise_volumes[exercise][workout_date] += set_data.weight_kg * set_data.reps
    
    def get_exercise_progress(self, exercise_name: str) -> pd.DataFrame:
        """
        Get progress data for a specific exercise over time
        
        Args:
            exercise_name: Name of the exercise to analyze
            
        Returns:
            DataFrame with exercise progress metrics (date, max_weight, max_reps, volume, estimated_1rm)
        """
        if exercise_name not in self.exercise_workouts:
            return pd.DataFrame()
        
        # Prepare data structure
        progress_data = []
        
        # Group sets by workout date
        sets_by_date = defaultdict(list)
        for date_obj, set_data in self.exercise_workouts[exercise_name]:
            sets_by_date[date_obj].append(set_data)
        
        # Process each workout date
        for date_obj, sets in sorted(sets_by_date.items()):
            # Skip if no weight or reps data
            valid_sets = [s for s in sets if s.weight_kg is not None and s.reps is not None]
            if not valid_sets:
                continue
            
            # Calculate metrics
            max_weight = max([s.weight_kg for s in valid_sets])
            max_reps = max([s.reps for s in valid_sets])
            total_volume = sum([s.weight_kg * s.reps for s in valid_sets])
            
            # Find the set with the highest estimated 1RM
            best_1rm = 0
            for set_data in valid_sets:
                est_1rm = estimate_one_rep_max(set_data.weight_kg, set_data.reps)
                best_1rm = max(best_1rm, est_1rm)
            
            progress_data.append({
                'date': date_obj,
                'max_weight_kg': max_weight,
                'max_reps': max_reps,
                'volume_kg': total_volume,
                'estimated_1rm_kg': best_1rm
            })
        
        return pd.DataFrame(progress_data)
    
    def get_volume_trend(self, exercise_name: str, weeks: int = 8) -> Tuple[float, bool]:
        """
        Calculate the trend in exercise volume over the specified period
        
        Args:
            exercise_name: Name of the exercise to analyze
            weeks: Number of weeks to analyze (default: 8)
            
        Returns:
            Tuple of (percent_change, is_improving)
        """
        if exercise_name not in self.exercise_volumes:
            return (0.0, False)
        
        # Get volume by date for this exercise
        volumes = self.exercise_volumes[exercise_name]
        if not volumes:
            return (0.0, False)
        
        # Filter to the specified time period
        end_date = max(volumes.keys())
        start_date = end_date - timedelta(weeks=weeks)
        
        # Get the earliest and latest workout in this period
        dates_in_range = [d for d in volumes.keys() if d >= start_date]
        if len(dates_in_range) < 2:
            return (0.0, False)
        
        first_date = min(dates_in_range)
        last_date = max(dates_in_range)
        
        # Calculate percent change
        first_volume = volumes[first_date]
        last_volume = volumes[last_date]
        
        if first_volume == 0:
            return (0.0, last_volume > 0)
        
        percent_change = ((last_volume - first_volume) / first_volume) * 100
        return (percent_change, percent_change > 0)
    
    def get_workout_frequency(self, weeks: int = 4) -> Dict[str, int]:
        """
        Calculate workout frequency by routine type over the specified period
        
        Args:
            weeks: Number of weeks to analyze (default: 4)
            
        Returns:
            Dictionary of {routine_name: count}
        """
        if not self.workout_data:
            return {}
        
        # Define time period
        end_date = max([w.date for w in self.workout_data])
        start_date = end_date - timedelta(weeks=weeks)
        
        # Count workouts by routine name
        routine_counts = defaultdict(int)
        for workout in self.workout_data:
            if workout.date >= start_date and workout.date <= end_date:
                routine_name = workout.routine_name or "Unnamed"
                routine_counts[routine_name] += 1
        
        return dict(routine_counts)
    
    def identify_stalled_exercises(self, weeks: int = 8, threshold: float = 5.0) -> List[str]:
        """
        Identify exercises where progress has stalled or regressed
        
        Args:
            weeks: Number of weeks to analyze (default: 8)
            threshold: Minimum percent improvement expected (default: 5%)
            
        Returns:
            List of exercise names that have stalled
        """
        stalled = []
        
        for exercise in self.exercise_volumes.keys():
            percent_change, is_improving = self.get_volume_trend(exercise, weeks)
            if not is_improving or percent_change < threshold:
                stalled.append(exercise)
        
        return stalled