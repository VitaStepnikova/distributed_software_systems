# 1. Python Base Image
FROM python:3.12-slim

# 2. Set up a working directory in the container
WORKDIR /app

# 3. Copy files to container
COPY requirements.txt .
COPY . .

# 4. Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Open port 50051 for gRPC
EXPOSE 50051

# 6. Launch command
CMD ["python", "grpc_server.py"]
