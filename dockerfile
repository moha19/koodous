FROM python:3.6-alpine
COPY ./Source/requirements.txt /home
RUN pip install -r /home/requirements.txt
COPY ./Source /home
WORKDIR /home
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "mykoodous.wsgi:application", "--workers=1", "--threads=10", "--timeout=1800"]
