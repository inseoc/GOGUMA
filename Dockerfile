FROM python:3.9.13

WORKDIR /workspace

COPY . .

RUN python -m venv venv  
ENV PATH="/app/venv/bin:$PATH"