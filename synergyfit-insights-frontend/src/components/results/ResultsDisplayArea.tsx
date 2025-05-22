// Results Display Area Component

import { FullApiResponse } from '@/types/api';
import SummaryCard from './SummaryCard';
import WorkoutProgressionCard from './WorkoutProgressionCard';
import NutritionWeightCard from './NutritionWeightCard';
import RecommendationItem from './RecommendationItem';

interface ResultsDisplayAreaProps {
  results: FullApiResponse;
}

export default function ResultsDisplayArea({ results }: ResultsDisplayAreaProps) {
  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Analysis Results</h2>
      
      {/* Summary Card */}
      <SummaryCard data={results.summary} />
      
      {/* Workout Progression Cards */}
      <h3 className="text-xl font-semibold text-gray-700 mb-4">Exercise Progress</h3>
      <div className="space-y-6">
        {results.workoutProgression.map((exercise) => (
          <WorkoutProgressionCard 
            key={exercise.exerciseName} 
            data={exercise} 
          />
        ))}
      </div>
      
      {/* Nutrition and Weight Card */}
      <h3 className="text-xl font-semibold text-gray-700 my-4">Nutrition & Weight Analysis</h3>
      <NutritionWeightCard data={results.nutritionWeightTrends} />
      
      {/* General Recommendations */}
      {results.generalRecommendations && results.generalRecommendations.length > 0 && (
        <>
          <h3 className="text-xl font-semibold text-gray-700 my-4">General Recommendations</h3>
          <div className="space-y-2 mb-6">
            {results.generalRecommendations.map((recommendation, index) => (
              <RecommendationItem 
                key={index}
                recommendation={recommendation}
                index={index}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
