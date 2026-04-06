#!/bin/bash
echo "====================================================="
echo "  DRTMS — Starting Backend API"
echo "====================================================="
cd backend
python3 app.py &
BACKEND_PID=$!
sleep 2
echo ""
echo "Backend running at http://localhost:5000 (PID: $BACKEND_PID)"
echo ""
echo "Opening frontend..."
if [[ "$OSTYPE" == "darwin"* ]]; then
  open ../frontend/index.html
else
  xdg-open ../frontend/index.html 2>/dev/null || echo "Open frontend/index.html manually in your browser."
fi
echo ""
echo "Press Ctrl+C to stop the server."
wait $BACKEND_PID
