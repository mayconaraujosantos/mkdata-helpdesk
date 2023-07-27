# Use the official Python image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /code

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /code/

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Install project dependencies
RUN pipenv install --system --deploy

# Copy the codebase to the container
COPY . /code/

# Install Node.js and npm for Angular setup
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs

# Change directory to the Angular app
WORKDIR /code/frontend

# Install Angular CLI
RUN npm install -g @angular/cli

# Install the frontend dependencies
RUN npm install

# Build the Angular app
RUN ng build --prod

# Change directory back to the project root
WORKDIR /code

# Expose the port the Django app will run on
EXPOSE 8000

# Run the Django development server
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
