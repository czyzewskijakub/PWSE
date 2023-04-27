FROM python:3.11-slim-bullseye
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/pwse:/pwse/backend
ENV FLASK_APP=app
COPY . /pwse
WORKDIR /pwse
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /pwse/backend

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]