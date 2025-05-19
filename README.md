# Strong-MyFitnessPal Buddy

A comprehensive fitness analysis tool that processes data from Strong (workout tracking) and MyFitnessPal/SynergyFit (nutrition and weight tracking) to provide actionable insights for your fitness journey.

## Core Python Analysis Tool

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

## Future Development

### Web Application (Coming Soon)

*This section will be expanded as the web application is developed.*

In the future, this project will be extended with a web-based interface that provides:

- Interactive dashboards for visualizing progress
- Easy data import and management
- Goal setting and tracking
- Customizable reports and recommendations

Stay tuned for updates on the web application development!

## License

[MIT License](LICENSE)