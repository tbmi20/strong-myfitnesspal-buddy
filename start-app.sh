#!/bin/bash
# Script to start both frontend and backend servers

echo "Starting SynergyFit Insights application..."

# Start Flask backend server
echo "Starting Flask backend server..."
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt
python3 app.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start Next.js frontend
echo "Starting Next.js frontend..."
cd "$(dirname "$0")/synergyfit-insights-frontend"
npm install
npm run dev &
FRONTEND_PID=$!

# Function to handle exit
function cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Register the cleanup function for when the script receives SIGINT
trap cleanup SIGINT

echo -e "\n============================================"
echo "SynergyFit Insights is now running!"
echo "* Backend: http://localhost:5000"
echo "* Frontend: http://localhost:3000"
echo "============================================"
echo "Press Ctrl+C to stop both servers"
echo -e "============================================"

# Wait for user to press Ctrl+C
wait
