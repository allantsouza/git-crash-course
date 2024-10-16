FROM jupyter/base-notebook

# Install necessary packages
USER root
RUN apt-get update && \
    apt-get install -y x11vnc xvfb fluxbox websockify && \
    rm -rf /var/lib/apt/lists/*

# Install PyQt5
RUN pip install --no-cache-dir PyQt5

# Install noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# Copy the startup script
COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh

USER ${NB_UID}

# Expose necessary ports
EXPOSE 8888 5900 6080

# Start the services
CMD ["start.sh"]
