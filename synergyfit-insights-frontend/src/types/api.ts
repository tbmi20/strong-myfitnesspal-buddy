// TypeScript interfaces for API responses

// User preferences interface
export interface UserPreferences {
  goal: 'muscle_gain' | 'fat_loss' | 'maintenance';
  targetExercises: string[];
  height: number;
  age: number;
  sex: 'M' | 'F';
  activityMultiplier: number;
}

// Chart data point interface
export interface ChartDataPoint {
  date: string;
  value: number;
}

// Analysis summary interface
export interface AnalysisSummary {
  estimatedTDEE: number;
  currentBMR: number;
  suggestedCalorieTarget: number;
  keyRecommendation: string;
}

// Workout progression data interface
export interface WorkoutProgressionData {
  exerciseName: string;
  e1rmTrendData: ChartDataPoint[];
  volumeTrendData: ChartDataPoint[];
  stagnationInfo?: string;
  progressionSuggestion?: string;
  lastPerformance: {
    date: string;
    weight: number;
    reps: number;
    estimatedOneRepMax: number;
  };
}

// Nutrition and weight trends interface
export interface NutritionWeightTrends {
  weightTrendData: ChartDataPoint[];
  currentWeight: number;
  totalWeightChange: number;
  recentWeightChange: number;
  avgDailyCalories: number;
  macroBreakdown: {
    protein: {
      grams: number;
      percentage: number;
    };
    carbs: {
      grams: number;
      percentage: number;
    };
    fat: {
      grams: number;
      percentage: number;
    };
  };
  suggestedCalories: number;
}

// Full API response interface
export interface FullApiResponse {
  summary: AnalysisSummary;
  workoutProgression: WorkoutProgressionData[];
  nutritionWeightTrends: NutritionWeightTrends;
  generalRecommendations: string[];
}
