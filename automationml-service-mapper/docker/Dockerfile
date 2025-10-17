
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY aml_service_mapper ./aml_service_mapper
COPY examples ./examples

ENV API_KEY=dev-key

EXPOSE 8000
CMD ["uvicorn", "aml_service_mapper.main:app", "--host", "0.0.0.0", "--port", "8000"]
