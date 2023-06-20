FROM python:3.11.4-slim-bookworm  as builder
ADD ./api /app
WORKDIR /app
ADD requirements.txt /
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean
RUN pip install --user -r /requirements.txt


# Here is the production image
FROM python:3.11.4-slim-bookworm as app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app", "--access-logfile", "-" ]
