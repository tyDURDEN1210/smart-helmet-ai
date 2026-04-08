FROM python:3.10-slim

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Ensure logs are visible
ENV PYTHONUNBUFFERED=1

# Run inference
CMD ["python", "inference.py"]