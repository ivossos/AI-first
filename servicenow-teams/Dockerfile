FROM python:3.12-slim
WORKDIR /app
COPY mock_servicenow.py .
ENV HOST=0.0.0.0 PORT=8080
EXPOSE 8080
CMD ["python3", "mock_servicenow.py"]
