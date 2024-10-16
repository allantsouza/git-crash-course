#!/bin/bash
set -e

# Start the virtual framebuffer
Xvfb :1 -screen 0 1024x768x16 &

# Start a window manager
fluxbox &

# Start the VNC server
x11vnc -display :1 -N -forever -shared -rfbport 5900 &

# Run Jupyter Notebook server
jupyter notebook --ip=0.0.0.0 --no-browser
