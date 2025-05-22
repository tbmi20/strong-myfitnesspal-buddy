# SynergyFit Insights - Troubleshooting Guide

This guide addresses common issues you might encounter when setting up and using the SynergyFit Insights application.

## Backend Issues

### Flask server won't start

**Symptom**: Error when trying to start the Flask server or `ModuleNotFoundError` messages

**Solutions**:

1. Ensure all Python dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Check if you're using the correct Python version (3.8+ recommended):
   ```bash
   python --version
   ```

3. If modules are still not found, try creating a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

### Flask CORS errors

**Symptom**: Frontend receives CORS errors when trying to connect to the backend

**Solutions**:

1. Ensure Flask-CORS is installed:
   ```bash
   pip install flask-cors
   ```

2. Verify that CORS is properly configured in `app.py`. It should contain:
   ```python
   from flask_cors import CORS
   
   app = Flask(__name__)
   CORS(app)  # Enable CORS for all routes
   ```

## Frontend Issues

### Frontend won't start

**Symptom**: Error when trying to start the Next.js application

**Solutions**:

1. Make sure Node.js and npm are properly installed:
   ```bash
   node --version  # Should be v18+
   npm --version
   ```

2. Verify that all dependencies are installed:
   ```bash
   cd synergyfit-insights-frontend
   npm install
   ```

3. Try clearing the Next.js cache:
   ```bash
   cd synergyfit-insights-frontend
   rm -rf .next
   npm run dev
   ```

### Connection to API fails

**Symptom**: "Network error: Unable to reach the server" message when trying to analyze data

**Solutions**:

1. Make sure the backend server is running at http://localhost:5000

2. Check that the `.env.local` file exists in the frontend directory with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```

3. Verify your browser's console for detailed error messages

### File upload issues

**Symptom**: "Missing one or more required files" error after uploading files

**Solutions**:

1. Make sure you're uploading the correct file types (CSV files)

2. Check that all three files are provided:
   - Strong workout file
   - MyFitnessPal nutrition file
   - MyFitnessPal weight file

3. Try using the sample files from the `data` directory for testing

## Data Analysis Issues

### Empty or incorrect results

**Symptom**: Analysis completes but shows incorrect or missing data

**Solutions**:

1. Check that the provided CSV files follow the expected format:
   - Strong files should contain workout data with exercises, sets, and weights
   - Nutrition files should contain daily calorie and macronutrient data
   - Weight files should contain date and weight measurements

2. Verify the dates in your files - the analysis focuses on recent data (last few weeks)

3. Try the sample files in the `data` directory to confirm functionality

## File Format Issues

### Unknown file format

**Symptom**: "File format not recognized" or parsing errors in the server logs

**Solution**:

The expected file formats are:

1. **Strong Export**: CSV with columns for workout date, exercise name, sets, reps, weight

2. **MyFitnessPal Nutrition Export**: CSV with columns for date, calories, protein, carbs, and fat

3. **MyFitnessPal Weight Export**: CSV with columns for date and weight measurements

## Getting Help

If issues persist after trying these troubleshooting steps, please:

1. Check the terminal output for both servers for error messages

2. Look at the browser console (F12) for frontend errors

3. File an issue on the GitHub repository with details about the error and steps to reproduce
