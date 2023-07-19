# Install Python.
FROM python:3.10-slim-bullseye

# Set our working directory to the CropGen root folder.
WORKDIR /crop-gen

# Copy the requirements text file and ask pip to install of our packages for us.
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all of our app files (see .dockerignore for files/directories that should be ignored)
COPY . .

# Setup environment variables
ENV RUNNING_IN_DOCKER Yes

CMD [ "python", "./main.py"]