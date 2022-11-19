FROM python:3.7-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY extract_project_requirements.txt .
RUN pip install -r extract_project_requirements.txt


# final stage
FROM python:3.7-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

COPY ./extract_project .

ENTRYPOINT ["python", "main.py"]
