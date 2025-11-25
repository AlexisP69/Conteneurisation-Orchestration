FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY main.py .
RUN useradd -m appuser
USER appuser
EXPOSE 8000
ENV DP_ENV=dev
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
