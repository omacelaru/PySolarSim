# Dockerfile for PySolarSim
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for OpenGL and X11
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    xauth \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY src/ ./src/
COPY style.qss ./

# Set the entrypoint
CMD ["python", "-m", "src.main"]

# Usage (Linux):
# docker build -t pysolarsim .
# docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pysolarsim
# (Pe Windows, folosește un X server precum VcXsrv/Xming și setează DISPLAY) 