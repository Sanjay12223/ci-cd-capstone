# ---------- Build Stage ----------
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- Runtime Stage ----------
FROM python:3.11-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local
COPY app.py .

# Update PATH
ENV PATH=/root/.local/bin:$PATH

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
