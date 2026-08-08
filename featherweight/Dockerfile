FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY featherweight_reader.py .
COPY featherweight_emulator.py .
COPY parse_gps_data.py .
COPY send_to_questdb.py .
COPY run_telemetry.py .

CMD ["python", "run_telemetry.py"]