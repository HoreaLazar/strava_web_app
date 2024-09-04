# 1. Start with a base image containing Python and other dependencies.
# The official Python 3.8 image is a good starting point.
FROM python:3.8-slim-buster

# 2. Set the working directory in the container.
# This is where the code will be copied to inside the container.
WORKDIR /app

# 3. Copy the requirements file to the working directory.
# This file contains all the Python dependencies.
COPY requirements.txt .

# 4. Install the dependencies from the requirements file.
# This ensures that all required Python packages are available.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code to the working directory.
# This includes all Python scripts and other necessary files.
COPY . .

# 6. Set environment variables to configure the Flask application.
# These tell Flask how to run the application inside Docker.
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 7. Expose the port that Flask will run on.
# This makes the port accessible to the outside world.
EXPOSE 8050

# 8. Command to run the application.
# This tells Docker how to start your app when the container is run.
CMD ["python", "app.py"]
