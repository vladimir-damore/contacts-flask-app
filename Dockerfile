FROM python

LABEL org.opencontainers.image.authors="Harshit"

WORKDIR /home/web-app/

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "server.py" ]