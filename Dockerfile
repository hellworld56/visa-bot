# Use the official Playwright image with Python
FROM mcr.microsoft.com/playwright/python:v1.54.0-jammy

# Set working directory inside the container
WORKDIR /app

# Copy all files to the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 8000

# Start your app (adjust if needed)

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--log-level=info", "--access-logfile=-", "--error-logfile=-", "bot-server:app"]
