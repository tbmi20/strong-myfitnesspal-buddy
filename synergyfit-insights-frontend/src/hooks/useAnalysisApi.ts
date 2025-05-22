// Custom hook for using the analysis API

import { useState } from 'react';
import { UserPreferences, FullApiResponse } from '@/types/api';
import { analyzeFitnessData } from '@/services/apiService';

interface UseAnalysisApiReturn {
  analyzeData: (
    strongFile: File,
    nutritionFile: File,
    weightFile: File,
    userPreferences: UserPreferences
  ) => Promise<void>;
  results: FullApiResponse | null;
  isLoading: boolean;
  error: string | null;
}

export const useAnalysisApi = (): UseAnalysisApiReturn => {
  const [results, setResults] = useState<FullApiResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeData = async (
    strongFile: File,
    nutritionFile: File,
    weightFile: File,
    userPreferences: UserPreferences
  ) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const data = await analyzeFitnessData(
        strongFile,
        nutritionFile,
        weightFile,
        userPreferences
      );
      
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      setResults(null);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    analyzeData,
    results,
    isLoading,
    error,
  };
};
