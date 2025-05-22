// Recommendation Item Component

interface RecommendationItemProps {
  recommendation: string;
  index: number;
}

export default function RecommendationItem({ recommendation, index }: RecommendationItemProps) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 mb-2">
      <div className="flex gap-3">
        <div className="flex-shrink-0">
          <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-sm font-medium">
            {index + 1}
          </div>
        </div>
        <div>
          <p className="text-gray-800">{recommendation}</p>
        </div>
      </div>
    </div>
  );
}
