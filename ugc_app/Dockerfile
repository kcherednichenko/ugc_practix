FROM python:3.10

WORKDIR /ugc_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN  pip install --no-cache-dir --upgrade pip && \
     pip install --no-cache-dir -r requirements.txt

COPY .. .

EXPOSE 8000

RUN chmod +x /ugc_app/entrypoint.sh

ENTRYPOINT ["/ugc_app/entrypoint.sh"]
