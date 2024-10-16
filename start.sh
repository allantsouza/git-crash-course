#!/bin/bash
set -e

# Start the virtual framebuffer
Xvfb :1 -screen 0 1024x768x16 &

# Start a window manager
fluxbox &

# Start x11vnc server
x11vnc -display :1 -nopw -forever -shared -rfbport 5900 &

# Start noVNC
/opt/noVNC/utils/launch.sh --vnc localhost:5900 &

# Wait for X server to start
sleep 2

# Run the quiz application
python /home/jovyan/gitGame.py &

# Keep the container running
tail -f /dev/null
