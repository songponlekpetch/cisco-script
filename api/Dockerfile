FROM python:3.10.7-bullseye


ENV PYTHONUNBUFFERED True
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD 1
ENV TZ="Asia/Bangkok"

WORKDIR /app
COPY . /app

## Install Dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl gcc gnupg libssl-dev make wget \
    && apt-get install -y gstreamer1.0-libav libnss3-tools libatk-bridge2.0-0 libcups2-dev libxkbcommon-x11-0 libxcomposite-dev libxrandr2 libgbm-dev libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

RUN chmod +x entrypoint.sh

CMD ["python", "app.py"]
