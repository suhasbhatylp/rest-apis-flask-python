FROM python:latest
EXPOSE 5000
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
