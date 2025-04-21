
  FROM python:latest

  WORKDIR /restaurent

  COPY . .

  RUN pip install --no-cache-dir -r requirement.txt

  # Expose the port your application runs on
  EXPOSE 8000

  # Run the application
  CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]