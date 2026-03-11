FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN ls -la && ls -la SkyAp

COPY . .

CMD ["gunicorn", "SkyApp.wsgi:application", "--bind", "0.0.0.0:8000"]

