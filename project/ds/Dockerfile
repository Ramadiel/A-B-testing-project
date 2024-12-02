# Use the official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project-specific folders into the container
COPY data /app/data
COPY scripts /app/scripts

# Set the default command to open a shell (can be overridden)
CMD ["bash"]

