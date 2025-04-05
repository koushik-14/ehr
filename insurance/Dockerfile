# Use Python as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (for Flask apps)
EXPOSE 5003

# Run the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:5003", "app:app"]
