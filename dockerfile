FROM python:3.9

# Install SSH client
RUN apt-get update && apt-get install -y openssh-client

# Set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt /app/requirements.txt

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

#Copy the application to the work directory
COPY . /app/

#Start the SSH tunnel
CMD python manage.py runserver 0.0.0.0:8000

