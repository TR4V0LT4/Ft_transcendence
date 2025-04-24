# Use the official Python base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files to the container
COPY . /code/

# Set up PostgreSQL
RUN apt-get update && apt-get install -y postgresql
RUN apt-get update && apt-get install -y nodejs npm
# ENV DATABASE_URL postgres://postgres:postgres@db:5432/mydatabase

# Expose the Django development server port
EXPOSE 8000

COPY ./scripts/script.sh /scripts/script.sh
RUN chmod +x /scripts/script.sh
# Start the Django development server
ENTRYPOINT /scripts/script.sh