#!/bin/bash
# Script to test the SynergyFit Insights application with sample data

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================================${NC}"
echo -e "${BLUE}       SynergyFit Insights - Testing Instructions        ${NC}"
echo -e "${BLUE}=========================================================${NC}"
echo ""

echo -e "${GREEN}Step 1:${NC} Start the application"
echo "Run the following command in a separate terminal:"
echo -e "${YELLOW}./start-app.sh${NC}"
echo ""

echo -e "${GREEN}Step 2:${NC} Open the application in your browser"
echo -e "Visit: ${YELLOW}http://localhost:3000${NC}"
echo ""

echo -e "${GREEN}Step 3:${NC} Use the sample data files"
echo "The following sample files are available in the data directory:"
echo -e "${YELLOW}- data/strong.csv${NC} - Upload as Strong workout data"
echo -e "${YELLOW}- data/Nutrition-Summary-2025-04-15-to-2025-05-15.csv${NC} - Upload as MyFitnessPal nutrition data"
echo -e "${YELLOW}- data/Measurement-Summary-2025-04-15-to-2025-05-15.csv${NC} - Upload as MyFitnessPal weight data"
echo ""

echo -e "${GREEN}Step 4:${NC} Set your preferences"
echo "Configure your preferences with the following recommendations:"
echo "- Goal: Choose based on your preference (muscle gain, fat loss, etc.)"
echo "- Target exercises: Leave blank for automatic selection"
echo "- Height: Enter your height in cm"
echo "- Age: Enter your age in years"
echo "- Sex: Select your biological sex (for BMR/TDEE calculations)"
echo "- Activity multiplier: Choose based on your activity level"
echo ""

echo -e "${GREEN}Step 5:${NC} Analyze the data"
echo "Click the 'Analyze My Data' button and wait for results"
echo ""

echo -e "${BLUE}=========================================================${NC}"
echo -e "${BLUE}                  Troubleshooting Tips                   ${NC}"
echo -e "${BLUE}=========================================================${NC}"
echo ""

echo "If you encounter any issues:"
echo ""
echo "1. Check if both servers are running:"
echo "   - Backend: http://localhost:5000"
echo "   - Frontend: http://localhost:3000"
echo ""
echo "2. Verify that all Python dependencies are installed:"
echo -e "${YELLOW}pip install -r requirements.txt${NC}"
echo ""
echo "3. Ensure Node.js dependencies are installed:"
echo -e "${YELLOW}cd synergyfit-insights-frontend && npm install${NC}"
echo ""
echo "4. Check browser console for frontend errors"
echo ""
echo "5. Check the terminal running the servers for backend errors"
echo ""

echo -e "${BLUE}=========================================================${NC}"
echo -e "${BLUE}                  Happy fitness tracking!                ${NC}"
echo -e "${BLUE}=========================================================${NC}"
