FROM jupyter/scipy-notebook

# Install PyQt5 and other dependencies
RUN pip install --no-cache-dir PyQt5

# Install xvfb and other necessary packages
USER root
RUN apt-get update && \
    apt-get install -y x11vnc xvfb fluxbox && \
    rm -rf /var/lib/apt/lists/*

# Copy the startup script and set permissions as root
COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh

# Switch back to the default non-root user
USER ${NB_UID}

# Expose the port for the VNC server
EXPOSE 5900

# Set the command to run when the container starts
CMD ["start.sh"]
