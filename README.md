# SynergyFit Insights

A comprehensive fitness analysis tool that processes data from Strong (workout tracking) and MyFitnessPal (nutrition and weight tracking) to provide actionable insights for your fitness journey. The application includes both a Python core analysis engine and a modern web interface.

## Web Application (New!)

SynergyFit Insights now includes a full web application with an intuitive interface built on Next.js and a Flask API backend. The web app makes it easy to:

- Upload your fitness data files in a user-friendly interface
- Customize your analysis with preference settings
- View beautiful interactive charts of your workout and nutrition progress
- Get personalized recommendations based on your goals
- Track your progress over time

### Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Chart.js, React Query
- **Backend**: Flask, Pandas, NumPy

### Running the Web Application

To start both the frontend and backend servers with a single command:

```bash
./start-app.sh
```

Then open your browser to http://localhost:3000

## Core Python Analysis Engine

### Overview

The Strong-MyFitnessPal Buddy is a Python-based engine that takes exported data from fitness apps and generates actionable recommendations regarding:

- Progressive overload for strength training
- Nutrition optimization based on your goals
- BMR/TDEE adjustments for weight management
- Exercise progression tracking

### Features

- **Data Import & Processing**
  - Parse workout data from Strong CSV exports
  - Process nutrition data from MyFitnessPal CSV exports
  - Analyze weight trends from measurement tracking

- **Workout Analysis**
  - Track progress for each exercise over time
  - Calculate estimated one-rep max (1RM) values
  - Identify stalled lifts that need attention
  - Analyze workout volume and frequency

- **Nutrition Analysis**
  - Calculate daily calorie and macronutrient intake
  - Track weight changes over time
  - Estimate TDEE (Total Daily Energy Expenditure)
  - Evaluate protein intake adequacy for goals

- **Actionable Insights**
  - Generate specific recommendations for training
  - Provide nutrition adjustments based on goals
  - Suggest calorie targets for muscle gain or fat loss
  - Evaluate alignment between actions and stated goals

### Getting Started

1. **Export your fitness data**
   - Export your workout history from Strong app
   - Export nutrition data from MyFitnessPal/SynergyFit
   - Export weight measurements from MyFitnessPal/SynergyFit

2. **Place the data files in the `/data` directory**

3. **Run the analysis**
   ```bash
   python main.py
   ```

### Requirements

- Python 3.8+
- pandas
- numpy

Install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install pandas numpy
```

## Project Structure

```
fitness_analyzer/
├── main.py                 # Main script to run analysis
├── parsers/                # Data import modules
│   ├── strong_parser.py    # Process Strong workout data
│   ├── mfp_parser.py       # Process MyFitnessPal nutrition data
│   └── base_parser.py      # Base class for parsers
├── analysis/               # Analysis modules
│   ├── workout_analysis.py # Analyze workout progress
│   ├── nutrition_analysis.py # Analyze nutrition data
│   └── insights.py         # Generate recommendations
├── utils/                  # Utility functions
│   └── formulas.py         # BMR, TDEE, 1RM formulas
└── data_models/            # Data structure definitions
    ├── workout_models.py   # Workout data structures
    └── nutrition_models.py # Nutrition data structures
```

## Web Application Setup and Usage

### Prerequisites

- Node.js (v18 or later)
- Python 3.8+
- pip (Python package manager)
- npm (Node package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/strong-myfitnesspal-buddy.git
   cd strong-myfitnesspal-buddy
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```
   cd synergyfit-insights-frontend
   npm install
   ```

### Running the Application

#### Option 1: Using the start script

Simply run:
```
./start-app.sh
```

This will start both the backend and frontend servers.

#### Option 2: Starting servers manually

1. Start the backend server:
   ```
   # In the project root directory
   python app.py
   ```

2. In a separate terminal, start the frontend server:
   ```
   # Navigate to frontend directory
   cd synergyfit-insights-frontend
   npm run dev
   ```

3. Open your browser and navigate to:
   - Frontend: http://localhost:3000
   - API (backend): http://localhost:5000

### Using the Application

1. **Prepare your data files**:
   - Export your workout data from Strong app as CSV
   - Export your nutrition diary from MyFitnessPal as CSV
   - Export your weight tracking data from MyFitnessPal as CSV

2. **Upload your files**:
   - Use the file upload forms on the main page
   - Ensure you select the correct file for each input

3. **Configure your preferences**:
   - Set your fitness goals
   - Enter personal details like height, weight, and age
   - Select target exercises for detailed analysis

4. **Analyze your data**:
   - Click the "Analyze My Data" button
   - Wait for the analysis to complete (this may take a few moments)

5. **Review your insights**:
   - Explore the generated charts and visualizations
   - Read through personalized recommendations
   - Use the insights to adjust your training and nutrition

## License

[MIT License](LICENSE)