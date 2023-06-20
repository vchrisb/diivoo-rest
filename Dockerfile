FROM python:3.11.4-slim-bookworm
ADD ./api /app
WORKDIR /app
ADD requirements.txt /
RUN pip install -r /requirements.txt

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app", "--access-logfile", "-" ]
