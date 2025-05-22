'use client';

import { useState } from 'react';
import Layout from '@/components/Layout';
import FileUploadForm from '@/components/forms/FileUploadForm';
import UserPreferencesForm from '@/components/forms/UserPreferencesForm';
import ResultsDisplayArea from '@/components/results/ResultsDisplayArea';
import { UserPreferences, FullApiResponse } from '@/types/api';
import { useAnalysisApi } from '@/hooks/useAnalysisApi';

export default function Home() {
  // File states
  const [strongFile, setStrongFile] = useState<File | null>(null);
  const [nutritionFile, setNutritionFile] = useState<File | null>(null);
  const [weightFile, setWeightFile] = useState<File | null>(null);
  
  // User preferences state with defaults
  const [userPreferences, setUserPreferences] = useState<UserPreferences>({
    goal: 'muscle_gain',
    targetExercises: [],
    height: 175,
    age: 30,
    sex: 'M',
    activityMultiplier: 1.55
  });
  
  // API hook for analysis
  const { analyzeData, results, isLoading, error } = useAnalysisApi();
  
  // Handle analyze button click
  const handleAnalyze = async () => {
    // Validate files
    if (!strongFile || !nutritionFile || !weightFile) {
      alert('Please upload all required data files.');
      return;
    }
    
    try {
      await analyzeData(strongFile, nutritionFile, weightFile, userPreferences);
    } catch (err) {
      console.error('Analysis error:', err);
    }
  };
  
  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">SynergyFit Insights</h1>
          <p className="text-gray-600">
            Upload your Strong and MyFitnessPal data to get personalized fitness insights and recommendations.
          </p>
        </div>
        
        {/* File Upload Form */}
        <FileUploadForm
          onStrongFileChange={setStrongFile}
          onNutritionFileChange={setNutritionFile}
          onWeightFileChange={setWeightFile}
          strongFile={strongFile}
          nutritionFile={nutritionFile}
          weightFile={weightFile}
        />
        
        {/* User Preferences Form */}
        <UserPreferencesForm
          preferences={userPreferences}
          onPreferencesChange={setUserPreferences}
        />
        
        {/* Analyze Button */}
        <div className="mt-8 flex justify-center">
          <button
            onClick={handleAnalyze}
            disabled={isLoading}
            className={`
              px-6 py-3 rounded-md text-white font-medium text-lg shadow-md
              ${isLoading 
                ? 'bg-blue-400 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 active:bg-blue-800'
              }
            `}
          >
            {isLoading ? 'Analyzing...' : 'Analyze My Data'}
          </button>
        </div>
        
        {/* Loading State */}
        {isLoading && (
          <div className="mt-8 text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-gray-300 border-t-blue-600"></div>
            <p className="mt-2 text-gray-600">Analyzing your fitness data...</p>
          </div>
        )}
        
        {/* Error State */}
        {error && (
          <div className="mt-8 p-4 bg-red-50 border border-red-200 rounded-md">
            <h3 className="text-lg font-medium text-red-800 mb-1">Analysis Error</h3>
            <p className="text-red-700">{error}</p>
          </div>
        )}
        
        {/* Results Area */}
        {results && !error && !isLoading && (
          <ResultsDisplayArea results={results} />
        )}
      </div>
    </Layout>
  );
}
