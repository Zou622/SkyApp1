FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "skyApp.wsgi:application", "--bind", "0.0.0.0:8000"]