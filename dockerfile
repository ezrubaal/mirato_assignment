FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports for webhook (8443) and Prometheus metrics (9000)
EXPOSE 8443 9000

# Run the application
CMD ["python", "resource_injector.py"]