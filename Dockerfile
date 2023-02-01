# Install Python using the published slim version.
FROM python:3.9-slim-buster

WORKDIR /crop-gen

# Copy the requirements text file and ask pip to install of our packages for us.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy all of our app files
COPY . .

# Setup environment variables
ENV RUNNING_IN_DOCKER Yes

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]