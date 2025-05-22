// Summary Card Component

import { AnalysisSummary } from '@/types/api';

interface SummaryCardProps {
  data: AnalysisSummary;
}

export default function SummaryCard({ data }: SummaryCardProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Summary</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="border rounded-md p-4 bg-blue-50">
          <div className="text-sm font-medium text-gray-500">Estimated TDEE</div>
          <div className="text-2xl font-bold text-blue-700">
            {data.estimatedTDEE} <span className="text-sm font-normal">kcal</span>
          </div>
          <div className="text-xs text-gray-600 mt-1">Total Daily Energy Expenditure</div>
        </div>
        
        <div className="border rounded-md p-4 bg-gray-50">
          <div className="text-sm font-medium text-gray-500">Current BMR</div>
          <div className="text-2xl font-bold text-gray-700">
            {data.currentBMR} <span className="text-sm font-normal">kcal</span>
          </div>
          <div className="text-xs text-gray-600 mt-1">Basal Metabolic Rate</div>
        </div>
        
        <div className="border rounded-md p-4 bg-green-50">
          <div className="text-sm font-medium text-gray-500">Suggested Calorie Target</div>
          <div className="text-2xl font-bold text-green-700">
            {data.suggestedCalorieTarget} <span className="text-sm font-normal">kcal</span>
          </div>
          <div className="text-xs text-gray-600 mt-1">Based on your goals</div>
        </div>
      </div>
      
      {data.keyRecommendation && (
        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
          <h3 className="text-sm font-medium text-gray-700">Key Recommendation:</h3>
          <p className="text-base text-gray-800">{data.keyRecommendation}</p>
        </div>
      )}
    </div>
  );
}
