# Install Python.
FROM python:3.10-slim-bullseye 

# Set our working directory to the CropGen root folder.
WORKDIR /crop-gen

# Copy the requirements text file and ask pip to install of our packages for us.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Remove the "logs" directory if it exists
RUN if [ -d "logs" ]; then rm -rf logs; fi

# Copy all of our app files
COPY . .

# Setup environment variables
ENV RUNNING_IN_DOCKER Yes

CMD [ "python", "./main.py"]