// Nutrition and Weight Card Component

import { NutritionWeightTrends } from '@/types/api';
import LineChart from '@/components/charts/LineChart';
import BarChart from '@/components/charts/BarChart';

interface NutritionWeightCardProps {
  data: NutritionWeightTrends;
}

export default function NutritionWeightCard({ data }: NutritionWeightCardProps) {
  // Prepare data for the macros bar chart
  const macroLabels = ['Protein', 'Carbs', 'Fat'];
  const macroData = [
    data.macroBreakdown.protein.grams,
    data.macroBreakdown.carbs.grams,
    data.macroBreakdown.fat.grams
  ];
  const macroPercentages = [
    data.macroBreakdown.protein.percentage,
    data.macroBreakdown.carbs.percentage,
    data.macroBreakdown.fat.percentage
  ];

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Nutrition & Weight Trends</h2>
      
      <div className="space-y-6">
        {/* Weight Trend Chart */}
        <div className="border rounded-md p-4">
          <h3 className="text-md font-semibold text-gray-700 mb-2">Weight Trend</h3>
          <LineChart 
            data={data.weightTrendData} 
            title="Weight" 
            yAxisLabel="Weight (kg)" 
            color="rgb(234, 88, 12)"
          />
        </div>
        
        {/* Weight Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-orange-50 p-4 rounded-md border border-orange-200">
            <div className="text-sm text-gray-500">Current Weight</div>
            <div className="text-2xl font-bold text-gray-800">{data.currentWeight} kg</div>
          </div>
          
          <div className="bg-blue-50 p-4 rounded-md border border-blue-200">
            <div className="text-sm text-gray-500">Total Weight Change</div>
            <div className={`text-2xl font-bold ${data.totalWeightChange > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {data.totalWeightChange > 0 ? '+' : ''}{data.totalWeightChange} kg
            </div>
          </div>
          
          <div className="bg-green-50 p-4 rounded-md border border-green-200">
            <div className="text-sm text-gray-500">Recent Change (4 weeks)</div>
            <div className={`text-2xl font-bold ${data.recentWeightChange > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {data.recentWeightChange > 0 ? '+' : ''}{data.recentWeightChange} kg
            </div>
          </div>
        </div>
        
        {/* Nutrition Stats */}
        <div className="bg-gray-50 p-4 rounded-md">
          <h3 className="text-md font-semibold text-gray-700 mb-2">Nutrition Summary</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Calories */}
            <div>
              <div className="mb-2">
                <span className="text-sm text-gray-500">Average Daily Calories:</span>
                <span className="ml-2 font-semibold text-gray-800">{data.avgDailyCalories} kcal</span>
              </div>
              
              <div className="mb-2">
                <span className="text-sm text-gray-500">Suggested Calorie Target:</span>
                <span className="ml-2 font-semibold text-blue-600">{data.suggestedCalories} kcal</span>
              </div>
              
              {/* Calorie comparison bar chart could go here */}
              <div className="h-20">
                <BarChart
                  labels={['Current', 'Suggested']}
                  datasets={[
                    {
                      label: 'Calories',
                      data: [data.avgDailyCalories, data.suggestedCalories],
                      backgroundColor: ['rgba(107, 114, 128, 0.5)', 'rgba(37, 99, 235, 0.5)'],
                    },
                  ]}
                  title="Calorie Comparison"
                />
              </div>
            </div>
            
            {/* Macros */}
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Macronutrient Breakdown</h4>
              
              <div className="grid grid-cols-3 gap-2 mb-4">
                <div className="bg-blue-100 p-2 rounded text-center">
                  <div className="text-xs text-gray-500">Protein</div>
                  <div className="font-medium">{data.macroBreakdown.protein.grams}g</div>
                  <div className="text-xs text-gray-700">{data.macroBreakdown.protein.percentage}%</div>
                </div>
                
                <div className="bg-green-100 p-2 rounded text-center">
                  <div className="text-xs text-gray-500">Carbs</div>
                  <div className="font-medium">{data.macroBreakdown.carbs.grams}g</div>
                  <div className="text-xs text-gray-700">{data.macroBreakdown.carbs.percentage}%</div>
                </div>
                
                <div className="bg-yellow-100 p-2 rounded text-center">
                  <div className="text-xs text-gray-500">Fat</div>
                  <div className="font-medium">{data.macroBreakdown.fat.grams}g</div>
                  <div className="text-xs text-gray-700">{data.macroBreakdown.fat.percentage}%</div>
                </div>
              </div>
              
              {/* Macro breakdown bar chart */}
              <div className="h-20">
                <BarChart
                  labels={macroLabels}
                  datasets={[
                    {
                      label: 'Grams',
                      data: macroData,
                      backgroundColor: ['rgba(59, 130, 246, 0.5)', 'rgba(16, 185, 129, 0.5)', 'rgba(245, 158, 11, 0.5)'],
                    },
                  ]}
                  title="Macro Distribution"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
