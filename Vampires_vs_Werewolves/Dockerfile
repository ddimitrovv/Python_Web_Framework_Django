FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY manage.py /app/manage.py
COPY nginx /app/nginx
COPY media /app/media
COPY custom /app/custom
COPY static /app/static
COPY static_root /app/static_root
COPY templates /app/templates
COPY Vampires_vs_Werewolves /app/Vampires_vs_Werewolves