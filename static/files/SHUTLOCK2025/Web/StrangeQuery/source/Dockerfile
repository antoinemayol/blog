FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app/ ./

EXPOSE 5000

#CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]
CMD ["python3", "app.py"]

#Run en user
