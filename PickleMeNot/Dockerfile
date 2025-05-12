### STAGE 1: Builder
FROM python:3.11-slim AS builder

# Create app directory
WORKDIR /app

# Add non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy project files
COPY requirements.txt ./
COPY app ./app

# Set up and install in virtual environment
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"

### STAGE 2: Runtime
FROM python:3.11-slim

# Copy virtualenv and app
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

# Activate virtualenv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

# Recreate non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# 🧹 Strip pip and setuptools
RUN rm -rf /opt/venv/lib/python3.11/site-packages/pip* \
           /opt/venv/lib/python3.11/site-packages/setuptools* \
           /opt/venv/bin/pip* \
           /opt/venv/bin/easy_install*

USER appuser

EXPOSE 8080

CMD ["/opt/venv/bin/gunicorn", "--preload", "-w", "2", "-b", "0.0.0.0:8080", "app.app:app"]

