# RUN WITH COMMAND BELOW 
#docker run -d -p 8000:8000 -p 5432:5432 --env-file=.env ticdjango


# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y libpq-dev build-essential && \
    apt-get clean

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt


# Copy the code into the container
COPY . .

# Run bash file
CMD ["./start_docker.sh"]                   