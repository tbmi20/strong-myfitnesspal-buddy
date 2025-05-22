// Workout Progression Card Component

import { WorkoutProgressionData } from '@/types/api';
import LineChart from '@/components/charts/LineChart';

interface WorkoutProgressionCardProps {
  data: WorkoutProgressionData;
}

export default function WorkoutProgressionCard({ data }: WorkoutProgressionCardProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">{data.exerciseName}</h2>
      
      <div className="space-y-6">
        {/* Charts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* 1RM Trend Chart */}
          <div className="border rounded-md p-4">
            <h3 className="text-md font-semibold text-gray-700 mb-2">Estimated 1RM Trend</h3>
            <LineChart 
              data={data.e1rmTrendData} 
              title="Est. 1RM" 
              yAxisLabel="Weight (kg)" 
              color="rgb(34, 139, 230)"
            />
          </div>
          
          {/* Volume Trend Chart */}
          <div className="border rounded-md p-4">
            <h3 className="text-md font-semibold text-gray-700 mb-2">Volume Trend</h3>
            <LineChart 
              data={data.volumeTrendData} 
              title="Volume" 
              yAxisLabel="Volume (kg)" 
              color="rgb(68, 64, 204)"
            />
          </div>
        </div>
        
        {/* Last Performance */}
        <div className="bg-gray-50 p-4 rounded-md">
          <h3 className="text-md font-semibold text-gray-700 mb-2">Last Performance</h3>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-sm text-gray-500">Date</div>
              <div className="font-medium">{new Date(data.lastPerformance.date).toLocaleDateString()}</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Weight x Reps</div>
              <div className="font-medium">
                {data.lastPerformance.weight} kg x {data.lastPerformance.reps}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Estimated 1RM</div>
              <div className="font-medium">{data.lastPerformance.estimatedOneRepMax} kg</div>
            </div>
          </div>
        </div>
        
        {/* Stagnation Info */}
        {data.stagnationInfo && (
          <div className="bg-yellow-50 p-4 rounded-md border border-yellow-200">
            <h3 className="text-md font-semibold text-yellow-700 mb-1">Stagnation Analysis</h3>
            <p className="text-gray-700">{data.stagnationInfo}</p>
          </div>
        )}
        
        {/* Progression Suggestion */}
        {data.progressionSuggestion && (
          <div className="bg-green-50 p-4 rounded-md border border-green-200">
            <h3 className="text-md font-semibold text-green-700 mb-1">Progression Suggestion</h3>
            <p className="text-gray-700">{data.progressionSuggestion}</p>
          </div>
        )}
      </div>
    </div>
  );
}
