# Install Python using the published slim version.
FROM python:3.9-slim-buster

WORKDIR /crop-gen

# Copy the requirements text file and ask pip to install of our packages for us.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy all of our app files
COPY . .

# Setup environment variables
ENV FLASK_APP=main.py
ENV RUNNING_IN_DOCKER Yes

CMD [ "python", "./main.py", "--host", "0.0.0.0", "--port", "8000"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]