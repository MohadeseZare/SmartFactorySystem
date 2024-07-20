# Use the official Python 3.9 image from the Docker Hub as the base image
FROM python:3.9

# Set metadata information about the image
LABEL maintainer="sh.dareshiri@gmail.com"
LABEL version="v1"

# Set the working directory inside the container to /code
WORKDIR /code

# Copy the requirements.txt file from the host to the /code directory in the container
COPY requirements.txt /code/

# Upgrade pip to the latest version
RUN pip install -U pip

# Install the python dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire content of the current directory on the host to the /code directory in the container
COPY . /code/

# Add the wait-for-it script to the /code directory in the container and ensure it is executable
COPY wait-for-it.sh /code/
RUN chmod +x /code/wait-for-it.sh

# Ensure the start.sh script in the /code directory is executable
RUN chmod +x /code/start.sh

# Expose port 8000 to allow external access to this port
EXPOSE 8000

# Set the default command to execute when the container starts
CMD ["/code/start.sh"]

