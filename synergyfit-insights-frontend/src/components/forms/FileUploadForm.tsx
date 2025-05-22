// File Upload Form Component

'use client';

import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface FileUploadFormProps {
  onStrongFileChange: (file: File) => void;
  onNutritionFileChange: (file: File) => void;
  onWeightFileChange: (file: File) => void;
  strongFile: File | null;
  nutritionFile: File | null;
  weightFile: File | null;
}

export default function FileUploadForm({
  onStrongFileChange,
  onNutritionFileChange,
  onWeightFileChange,
  strongFile,
  nutritionFile,
  weightFile,
}: FileUploadFormProps) {
  // Dropzone for Strong workout data
  const onStrongDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onStrongFileChange(acceptedFiles[0]);
    }
  }, [onStrongFileChange]);

  const { getRootProps: getStrongRootProps, getInputProps: getStrongInputProps } = useDropzone({
    onDrop: onStrongDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    maxFiles: 1,
  });

  // Dropzone for Nutrition data
  const onNutritionDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onNutritionFileChange(acceptedFiles[0]);
    }
  }, [onNutritionFileChange]);

  const { getRootProps: getNutritionRootProps, getInputProps: getNutritionInputProps } = useDropzone({
    onDrop: onNutritionDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    maxFiles: 1,
  });

  // Dropzone for Weight data
  const onWeightDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onWeightFileChange(acceptedFiles[0]);
    }
  }, [onWeightFileChange]);

  const { getRootProps: getWeightRootProps, getInputProps: getWeightInputProps } = useDropzone({
    onDrop: onWeightDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    maxFiles: 1,
  });

  return (
    <div className="space-y-6 mb-8">
      <h2 className="text-2xl font-semibold text-gray-800">Upload Your Data Files</h2>
      
      {/* Strong Data Upload */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Strong Workout Data (CSV)</label>
        <div 
          {...getStrongRootProps()} 
          className="border-2 border-dashed border-gray-300 rounded-lg p-6 cursor-pointer hover:bg-gray-50 transition-colors"
        >
          <input {...getStrongInputProps()} />
          {strongFile ? (
            <div className="text-center">
              <p className="text-sm text-gray-600">Selected file: <span className="font-medium">{strongFile.name}</span></p>
              <p className="text-xs text-gray-500 mt-1">Click or drag to replace</p>
            </div>
          ) : (
            <div className="text-center">
              <p className="text-sm text-gray-600">Drag & drop your Strong CSV file here, or click to select</p>
              <p className="text-xs text-gray-500 mt-1">Export from Strong app → History → Export → CSV</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Nutrition Data Upload */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Nutrition Data (CSV)</label>
        <div 
          {...getNutritionRootProps()} 
          className="border-2 border-dashed border-gray-300 rounded-lg p-6 cursor-pointer hover:bg-gray-50 transition-colors"
        >
          <input {...getNutritionInputProps()} />
          {nutritionFile ? (
            <div className="text-center">
              <p className="text-sm text-gray-600">Selected file: <span className="font-medium">{nutritionFile.name}</span></p>
              <p className="text-xs text-gray-500 mt-1">Click or drag to replace</p>
            </div>
          ) : (
            <div className="text-center">
              <p className="text-sm text-gray-600">Drag & drop your MyFitnessPal Nutrition CSV file here, or click to select</p>
              <p className="text-xs text-gray-500 mt-1">Export from MyFitnessPal app → More → Export Data → Nutrition Summary</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Weight Data Upload */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Weight Measurement Data (CSV)</label>
        <div 
          {...getWeightRootProps()} 
          className="border-2 border-dashed border-gray-300 rounded-lg p-6 cursor-pointer hover:bg-gray-50 transition-colors"
        >
          <input {...getWeightInputProps()} />
          {weightFile ? (
            <div className="text-center">
              <p className="text-sm text-gray-600">Selected file: <span className="font-medium">{weightFile.name}</span></p>
              <p className="text-xs text-gray-500 mt-1">Click or drag to replace</p>
            </div>
          ) : (
            <div className="text-center">
              <p className="text-sm text-gray-600">Drag & drop your MyFitnessPal Weight CSV file here, or click to select</p>
              <p className="text-xs text-gray-500 mt-1">Export from MyFitnessPal app → More → Export Data → Measurement Summary</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
