FROM python:3-slim-buster

WORKDIR /

COPY /requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "code/bot.py" ]