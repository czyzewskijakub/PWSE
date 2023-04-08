FROM python:3.11-slim-bullseye
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/pwse:/pwse/backend
WORKDIR /pwse
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "backend/run.py"]