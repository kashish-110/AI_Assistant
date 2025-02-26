from python
Set the working directory inside the container
WORKDIR /app

# Copy all files from your project directory to the container
COPY . /app

# Install required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI’s default port (8000)
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "help:app", "--host", "0.0.0.0", "--port", "8000"]