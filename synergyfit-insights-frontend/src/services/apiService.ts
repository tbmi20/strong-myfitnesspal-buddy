// API service for making API calls to the backend

import axios from 'axios';
import { UserPreferences, FullApiResponse } from '@/types/api';

// Get the API URL from environment variables or use default
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

/**
 * Analyze fitness data by sending files and user preferences to the backend
 */
export const analyzeFitnessData = async (
  strongFile: File,
  nutritionFile: File,
  weightFile: File,
  userPreferences: UserPreferences
): Promise<FullApiResponse> => {
  try {
    const formData = new FormData();
    
    // Append files
    formData.append('strong_file', strongFile);
    formData.append('nutrition_file', nutritionFile);
    formData.append('weight_file', weightFile);
    
    // Append user preferences as JSON
    formData.append('user_preferences_json', JSON.stringify(userPreferences));
    
    // Make the API call
    const response = await axios.post(`${API_URL}/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  }  catch (error) {
    if (axios.isAxiosError(error)) {
      // Handle Axios errors
      if (error.response) {
        // Server responded with non-2xx status
        const errorMsg = error.response.data.error || error.response.data.message || 'Unknown server error';
        console.error('API Error Response:', error.response.data);
        throw new Error(`Server error (${error.response.status}): ${errorMsg}`);
      } else if (error.request) {
        // Request was made but no response received
        console.error('Network Error:', error.request);
        throw new Error('Network error: Unable to reach the server. Please check if the backend is running at ' + API_URL);
      } else {
        // Request setup error
        console.error('Request Error:', error.message);
        throw new Error(`Request setup error: ${error.message}`);
      }
    }
    
    // Handle other errors
    console.error('Unexpected Error:', error);
    throw new Error('An unexpected error occurred. Please check the console for details.');
  }
};
