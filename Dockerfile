FROM python:3.12-bullseye

WORKDIR /api
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]