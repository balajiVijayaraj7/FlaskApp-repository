# official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy only the requirements file and install the Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to specify where the Flask application is
ENV FLASK_APP=app.py

# Run app.py using Flask's development server when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
