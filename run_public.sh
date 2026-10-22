#!/bin/bash
# ========================================================
# SunLoop: Public Instant Tunnel & Startup Script
# ========================================================

echo "Starting SunLoop Streamlit Server on port 8501..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false &

sleep 3

echo "========================================================"
echo " Launching Instant Public Sharing Tunnel (Pinggy)"
echo " Anyone can open this link on their mobile or computer!"
echo "========================================================"

# Expose port 8501 via Pinggy SSH tunnel
ssh -p 443 -o StrictHostKeyChecking=no -R0:localhost:8501 a.pinggy.io
