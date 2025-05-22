// User Preferences Form Component

'use client';

import { useState } from 'react';
import { UserPreferences } from '@/types/api';

interface UserPreferencesFormProps {
  preferences: UserPreferences;
  onPreferencesChange: (newPreferences: UserPreferences) => void;
}

export default function UserPreferencesForm({
  preferences,
  onPreferencesChange,
}: UserPreferencesFormProps) {
  const [targetExercisesText, setTargetExercisesText] = useState<string>(
    preferences.targetExercises.join(', ')
  );
  
  // Handle individual field changes
  const handleGoalChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onPreferencesChange({
      ...preferences,
      goal: e.target.value as UserPreferences['goal'],
    });
  };
  
  const handleTargetExercisesChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTargetExercisesText(e.target.value);
    
    // Convert comma-separated text to array
    const exercisesArray = e.target.value
      .split(',')
      .map(ex => ex.trim())
      .filter(ex => ex.length > 0);
    
    onPreferencesChange({
      ...preferences,
      targetExercises: exercisesArray,
    });
  };
  
  const handleHeightChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onPreferencesChange({
      ...preferences,
      height: Number(e.target.value),
    });
  };
  
  const handleAgeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onPreferencesChange({
      ...preferences,
      age: Number(e.target.value),
    });
  };
  
  const handleSexChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onPreferencesChange({
      ...preferences,
      sex: e.target.value as UserPreferences['sex'],
    });
  };
  
  const handleActivityMultiplierChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onPreferencesChange({
      ...preferences,
      activityMultiplier: Number(e.target.value),
    });
  };
  
  return (
    <div className="space-y-6 mb-8">
      <h2 className="text-2xl font-semibold text-gray-800">Personal Preferences</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Goal Selection */}
        <div className="space-y-2">
          <label htmlFor="goal" className="block text-sm font-medium text-gray-700">
            Main Goal
          </label>
          <select
            id="goal"
            value={preferences.goal}
            onChange={handleGoalChange}
            className="w-full rounded-md border border-gray-300 shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="muscle_gain">Muscle Gain</option>
            <option value="fat_loss">Fat Loss</option>
            <option value="maintenance">Maintenance</option>
          </select>
          <p className="text-xs text-gray-500 mt-1">
            This helps tailor recommendations for your specific goal
          </p>
        </div>
        
        {/* Height */}
        <div className="space-y-2">
          <label htmlFor="height" className="block text-sm font-medium text-gray-700">
            Height (cm)
          </label>
          <input
            type="number"
            id="height"
            value={preferences.height}
            onChange={handleHeightChange}
            min="100"
            max="250"
            step="1"
            className="w-full rounded-md border border-gray-300 shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        {/* Age */}
        <div className="space-y-2">
          <label htmlFor="age" className="block text-sm font-medium text-gray-700">
            Age (years)
          </label>
          <input
            type="number"
            id="age"
            value={preferences.age}
            onChange={handleAgeChange}
            min="16"
            max="100"
            step="1"
            className="w-full rounded-md border border-gray-300 shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        {/* Sex */}
        <div className="space-y-2">
          <label htmlFor="sex" className="block text-sm font-medium text-gray-700">
            Biological Sex
          </label>
          <select
            id="sex"
            value={preferences.sex}
            onChange={handleSexChange}
            className="w-full rounded-md border border-gray-300 shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="M">Male</option>
            <option value="F">Female</option>
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Used for metabolic calculations
          </p>
        </div>
        
        {/* Activity Multiplier */}
        <div className="space-y-2">
          <label htmlFor="activityMultiplier" className="block text-sm font-medium text-gray-700">
            Activity Multiplier
          </label>
          <input
            type="number"
            id="activityMultiplier"
            value={preferences.activityMultiplier}
            onChange={handleActivityMultiplierChange}
            min="1.2"
            max="2.0"
            step="0.05"
            className="w-full rounded-md border border-gray-300 shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-xs text-gray-500 mt-1">
            1.2 = Sedentary, 1.375 = Light activity, 1.55 = Moderate activity, 1.725 = Very active, 1.9 = Extremely active
          </p>
        </div>
      </div>
      
      {/* Target Exercises */}
      <div className="space-y-2">
        <label htmlFor="targetExercises" className="block text-sm font-medium text-gray-700">
          Target Exercises (Optional)
        </label>
        <textarea
          id="targetExercises"
          value={targetExercisesText}
          onChange={handleTargetExercisesChange}
          rows={3}
          placeholder="Bench Press, Squat, Deadlift, Pull Up"
          className="w-full rounded-md border border-gray-300 shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <p className="text-xs text-gray-500 mt-1">
          Comma-separated list of exercises you want to analyze (leave empty to analyze all)
        </p>
      </div>
    </div>
  );
}
