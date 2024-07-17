FROM python:3.9-slim

# Working directory in the container
WORKDIR /app

# Copy necessary contents into the container at /app
COPY http_server.py /app/http_server.py
COPY requirements.txt /app/requirements.txt

# Install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader punkt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the http server
CMD ["python", "http_server.py"]
