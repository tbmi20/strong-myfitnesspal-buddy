#!/usr/bin/env python3
# Flask API server for SynergyFit Insights

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import tempfile
from datetime import datetime, timedelta
import random

# Import our analysis modules
from parsers.strong_parser import parse_strong_csv
from parsers.mfp_parser import parse_mfp_csv_nutrition, parse_mfp_csv_weight
from analysis.workout_analysis import WorkoutAnalyzer
from analysis.nutrition_analysis import NutritionAnalyzer
from analysis.insights import InsightGenerator
from utils.formulas import calculate_bmr, calculate_tdee

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze uploaded fitness data files and return insights
    """
    try:
        # Check if all files are present
        if 'strong_file' not in request.files or \
           'nutrition_file' not in request.files or \
           'weight_file' not in request.files:
            return jsonify({
                'error': 'Missing one or more required files'
            }), 400
        
        # Get the files
        strong_file = request.files['strong_file']
        nutrition_file = request.files['nutrition_file']
        weight_file = request.files['weight_file']
        
        # Parse user preferences
        user_preferences_json = request.form.get('user_preferences_json', '{}')
        user_preferences = json.loads(user_preferences_json)
        
        # Create temporary files to save the uploaded data
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_strong, \
             tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_nutrition, \
             tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_weight:
            
            strong_file.save(temp_strong.name)
            nutrition_file.save(temp_nutrition.name)
            weight_file.save(temp_weight.name)
            
            # Parse the data files
            workout_data = parse_strong_csv(temp_strong.name)
            nutrition_data = parse_mfp_csv_nutrition(temp_nutrition.name)
            weight_data = parse_mfp_csv_weight(temp_weight.name)
            
            # Create analyzers
            workout_analyzer = WorkoutAnalyzer(workout_data)
            nutrition_analyzer = NutritionAnalyzer(nutrition_data, weight_data)
            
            # Get user physical data from preferences
            height_cm = user_preferences.get('height', 175)
            age_years = user_preferences.get('age', 30)
            sex = user_preferences.get('sex', 'M')
            activity_multiplier = user_preferences.get('activityMultiplier', 1.55)
            goal = user_preferences.get('goal', 'muscle_gain')
            target_exercises = user_preferences.get('targetExercises', [])
            
            # For demo purposes, if no target exercises are specified, use some common ones
            if not target_exercises:
                all_exercises = set()
                for workout in workout_data:
                    for exercise in workout.exercises:
                        all_exercises.add(exercise.name)
                
                # Take up to 3 random exercises for analysis
                exercise_list = list(all_exercises)
                target_exercises = random.sample(exercise_list, min(3, len(exercise_list)))
            
            # Get basic insights
            insight_generator = InsightGenerator(workout_data, nutrition_data, weight_data)
            insights = insight_generator.get_combined_insights(
                height_cm=height_cm,
                age_years=age_years,
                sex=sex,
                goal=goal
            )
            
            # Get weight and nutrition data
            weight_change, is_losing = nutrition_analyzer.get_weight_trend(weeks=4)
            macro_ratios = nutrition_analyzer.get_macronutrient_ratios(days=14)
            
            # Get latest weight
            latest_weight = None
            if weight_data:
                latest_weight = sorted(weight_data, key=lambda x: x.date)[-1].weight_kg
            
            # Calculate BMR/TDEE
            bmr = None
            tdee = None
            suggested_calories = None
            
            if latest_weight:
                bmr = calculate_bmr(latest_weight, height_cm, age_years, sex)
                tdee = calculate_tdee(bmr, activity_multiplier)
                
                # Adjust calories based on goal
                if goal == 'muscle_gain':
                    suggested_calories = tdee + 300  # Surplus for muscle gain
                elif goal == 'fat_loss':
                    suggested_calories = max(tdee - 500, 1200)  # Deficit for fat loss (min 1200)
                else:
                    suggested_calories = tdee  # Maintenance
            
            # Build the response payload
            response = {
                'summary': {
                    'estimatedTDEE': round(tdee) if tdee else 2000,
                    'currentBMR': round(bmr) if bmr else 1500,
                    'suggestedCalorieTarget': round(suggested_calories) if suggested_calories else 2000,
                    'keyRecommendation': insights['recommendations']['nutrition'][0]['message'] 
                        if insights.get('recommendations', {}).get('nutrition') else 
                        "Focus on progressive overload and consistent nutrition tracking."
                },
                'workoutProgression': [],
                'nutritionWeightTrends': {
                    'weightTrendData': [],
                    'currentWeight': latest_weight or 70,
                    'totalWeightChange': 0,
                    'recentWeightChange': round(weight_change, 1) if weight_change is not None else 0,
                    'avgDailyCalories': 0,
                    'macroBreakdown': {
                        'protein': {
                            'grams': 0,
                            'percentage': macro_ratios.get('protein_pct', 25)
                        },
                        'carbs': {
                            'grams': 0,
                            'percentage': macro_ratios.get('carbs_pct', 50)
                        },
                        'fat': {
                            'grams': 0,
                            'percentage': macro_ratios.get('fat_pct', 25)
                        }
                    },
                    'suggestedCalories': round(suggested_calories) if suggested_calories else 2000
                },
                'generalRecommendations': []
            }
            
            # Get general recommendations from insights
            for rec_type, recommendations in insights.get('recommendations', {}).items():
                for rec in recommendations:
                    response['generalRecommendations'].append(rec['message'])
            
            # Process workout progression for target exercises
            for exercise_name in target_exercises:
                progress_df = workout_analyzer.get_exercise_progress(exercise_name)
                
                if not progress_df.empty:
                    # Extract data points for the charts
                    e1rm_data = []
                    volume_data = []
                    
                    for _, row in progress_df.iterrows():
                        date_str = row['date'].strftime('%Y-%m-%d')
                        
                        e1rm_data.append({
                            'date': date_str,
                            'value': round(float(row['estimated_1rm_kg']), 1)
                        })
                        
                        volume_data.append({
                            'date': date_str,
                            'value': round(float(row['volume_kg']), 1)
                        })
                    
                    # Get stagnation info
                    percent_change, is_improving = workout_analyzer.get_volume_trend(exercise_name)
                    stagnation_info = None
                    progression_suggestion = None
                    
                    if not is_improving:
                        stagnation_info = f"Your progress on {exercise_name} has stalled. Volume has decreased by {abs(round(percent_change, 1))}% over the past 8 weeks."
                        progression_suggestion = f"Try varying your rep ranges, add an extra set, or increase frequency for {exercise_name}."
                    elif percent_change < 5:
                        stagnation_info = f"Your progress on {exercise_name} is minimal. Volume has only increased by {round(percent_change, 1)}% over the past 8 weeks."
                        progression_suggestion = f"Consider adding 5-10% more volume to your {exercise_name} workouts."
                    
                    # Get last performance
                    last_row = progress_df.iloc[-1]
                    last_performance = {
                        'date': last_row['date'].strftime('%Y-%m-%d'),
                        'weight': float(last_row['max_weight_kg']),
                        'reps': int(last_row['max_reps']),
                        'estimatedOneRepMax': round(float(last_row['estimated_1rm_kg']), 1)
                    }
                    
                    # Add exercise data to response
                    response['workoutProgression'].append({
                        'exerciseName': exercise_name,
                        'e1rmTrendData': e1rm_data,
                        'volumeTrendData': volume_data,
                        'stagnationInfo': stagnation_info,
                        'progressionSuggestion': progression_suggestion,
                        'lastPerformance': last_performance
                    })
            
            # Process nutrition and weight data for charts
            if weight_data:
                weight_trend_data = []
                sorted_weight_data = sorted(weight_data, key=lambda x: x.date)
                
                # Calculate total weight change
                if len(sorted_weight_data) >= 2:
                    first_weight = sorted_weight_data[0].weight_kg
                    last_weight = sorted_weight_data[-1].weight_kg
                    response['nutritionWeightTrends']['totalWeightChange'] = round(last_weight - first_weight, 1)
                
                # Generate weight trend data points
                for weight_entry in sorted_weight_data:
                    weight_trend_data.append({
                        'date': weight_entry.date.strftime('%Y-%m-%d'),
                        'value': weight_entry.weight_kg
                    })
                
                response['nutritionWeightTrends']['weightTrendData'] = weight_trend_data
            
            # Process nutrition data for average calories and macros
            if nutrition_data:
                total_calories = sum(n.calories_kcal for n in nutrition_data)
                avg_calories = total_calories / len(nutrition_data)
                response['nutritionWeightTrends']['avgDailyCalories'] = round(avg_calories)
                
                # Calculate average macros in grams
                total_protein = sum(n.protein_g for n in nutrition_data)
                total_carbs = sum(n.carbs_g for n in nutrition_data)
                total_fat = sum(n.fat_g for n in nutrition_data)
                
                avg_protein = total_protein / len(nutrition_data)
                avg_carbs = total_carbs / len(nutrition_data)
                avg_fat = total_fat / len(nutrition_data)
                
                response['nutritionWeightTrends']['macroBreakdown']['protein']['grams'] = round(avg_protein)
                response['nutritionWeightTrends']['macroBreakdown']['carbs']['grams'] = round(avg_carbs)
                response['nutritionWeightTrends']['macroBreakdown']['fat']['grams'] = round(avg_fat)
            
            # Clean up temporary files
            os.unlink(temp_strong.name)
            os.unlink(temp_nutrition.name)
            os.unlink(temp_weight.name)
            
            return jsonify(response)
            
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)