FROM python

LABEL maintainer="Harshit M"

WORKDIR /home/app/

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "gunicorn", "-b", "0.0.0.0:5000", "server:app" ]