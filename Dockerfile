FROM python:3.10.12

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

# Define environment variable to prevent buffering of Python output
ENV PYTHONUNBUFFERED 1

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]