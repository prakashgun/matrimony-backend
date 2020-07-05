# Pull official base image
FROM python:3.8.3-alpine

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Copy project
COPY . /usr/src/app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]